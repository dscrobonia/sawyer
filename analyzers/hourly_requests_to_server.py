import json
import logging
import re

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    net_req_hr = dict()

    hostlist = dict()

    net_req_hr_key = []  # keeps track of keys of type hr+date+month. for finding requests received per hour

    # Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]

        hostlist[y['HOST']] = 1

        if y['HOST'] in hostlist:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
            if net_key in net_req_hr_key:
                net_req_hr[net_key] += 1
            else:
                net_req_hr[net_key] = 1
                net_req_hr_key.append(net_key)


        else:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
            if net_key in net_req_hr_key:
                net_req_hr[net_key] += 1
            else:
                net_req_hr[net_key] = 1
                net_req_hr_key.append(net_key)

    ###Analysis 8: Per-hour requests for a particular hour and day: key of type: hr+date

    log.info(
        "Analysis #8: \n####****** Printing net requests per hour stats at the Server with Key: Hour/DATE Value: Number of requests ******###########")
    log.info(
        "** Note that this shows data if number of requests exceed 500. For detailed info, check INFO.log")
    for x in net_req_hr_key:
        if net_req_hr[x] > 500:
            log.info(x + " received :" + str(net_req_hr[x]) + " requests!!")
            if net_req_hr[x] > 750:
                log.info("ALERT! Abnormal behaviour!")
        else:
            log.info(x + " received :" + str(net_req_hr[x]) + " requests!!")


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]
