import argparse
import logreader
from analyzers import response_size_dbscan, response_size_dendogramhac, response_size_lof, hourly_peak, hourly_requests_by_host, hourly_requests_to_server, param_count, param_extra, param_length

parser = argparse.ArgumentParser(description='Get more from your logs.')

parser.add_argument('logfile', help='the web application logs to parse')
parser.add_argument('-c', '--config', metavar='', help='a configuration file')
parser.add_argument('-d', '--debug', metavar='', help='output debug information')
parser.add_argument('-v', '--verbose', metavar='', help='output additional information')

parser.add_argument('-a', '--all', action='store_true', help='run all analyzers')
parser.add_argument('--dbscan', action='store_true')
parser.add_argument('--hac', action='store_true')
parser.add_argument('--local-outlier', action='store_true')
parser.add_argument('--hourly-peak', action='store_true')
parser.add_argument('--hourly-requests-by-host', action='store_true')
parser.add_argument('--hourly-requests-to-server', action='store_true')
parser.add_argument('--param-count', action='store_true')
parser.add_argument('--param-extra', action='store_true')
parser.add_argument('--param-length', action='store_true')
'''
parser.add_argument('--elliptic', action='store_true')
parser.add_argument('--knn', action='store_true')
parser.add_argument('--meanshift', action='store_true')
parser.add_argument('--centroid-median-hac', action='store_true')
parser.add_argument('--single-complete-hac', action='store_true')
parser.add_argument('--ward-avg-hac', action='store_true')
parser.add_argument('--response-size-kmeans', action='store_true')
parser.add_argument('--response-status-kmeans', action='store_true')
parser.add_argument('--response-code', action='store_true')
parser.add_argument('--verb-kproto', action='store_true')
parser.add_argument('--url-kproto', action='store_true')
parser.add_argument('--num-param-ip', action='store_true')
parser.add_argument('--ip-url-param', action='store_true')
parser.add_argument('--url-one-time-hit', action='store_true')
parser.add_argument('--hosts-unique-url-hits', action='store_true')
parser.add_argument('--missing-extra-params', action='store_true')
'''

args = parser.parse_args()

# read log file
logs = logreader.toJson(args.logfile)

# run analysis
if args.all:
	response_size_dbscan.analyze(logs)
	response_size_dendogramhac.analyze(logs)
	response_size_lof.analyze(logs)

elif args.dbscan:
	response_size_dbscan.analyze(logs)

elif args.hac:
	response_size_dendogramhac.analyze(logs)

elif args.local_outlier:
	response_size_lof.analyze(logs)

elif args.hourly_peak:
	hourly_peak.analyze(logs)

elif args.hourly_requests_by_host:
	hourly_requests_by_host.analyze(logs)

elif args.hourly_requests_to_server:
	hourly_requests_to_server.analyze(logs)

elif args.param_count:
	param_count.analyze(logs)

elif args.param_extra:
	param_extra.analyze(logs)

elif args.param_length:
	param_length.analyze(logs)

else:
	print 'run all'

'''
elif args.elliptic:
	response_size_elliptic.analyze(logs)

elif args.knn:
	response_size_knn.analyze(logs)

elif args.meanshift:
	print 'run meanshift'

elif args.centroid_median_hac:
	print 'run centroid-median-hac'

elif args.single_complete_hac:
	print 'run single-complete-hac'

elif args.ward_avg_hac:
	print 'run ward-avg-hac'

elif args.response_size_kmeans:
	print 'run response-size-kmeans'

elif args.response_status_kmeans:
	print 'run response-status-kmeans'

elif args.response_code:
	print 'run response-code'

elif args.verb_kproto:
	print 'run verb-kproto'

elif args.url_kproto:
	print 'run url-kproto'

elif args.num_param_ip:
	print 'run num-param-ip'

elif args.ip_url_param:
	print 'run ip-url-params'

elif args.url_one_time_hit:
	print 'run url-one-time-hit'

elif args.hosts_unique_url_hits:
	print 'run hosts-unique-url-hits'

elif args.missing_extra_params:
	print 'run missing-extra-params'

else:
	print 'run all'
'''
