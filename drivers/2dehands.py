__author__ = 'simon'

import base


class _2dehands_be(base._AuctionSite):
    """
    Class for the auction site www.2dehands.be
    """

    def __init__(self):
        self.base_url = "www.2dehands.be"
        self.__dict__["item_name"] = "add_option_item_name"
        self.__dict__["min_price"] = "add_option_min_price"
        self.__dict__["max_price"] = "add_option_max_price"


    def add_option_item_name(self, url, value):
        print("adding item_name={1}".format(value))

    def add_option_min_price(self, url, value):
        print("adding min_price={1}".format(value))

    def add_option_max_price(self, url, value):
        print("adding max_price={1}".format(value))
