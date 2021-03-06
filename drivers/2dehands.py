# -*- coding: utf-8 -*-
__author__ = 'simon'

import logging
import re

import urllib.request

from pyquery import PyQuery
from drivers import base


class _2dehands_be(base._AuctionSite):
    SEARCH_ITEM = "/markt/2/"
    LOCALE_INFO = "/?locale=all&p=be"
    PRICE_MIN = "&prijsmin="
    PRICE_MAX = "&prijsmax="
    SORT_DATE_ASC = "&sort=datum_asc"
    SORT_DATE_DESC = "&sort=datum_desc"
    OFFSET = "&offset="

    """
    Class for the auction site www.2dehands.be
    """

    def __init__(self):
        self.base_url = "http://www.2dehands.be"
        self.logger = logging.getLogger("2dehands-driver")

    def create_GET_query(self, options):
        """
        The create_GET_query method is able to create a query URL for this site based on passed options.
        Note that this only works for auction sites in which queries are done using GET.
        Subclasses must not implement this class.

        :return: a URL that should be queried by the query engine.
        """
        query_url = self.base_url
        if options is None:
            raise SystemError("options cannot be None, need at least the item_name option")

        if "item_name" not in options.__dict__:
            raise KeyError("missing mandatory item_name option!")
        else:
            # add this first!
            query_url = self.add_option_item_name(query_url, options.__dict__["item_name"])

        # this part assumes that option ordering in the URL does not matter!
        for option in options.__dict__.keys():
            try:
                # this one's already added
                if option == "item_name":
                    continue

                # check if function is supported
                method = getattr(self, "add_option_" + option)
                query_url = method(query_url, options.__dict__[option])
            except AttributeError as e:
                self.logger.warning(str(e))

        return query_url

    @staticmethod
    def parse_article_page(html, item):
        """
        Parse html of an article entry in the query result page.
        If this fails for some reason, return None so that the user is not bothered with it.
        :param html: portion that contains article info.
        :param item: AuctionItem that will contain parsed data.
        :return: True if parse was successful, False if not.
        """
        # parse out the bullshit
        pq = PyQuery(html)
        div_item = pq('div#item-id.item')

        # get the separate fields
        pq = PyQuery(div_item)
        item.title = pq('div.title-wrapper>h1').text()
        item.price = pq('span.price').text()
        item.description = pq('div.item-details').text()

        return True

    @staticmethod
    def get_num_pages_and_offset(html):
        pq = PyQuery(html)

        # get number of pages in search result
        pages_div = pq('ul.page-count>li')
        if pages_div is None or len(pages_div) <= 0:
            logging.warning("could not get page count or is 0")
            return [0, 0]

        if len(pages_div) == 1:
            # offset doesn't matter in this case
            return [1, 0]

        # if more than 1 we need the offset
        pq = PyQuery(pages_div[1])
        a = pq('a')
        offset_href = a[0].attrib['href']
        if not offset_href:
            return [0, 0]
        else:
            offset_array = offset_href.split('=')
            offset = int(offset_array[-1]) if offset_array else 0

        # also get num pages
        pq = PyQuery(pages_div[-1])
        a = pq('a')
        num_pages = int(a.text())

        return [num_pages, offset]

    @staticmethod
    def parse_html_page(html):
        """
        2dehands.be sends back a html object.
        We can parse it in this function.
        :type html: html data
        """
        items = []

        pq = PyQuery(html)
        search_div = pq('div.search-result')
        pq = PyQuery(search_div)
        articles = pq('article>div>a')
        for article in articles:
            item = base.AuctionItem()
            # get html for the article
            url = article.attrib['href']

            req = urllib.request.Request(url)
            html = urllib.request.urlopen(req)
            if html is None:
                continue

            if _2dehands_be.parse_article_page(html.read(), item):
                # fill in the url
                item.url = url
                # magic to find the id
                end = url.rfind('.html')
                begin = url.rfind('-') + 1
                item.id = url[begin:end]
                items.append(item)

        return items

    def query_html_page(self, url):
        """
        Query a page with given url or return None if failed.
        :param url: query url
        :return: a html
        """
        self.logger.info("querying: %s" % url)
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            return the_page

        return None

    def perform_query(self, options, max_items=50):
        items = []
        query_url = self.create_GET_query(options)
        self.logger.info("created GET query url: {0}".format(query_url))

        # first determine how many pages with results there are
        page = self.query_html_page(query_url)
        if page is None:
            return items

        values = self.get_num_pages_and_offset(page)
        pages = values[0]
        offset = values[1]
        self.logger.debug("pages found: %d - offset: %d" % (pages, offset))

        current_page = 0
        while current_page < pages:
            page_url = query_url
            # although we already queried page 1 we do it again, for ease
            page = self.query_html_page(self.add_option_offset(page_url, current_page * offset))
            if page is not None:
                new_items = self.parse_html_page(page)
                if new_items is not None:
                    self.logger.info("found %d items on page %d" % (len(new_items), current_page + 1))
                    left = max_items - len(items)

                    if left > len(new_items):
                        # we can add all the items
                        items += new_items
                    else:
                        # need to add subset
                        items += new_items[0:left]
                        # add this point max items has been reached (this is why else is <=)
                        self.logger.info("reached max items")
                        break
                else:
                    self.logger.warning("no items on found for URL %s" % page_url)
            else:
                self.logger.warning("page for %s was None" % page_url)

            current_page += 1

        return items

    @staticmethod
    def encode_value(value):
        # only does space replacement for now
        value = re.sub(' ', '%20', value)
        return value

    """
    Functions to support query options
    """
    def add_option_item_name(self, url, value):
        return url + self.SEARCH_ITEM + self.encode_value(value) + self.LOCALE_INFO

    def add_option_min_price(self, url, value):
        return url + self.PRICE_MIN + str(value)

    def add_option_max_price(self, url, value):
        return url + self.PRICE_MAX + str(value)

    # if this option is supported, a smart query can be done!
    def add_option_sort_date_asc(self, url):
        return url + self.SORT_DATE_ASC

    def add_option_sort_date_desc(self, url):
        return url + self.SORT_DATE_DESC

    def add_option_offset(self, url, value):
        if value == 0:
            # not needed to include offset in url for 0 value
            return url
        else:
            return url + self.OFFSET + str(value)
