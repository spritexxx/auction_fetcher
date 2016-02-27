import logging

import drivers
import query

__author__ = 'simon'


def find_driver(url):
    """
    Find a supporting driver for the auction site with specified url.
    :rtype : class of the supporting driver
    """
    name = "_" + url.replace(".", "_")

    cls = drivers.supported_drivers.get(name, None)
    return cls


def main():
    # TODO options for the runner, how long it runs etc... How much time between queries...
    # TODO non-hardcoded url & options in future
    driver_class = find_driver("2dehands.be")

    if driver_class is None:
        logging.error("error - this site is not yet supported...")
        return

    driver = driver_class()

    # specify options for this query
    options = drivers.base.QueryOptions(item_name="iphone 6s", min_price=400, max_price=700, unsupported_option=1)
    items = query.query_items(driver, options)
    if items is not None:
        # TODO invoke actuator
        print("Found some items: \n")
        for item in items:
            print(item.to_string())
    else:
        print("Oops, no results...")


if __name__ == "__main__":
    main()
