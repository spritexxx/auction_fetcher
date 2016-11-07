"""
Contains base classes for the drivers.
"""
__author__ = 'simon'

from hashlib import md5

class QueryOptions:
    """
    Models options that can be given to a Query.
    TODO: standardize option names but keep open for extra options.
    Drivers must be able to handle these options but they do not
    need to support all options. If an unsupported option is passed to a driver it
    may simply ignore it and print a warning.
    """

    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class Vendor(object):
    """
    Models a vendor of an AuctionItem
    """

    def __init__(self):
        self.name = ""
        self.email = ""
        self.phone_number = ""


class AuctionItem(object):
    """
    Models an auction item.

    Items from auction sites should be parsed into objects of this class for
    easy usage elsewhere.
    """

    def __init__(self):
        # unique ID for this item MUST always be set!
        self.id = ""
        self.title = ""
        self.price = ""
        self.description = ""

        self.price_descr_hash = ""

        self.url = ""
        # save this as a string because some sites have string prices
        # e.g 'prijs overeen te komen' on 2dehands.be
        self.list_img_url = ""
        self.item_img_urls = []

        # fill in if found...
        self.vendor = None

    def to_string(self):
        string = "Title: " + self.title + "\n"
        string = string + "URL: " + self.url + "\n"
        string = string + "Price: " + self.price + "\n"
        string = string + "Description: " + self.description + "\n"
        string = string + "ID: " + self.id + "\n"
        string = string + "Hash: " + self.get_item_hash() + "\n"
        return string

    def get_item_hash(self):
        """
        This is used to detect changes in an auction item.
        :return:
        """
        if self.price_descr_hash == "":
            self.price_descr_hash = md5((self.price + self.description).encode()).hexdigest()

        return self.price_descr_hash


class _AuctionSite(object):
    """
    Models an Auction Site.
    This class needs to be extended for each supported auction site.

    You should not create an object of this class directly!
    See 2dehands.py for an example of a driver implementing this interface.
    """

    def perform_query(self, options, max_items=100):
        """
        Perform a query to obtain the unparsed items matching the query incl. options.
        :param options: options for the query.
        :param max_items: max AuctionItems that are queried/returned.
        :return: list of AuctionItems. An empty list is returned in case none where found.
        """
        raise NotImplementedError("actual driver must implement this function")
