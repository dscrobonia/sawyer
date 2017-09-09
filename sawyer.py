import argparse
import logreader
import analyzers

parser = argparse.ArgumentParser(description='Get more from your logs.')

parser.add_argument('logfile', help='the web application logs to parse')
parser.add_argument('-c', '--config', metavar='', help='a configuration file')
parser.add_argument('-d', '--debug', metavar='', help='output debug information')
parser.add_argument('-v', '--verbose', metavar='', help='output additional information')

parser.add_argument('-a', '--all', action='store_true', help='run all analyzers')
parser.add_argument('--hourly-peak', action='store_true')
parser.add_argument('--hourly-requests-by-host', action='store_true')
parser.add_argument('--hourly-requests-to-server', action='store_true')
parser.add_argument('--param-count', action='store_true')
parser.add_argument('--param-extra', action='store_true')
parser.add_argument('--param-length', action='store_true')
parser.add_argument('--response-code', action='store_true')
parser.add_argument('--response-size-centroid', action='store_true')
parser.add_argument('--response-size-dbscan', action='store_true')
parser.add_argument('--response-size-elliptic', action='store_true')
parser.add_argument('--response-size-hac', action='store_true')
parser.add_argument('--response-size-kmeans', action='store_true')
parser.add_argument('--response-size-knn', action='store_true')
parser.add_argument('--response-size-local-outlier', action='store_true')
parser.add_argument('--response-size-meanshift', action='store_true')
parser.add_argument('--response-size-singlecomplete', action='store_true')
parser.add_argument('--response-size-wardavg', action='store_true')
parser.add_argument('--response-status', action='store_true')
parser.add_argument('--url-requested', action='store_true')
parser.add_argument('--url-requested-lots', action='store_true')
parser.add_argument('--url-requested-once', action='store_true')
parser.add_argument('--verb', action='store_true')

args = parser.parse_args()

# read log file
logs = logreader.toJson(args.logfile)

# run analysis
if args.all:
	analyzers.hourly_peak.analyze(logs)
	analyzers.hourly_requests_by_host.analyze(logs)
	analyzers.hourly_requests_to_server.analyze(logs)
	analyzers.param_count.analyze(logs)
	analyzers.param_extra.analyze(logs)
	analyzers.param_length.analyze(logs)
	analyzers.response_code.analyze(logs)
	analyzers.response_size_centroidmedian.analyze(logs)
	analyzers.response_size_dbscan.analyze(logs)
	analyzers.response_size_elliptic.analyze(logs)
	analyzers.response_size_dendogramhac.analyze(logs)
	analyzers.response_size_kmeans.analyze(logs)
	analyzers.response_size_knn.analyze(logs)
	analyzers.response_size_lof.analyze(logs)
	analyzers.response_size_meanshift.analyze(logs)
	analyzers.response_size_singlecomplete.analyze(logs)
	analyzers.response_size_wardavg.analyze(logs)
	analyzers.response_status.analyze(logs)
	analyzers.url_requested.analyze(logs)
	analyzers.url_requested_lots.analyze(logs)
	analyzers.url_requested_once.analyze(logs)
	analyzers.verb.analyze(logs)

else:
	if args.hourly_peak:
		analyzers.hourly_peak.analyze(logs)

	if args.hourly_requests_by_host:
		analyzers.hourly_requests_by_host.analyze(logs)

	if args.hourly_requests_to_server:
		analyzers.hourly_requests_to_server.analyze(logs)

	if args.param_count:
		analyzers.param_count.analyze(logs)

	if args.param_extra:
		analyzers.param_extra.analyze(logs)

	if args.param_length:
		analyzers.param_length.analyze(logs)

	if args.response_code:
		analyzers.response_code.analyze(logs)

	if args.response_size_dbscan:
		analyzers.response_size_dbscan.analyze(logs)

	if args.response_size_elliptic:
		#todo: no output
		analyzers.response_size_elliptic.analyze(logs)

	if args.response_size_hac:
		analyzers.response_size_dendogramhac.analyze(logs)

	if args.response_size_kmeans:
		analyzers.response_size_kmeans.analyze(logs)

	if args.response_size_knn:
		analyzers.response_size_knn.analyze(logs)

	if args.response_size_local_outlier:
		analyzers.response_size_lof.analyze(logs)

	if args.response_size_centroid:
		analyzers.response_size_centroidmedian.analyze(logs)

	if args.response_size_meanshift:
		analyzers.response_size_meanshift.analyze(logs)

	if args.response_size_singlecomplete:
		analyzers.response_size_singlecomplete.analyze(logs)

	if args.response_size_wardavg:
		analyzers.response_size_wardavg.analyze(logs)

	if args.response_status:
		analyzers.response_status.analyze(logs)

	if args.url_requested:
		analyzers.url_requested.analyze(logs)

	if args.url_requested_lots:
		analyzers.url_requested_lots.analyze(logs)

	if args.url_requested_once:
		analyzers.url_requested_once.analyze(logs)

	if args.verb:
		analyzers.verb.analyze(logs)