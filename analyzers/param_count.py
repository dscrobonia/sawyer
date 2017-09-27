import json
import logging
import re

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    req_parameters = dict()

    hostlist = dict()
    req_para_key = []

    # Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]

        hostlist[y['HOST']] = 1

        if y['HOST'] in hostlist:

            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])

            reque = y['REQUEST']
            req = reque.split()
            lst = req[1].split("&")

            if par_key in req_parameters:
                req_parameters[par_key].append(len(lst))
            else:
                req_parameters[par_key] = [len(lst)]
                req_para_key.append(par_key)

        else:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])

            reque = y['REQUEST']
            req = reque.split()
            lst = req[1].split("&")

            if par_key in req_parameters:
                req_parameters[par_key].append(len(lst))
            else:
                req_parameters[par_key] = [len(lst)]
                req_para_key.append(par_key)

    ###Analysis 9: List of number of parameters requested by a Host-IP on a given day for urls it requests
    ##Every entry in the list corresponds to number of parameters requested for 1 url

    log.info(
        "Analysis #9:\n####****** Printing List of number of parameters requested by a Host-IP on a given day for urls.  *****#####"
    )
    log.info(
        "Analysis #9:\n####****** Printing List of number of parameters requested by a Host-IP on a given day for urls *****####"
    )
    log.info(
        "Every entry in the list corresponds to number of parameters requested for 1 url, if the count exceeds 5. \nCheck INFO.log for entries with less number of parameter requests"
    )
    for x in req_para_key:
        for y in req_parameters[x]:
            if y > 5:
                log.info(x + ": " + str(y))
            else:
                log.info(x + ": " + str(y))

    log.info("Check INFO.log for more details!")


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]
