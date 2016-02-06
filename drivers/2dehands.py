__author__ = 'simon'

import base
import logging
import urllib2


class _2dehands_be(base._AuctionSiteUsingGET):
    SEARCH_ITEM = "/markt/2/"

    """
    Class for the auction site www.2dehands.be
    """

    def __init__(self):
        self.base_url = "http://www.2dehands.be"

    def perform_query(self, options):
        query_url = self.create_GET_query(options)
        logging.debug("created GET query url: {0}".format(query_url))
        req = urllib2.Request(query_url)

        response = urllib2.urlopen(req)
        if response is not None:
            the_page = response.read()
            return the_page
        else:
            logging.info("response was None...")
            return None

    def parse_response(self, response):
        """
        2dehands.be sends back a html object.
        We can parse it in this function.
        """
        items = base.AuctionItems()
        print(response)
        return items

    """
    Functions to support query options
    """
    def add_option_item_name(self, url, value):
        return url + self.SEARCH_ITEM + value

    def add_option_min_price(self, url, value):
        print("adding min_price={0}".format(value))
        return url

    def add_option_max_price(self, url, value):
        print("adding max_price={0}".format(value))
        return url
