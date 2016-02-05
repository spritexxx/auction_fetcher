"""
Contains base classes for the drivers.
"""
__author__ = 'simon'


class QueryOptions:
    """
    Models
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class AuctionItems(object):
    # TODO define...
    pass


class _AuctionSite(object):
    """
    Models an Auction Site.
    This class needs to be extended for each supported auction site.

    You should not create an object of this class directly!
    """

    def formatter(self, options):
        """
        A formatter is able to create a query URL for this site based on passed options.
        :return: a URL that should be queried by the query engine.
        """
        query_url = self.base_url

        # TODO check that options contain mandatory item_name!

        for key in options.__dict__.keys():
            function_name = self.__dict__.get(key, None)
            if function_name is not None:
                print("got function {0}".format(function_name))
            else:
                print("not found")

        return query_url

    def get_formatter(self):
        """
        Get the formatter for this auction site.
        :return:
        """
        return self.formatter

    def parser(self, html_doc):
        """
        Parser function that can interpret the html_doc for this auction site.
        :return: an AuctionItems object or None in case there were none.
        """
        items = AuctionItems()
        return items

    def get_parser(self):
        return self.parser
