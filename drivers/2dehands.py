# -*- coding: utf-8 -*-
__author__ = 'simon'

import logging
import re

import urllib.request

from pyquery import PyQuery
from drivers import base


class _2dehands_be(base._AuctionSite):
    SEARCH_ITEM = "/markt/2/"
    LOCALE_INFO = "/?locale=nl&p=be"
    PRICE_MIN = "&prijsmin="
    PRICE_MAX = "&prijsmax="

    """
    Class for the auction site www.2dehands.be
    """

    def __init__(self):
        self.base_url = "http://www.2dehands.be"

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
                logging.warning(str(e))

        return query_url

    def perform_query(self, options):
        query_url = self.create_GET_query(options)
        print("Created GET query url: {0}".format(query_url))
        req = urllib.request.Request(query_url)

        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            return the_page

        logging.error("query failed for %s..." % query_url)
        return None

    def parse_article(self, html):
        """
        Parse html of an article.
        If this fails for some reason, return None so that the user is not bothered with it.
        """
        item = base.AuctionItem()
        # parse out the bullshit
        pq = PyQuery(html)
        div_item = pq('div#item-id.item')

        # get the separate fields
        pq = PyQuery(div_item)
        item.title = pq('div.title-wrapper>h1').text()
        item.price = pq('span.price').text()
        item.description = pq('div.item-details').text()

        return item

    def parse_response(self, response):
        """
        2dehands.be sends back a html object.
        We can parse it in this function.
        """
        items = []
        pq = PyQuery(response)
        search_div = pq('div.search-result')
        pq = PyQuery(search_div)
        articles = pq('article>div>a')
        # TODO multiple pages containing results
        logging.info("Found {0} articles.".format(len(articles)))
        for article in articles:
            # get html for the article
            url = article.attrib['href']

            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            if response is None:
                continue

            item = self.parse_article(response.read())
            # if it was successfully parsed
            if item is not None:
                # fill in the url
                item.url = url
                # magic to find the id
                end = url.rfind('.html')
                begin = url.rfind('-') + 1
                item.unique_id = url[begin:end]
                items.append(item)

        return items

    def encode_value(self, value):
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
