import json
import logging

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    hostlist = dict()
    req_per_hr_key_list = [
    ]  # keeps track of keys of the type ip+hour+date+month
    per_hr_req = dict()  # IP-req-per-hour

    # Data pre-processing here:
    for y in json_to_python:

        hostlist[y['HOST']] = 1

        if y['HOST'] in hostlist:

            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(
                date[0]) + str(date[1])
            if comp_key in per_hr_req:
                per_hr_req[comp_key] += 1
            else:
                per_hr_req[comp_key] = 1
                req_per_hr_key_list.append(comp_key)

        else:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(
                date[0]) + str(date[1])

            per_hr_req[comp_key] = 1
            req_per_hr_key_list.append(comp_key)

    ###########################****NON-ML Analysis here******################
    ###Analysis 7: Per-hour requests for a host at a particular hour and day: key of type: host+hr+date
    log.info(
        "Analysis #7: ####****** Printing per hour request stats for a given combination of : HOST/HOUR/DATE: ******###########"
    )
    log.info(
        "** Detects only in case th host makes more than 250 requests in 1 hour. For more detailed info, see INFO.log"
    )

    log.info(
        "Analysis #7: ####****** Printing per hour request stats for a given combination of : HOST/HOUR/DATE: ******###########"
    )

    for x in req_per_hr_key_list:
        if per_hr_req[x] > 250:
            log.info(x + ": " + str(per_hr_req[x]))
        else:
            log.info(x + ": " + str(per_hr_req[x]))
