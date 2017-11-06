import argparse
import logging
import os
import sys

# important to load analyzers - do NOT remove below line
# @formatter:off
import analyzers
# @formatter:on
import logreader


def main():
    # list all available analyzers by name
    available_analyzers = [
        'hourly_peak', 'hourly_requests_by_host', 'hourly_requests_to_server',
        'param_count', 'param_extra', 'param_length', 'response_code',
        'response_size_centroidmedian', 'response_size_dbscan',
        'response_size_elliptic', 'response_size_dendogramhac',
        'response_size_kmeans', 'response_size_knn', 'response_size_lof',
        'response_size_meanshift', 'response_size_singlecomplete',
        'response_size_wardavg', 'response_status', 'url_requested',
        'url_requested_lots', 'url_requested_once', 'verb'
    ]

    parser = argparse.ArgumentParser(description='Get more from your logs.')

    parser.add_argument('logfile', help='the web application log to parse')
    parser.add_argument(
        '-c', '--config', nargs=1, metavar='', help='a configuration file')
    parser.add_argument(
        '-d', '--debug', action='store_true', help='output debug information')
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='output additional information')
    parser.add_argument(
        '-a', '--all', action='store_true', help='run all analyzers')

    # add a cli switch for each analyzer
    for analyzer in available_analyzers:
        parser.add_argument('--' + analyzer, action='store_true')

    args = parser.parse_args()

    # default to info, override to debug if specified
    loglevel = "INFO"
    if args.verbose:
        loglevel = "DEBUG"

    # configure logging
    logging.basicConfig(
        stream=sys.stdout, level=os.environ.get("LOGLEVEL", loglevel))

    # read log file
    accesslog = logreader.parse(args.logfile)

    # run analysis for all analyzers
    if args.all:
        for analyzer in available_analyzers:
            # dynamically reference analyzer in global lookup
            sys.modules['analyzers.' + analyzer].analyze(accesslog)

    else:
        for analyzer in available_analyzers:
            # check for key in dictionary of args
            if vars(args)[analyzer]:
                # print sys.modules.keys()
                # dynamically reference analyzer in global lookup
                sys.modules['analyzers.' + analyzer].analyze(accesslog)


if __name__ == "__main__":
    main()
