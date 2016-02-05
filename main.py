import logging

import drivers
import query

__author__ = 'simon'


def find_driver(url):
    # put url in proper format
    name = "_" + url.replace(".", "_")

    cls = drivers.supported_drivers.get(name, None)
    return cls


def main():
    # TODO options for the runner, how long it runs etc... How much time between queries...
    # TODO non-hardcoded url & options in future

    driver_class = find_driver("ebay.be")

    if driver_class is None:
        logging.error("error - this site is not yet supported...")
    else:
        print("got driver!")

    driver = driver_class()

    items = query.query_items(driver, None)
    if items is not None:
        print("Nice we have found some data")
        # TODO check if we have parser for this url
        # TODO invoke parser if we have one!
    else:
        print("Oops, no results...")
        # TODO invoke actuator


if __name__ == "__main__":
    main()
