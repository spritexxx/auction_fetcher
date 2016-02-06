"""
Contains base classes for the drivers.
"""
__author__ = 'simon'

import logging
import urllib2


class QueryOptions:
    """
    Models
    """

    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class AuctionItems(object):
    pass


class _AuctionSite(object):
    """
    Models an Auction Site.
    This class needs to be extended for each supported auction site.

    You should not create an object of this class directly!
    See 2dehands.py for an example of a driver implementing this interface.
    """

    def perform_query(self, options):
        """
        Perform a query to obtain the unparsed items matching the query incl. options.
        :param options: options for the query.
        :return:
        """
        raise NotImplementedError("actual driver must implement this function")

    def add_option_item_name(self, url, value):
        """
        Function that adds the item_name option to the query url.
        E.g in case you are searching for a ps4 on 2dehands.be this would work as follows:

        base_url=www.2dehands.be
        item_name=ps4

        resulting query url returned by this function:
        www.2dehands.be/search/ps4/? (this is just an example, this depends on the site's API!)

        :param value: item name's value that should be added in the query url
        :return: updated query url that is capable of querying items with the specified value
        """
        raise NotImplementedError("actual driver MUST implement this function")

    def parse_response(self, response):
        """
        Parser function that can interpret the response for this auction site.
        :return: an AuctionItems object or None in case there were none.
        """
        raise NotImplementedError("actual driver MUST implement this function")


class _AuctionSiteUsingGET(_AuctionSite):
    """
    Base class containing common functionality for Auction Sites that perform their lookups using HTTP GET.
    """

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

        if not options.__dict__.has_key("item_name"):
            raise KeyError("missing mandatory item_name option!")

        for option in options.__dict__.keys():
            try:
                # check if function is supported
                method = getattr(self, "add_option_" + option)
                query_url = method(query_url, options.__dict__[option])
            except AttributeError as e:
                logging.warning(e.message)

        return query_url

    def perform_query(self, options):
        raise NotImplementedError("driver MUST implement this")

