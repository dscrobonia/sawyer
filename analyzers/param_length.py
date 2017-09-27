import json
import logging
import re
import urlparse

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    host_url_param_count = dict()

    hostlist = dict()
    log.info(
        "##******** Analysis #10: Printing input and info of parameters requested by host for a url. Key of type- host: url and value is parameter count *******######:")

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

        log.info("**** Printing information for " + key_for_par_count + " *****")
        for x, y in params:
            log.info("Parameter = " + str(x) + " Value = " + str(y))
            len(y)  ###########length of value of parameter
            if len(y) > 50:
                log.info("ALERT!!!!! \nHuge length (" + str(len(y)) + ") of request parameter :" + str(
                    x) + " with value \n" + y + "\n by host:url combination " + key_for_par_count)

            count = count + 1
            countnonoverlappingrematches('=&', url)  ## missing arguments

            if countnonoverlappingrematches('=&', url) > 3:
                log.info("More than 3 missing parameters in the request! found by =& logic")

            param_duplicates = dict()
            if x in param_duplicates:
                param_duplicates[x] += 1
                log.info(
                    "Duplicate parameter " + x + " by " + key_for_par_count + " in same request found!! Weird behaviour!!")  ###spots duplicates
            else:
                param_duplicates[x] = 1

        # count is count of the parameters

        if key_for_par_count in host_url_param_count:
            host_url_param_count[key_for_par_count].append(count)
        else:
            host_url_param_count[key_for_par_count] = [count]

    ###Analysis 10: List of number of parameters requested for (host+url) key:
    log.info(
        "##******** Analysis #10: Printing count of parameters requested by host for a url. Key of type- host: url and value is parameter count *******######:")
    log.info(
        "##******** Analysis #10: Printing count of parameters requested by host for a url. Key of type- host: url and value is parameter count *******######:")

    for x in host_url_param_count:
        for y in host_url_param_count[x]:
            if int(y) > 3:
                log.info(
                    "Huge count of parameters requested: " + str(x) + "requests : " + str(y) + " parameters")

            else:
                log.info(
                    "Huge count of parameters requested: " + str(x) + "requests : " + str(y) + " parameters")


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]
