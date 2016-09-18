import logging
import argparse

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


def read_arguments():
    """
    Read commandline arguments that alter behavior of this program.
    :return:
    """
    parser = argparse.ArgumentParser(description='Auction Fetcher')
    # currently we only allow scraping of one site only
    parser.add_argument('site', help="base url (drop the www.) of the website to crawl")
    parser.add_argument('item', help='description of the item you want to search')

    # search options
    parser.add_argument('-o', '--options', type=str, help='comma separated list of options in the opt=value format')
    parser.add_argument('-c', '--count', type=int, default=0, help='number of cycles to perform, 0 means infinite')

    parser.add_argument('--log', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="specify log level")

    return parser.parse_args()


def main():
    args = read_arguments()

    if args.log is not None:
        # set the root logger level
        numeric_level = getattr(logging, args.log.upper())
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log.upper())

        logging.basicConfig(level=numeric_level)

    logging.info("invoked with args:" + str(args))

    driver_class = find_driver(args.site)

    if driver_class is None:
        logging.error("error - %s is not yet supported" % args.site)
        return

    driver = driver_class()

    # specify options for this query
    options = drivers.base.QueryOptions(item_name=args.item)

    infinite = True if args.count == 0 else False

    while infinite or args.count > 0:
        args.count -= 1
        items = query.query_items(driver, options)
        if items is not None and len(items) > 0:
            logging.info("listing found items: \n")
            for item in items:
                logging.info(item.to_string())

            # TODO invoke post-processor
        else:
            logging.warning("no results found")

    logging.info("program exiting")

if __name__ == "__main__":
    main()
