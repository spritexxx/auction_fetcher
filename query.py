"""
Query Module
    Module taking care of fetching data from the world wide web.
"""
__author__ = 'simon'

import urllib2
import drivers.base


def query_items(driver, options):
    """
    Query items from a certain auction site.

    :param options: QueryOptions to be passed in the query.
    The allowed options depend on the formatter.
    The item_name is a mandatory option!

    :return: list of AuctionItems objects based on result of the query.
    Can be empty if none were found.
    """
    # item_name is a mandatory option!!!
    unparsed_data = driver.perform_query(options)
    # let the driver parse the data
    items = driver.parse_response(unparsed_data)
    return items

