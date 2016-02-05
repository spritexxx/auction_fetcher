"""
Query Module
    Module taking care of fetching data from the world wide web.
"""
__author__ = 'simon'

import drivers.base

def query_items(driver, options):
    """
    Query items from a certain auction site.

    :param url: url of the auction site (drop www or http(s)://).
    Based on this url a formatter function will be searched in the format DB.
    A formatter can create the correct query function that contains the specified options.

    :param options: QueryOptions to be passed in the query.
    The allowed options depend on the formatter.
    The item_name is a mandatory option!

    :return: json-list of items matching the query.
    """
    formatter = driver.get_formatter()

    # TODO perform query
    # item_name is a mandatory option!!!
    options = drivers.base.QueryOptions(item_name="ps4", min_price=150, max_price=275)
    query_url = formatter(options)
    return None

