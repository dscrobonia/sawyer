import json
import logging
import urlparse

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    per_host_req_url = dict()
    hostlist = dict()

    # Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]

        hostlist[y['HOST']] = 1

        requee = y['REQUEST']
        requ = requee.split()
        url = requ[1]
        parsed = urlparse.urlparse(url)
        params = urlparse.parse_qsl(parsed.query)
        count = 0
        r = url.split('?')
        r[0]  ####this is the url before query parameters

        log.debug(y['HOST'] + ": " + r[0])

        if r[0] in per_host_req_url:
            per_host_req_url[r[0]].append(y['HOST'])
        else:
            per_host_req_url[r[0]] = [y['HOST']]

    ###Analysis #12: List of number of unique urls hit by client ips
    log.info(
        "##******** Analysis #12:#####  Printing number of unique urls hit by client ips:   ###############"
    )

    host_unique_url_count = dict()

    for x in per_host_req_url:
        if len(per_host_req_url[x]) == 1:
            for y in per_host_req_url[x]:
                if y in host_unique_url_count:
                    host_unique_url_count[y] += 1
                else:
                    host_unique_url_count[y] = 1

                log.info(x + " is hit only by user: " + y)

    log.info(
        "##******** Analysis #12:#####  Printing number of unique urls hit by client ips:   ###############"
    )

    for x in host_unique_url_count:
        log.info(x + ":    " + str(host_unique_url_count[x]))
        if host_unique_url_count[x] > 30:
            log.info("The host " + x + " has hit many unique urls!! " + str(
                host_unique_url_count[x]) + " such hits!! That's huge!")
