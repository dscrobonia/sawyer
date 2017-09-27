import json
import logging
import urlparse

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    log.info(
        "##******** Analysis #11:###Printing INPUT for url and hosts with only one host requesting this url #####")

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

        log.info(str(y['HOST']) + ": " + r[0])
        if r[0] in per_host_req_url:
            per_host_req_url[r[0]].append(y['HOST'])
        else:
            per_host_req_url[r[0]] = [y['HOST']]

    ###Analysis 11: List of urls with only one host requesting it

    log.info("##******** Analysis #11:###Printing url and hosts with only one host requesting this url #####")

    host_unique_url_count = dict()

    for x in per_host_req_url:
        if len(per_host_req_url[x]) == 1:
            for y in per_host_req_url[x]:
                if y in host_unique_url_count:
                    host_unique_url_count[y] += 1
                else:
                    host_unique_url_count[y] = 1

                log.info("URL :    " + x + "\nis hit only by IP: " + y)
