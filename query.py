"""
Query Module
    Module taking care of fetching data from the world wide web.
"""
__author__ = 'simon'

import logging


def query_items(driver, options):
    """
    Query items from a certain auction site.

    :param options: QueryOptions to be passed in the query.
    The allowed options depend on the formatter.
    The item_name is a mandatory option!

    :return: list of AuctionItems objects based on result of the query.
    Can be empty if none were found.
    """
    # E.g check for mandatory options
    # item_name is a mandatory option!!!
    # TODO better define the Query Options
    # TODO options must be able to validate themselves!
    # TODO remove hard-coded max_items, should be an option!
    items = driver.perform_query(options, 25)
    if items is None:
        logging.warning("response was none...")
        return items

    # TODO weed out items that have been reported already
    return items

