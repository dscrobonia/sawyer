import json
import logging
import urlparse

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    rep_host_url_paramnamecnt = dict()
    url_req = []
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

        key_for_par_count = y['HOST'] + " : " + r[0]
        # key_for_par_count = y['TIME'] + y['HOST'] + " : " + r[0]

        for x, y in params:

            ##Important functionality
            if key_for_par_count in rep_host_url_paramnamecnt:
                random = rep_host_url_paramnamecnt[key_for_par_count]
                if x in random:
                    random[x] += 1
                else:
                    random[x] = 1
                rep_host_url_paramnamecnt[key_for_par_count] = random

            else:
                random = dict()
                random[x] = 1
                rep_host_url_paramnamecnt[key_for_par_count] = random

    log.info(
        "##Analysis #13:#######**** Printing count and name of parameters for host+url combination: Find missing and extra params with this: ***######## "
    )
    log.info(
        "Analysis #13:#######**** Printing missing/extra parameters *******#########"
    )

    for y in rep_host_url_paramnamecnt:
        log.info(y + "--")
        tem = rep_host_url_paramnamecnt[y]
        verify = 1
        flag = 0
        for random in rep_host_url_paramnamecnt[y]:
            flag += 1
            log.info(random + ": " + str(tem[random]))
            if flag == 1:
                verify = tem[random]
            if flag > 1:
                if verify > tem[random]:
                    log.info("Missing parameter: " + random + " for key : " +
                             y)
                if verify < tem[random]:
                    log.info("Extra parameter: " + random + " for key : " + y)
