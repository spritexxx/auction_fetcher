__author__ = 'simon'

import base


class _2dehands_be(base._AuctionSite):
    """
    Class for the auction site www.2dehands.be
    """

    def __init__(self):
        self.base_url = "www.2dehands.be"

    """
    Functions to support query options
    """
    def add_option_item_name(self, value):
        print("adding item_name={0}".format(value))

    def add_option_min_price(self, value):
        print("adding min_price={0}".format(value))

    def add_option_max_price(self, value):
        print("adding max_price={0}".format(value))
