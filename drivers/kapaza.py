__author__ = 'simon'

from drivers import base


class _kapaza_be(base._AuctionSite):
    def __init__(self):
        self.base_url = "www.kapaza.be"
