Different types of analysis are available for processing web-server logs. Please find the sample results on running the analysis
on a web server logs with these analysers. The log file used is partial-log-july.txt

1. python argparser.py --inputfile partial-log-july.txt --analyser hac
This creates png files for hierarchical clustering using different types of linkages: single, complete, centroid, median, ward.
The files of dendograms of the clustered results. The names of the png files created are available in ATTACK.log.
The features consist of client IP address and the response size received

2. python argparser.py --inputfile partial-log-july.txt --analyser response_status-kmeans
This does k-means clustering using k-prototypes for clustering categorical data (response status code) with k-modes and IP
addresses with k-means. The file ATTACK.info has information regarding the clusters with the highest and least number of elements:
Sample result:
Cluster no. 2 has the least elements: 175
Check INFO.log to view its contents!
Cluster no. 1 has the maximum elements: 382
Check INFO.log to view its contents!
Check DEBUG.log to view contents of all clusters along with the main input X!

INFO.log has information regarding the cluster contents of the clusters with minimum and maximum number of elements.

3. python argparser.py --inputfile partial-log-july.txt --analyser verb-kproto
This does k-means clustering using k-prototypes for clustering categorical data (http verb code) with k-modes and IP
addresses with k-means. The file ATTACK.info has information regarding the clusters with the highest and least number of elements:
Sample result:
luster no. 0 has the least elements: 39
Check INFO.log to view its contents!
Cluster no. 4 has the maximum elements: 410
Check INFO.log to view its contents!
Check DEBUG.log to view contents of all clusters along with the main input X


INFO.log has information regarding the cluster contents of the clusters with minimum and maximum number of elements.


4. python argparser.py --inputfile partial-log-july.txt --analyser url-kproto
This does k-means clustering using k-prototypes for clustering categorical data (URL requested) with k-modes and IP
addresses with k-means. The file ATTACK.info has information regarding the clusters with the highest and least number of elements:
Sample result:
******   Analysis #6: IP-URL Input data to k-prototypes:     ********
Cluster no. 2 has the least elements: 147
Check INFO.log to view its contents!
Cluster no. 3 has the maximum elements: 381
Check INFO.log to view its contents!
Check DEBUG.log to view contents of all clusters along with the main input X!

INFO.log has information regarding the cluster contents of the clusters with minimum and maximum number of elements.

5. python argparser.py --inputfile partial-log-july.txt --analyser response_code
Calculates the ratios of the failed attempts to successful attempts. If the ratio suggests only failed attempts or high number of 
failed attempts in comparison to successful ones, the get logged to ATTACK.info.

Sample results:
May be an attack by 5.226.137.101 as it has 54 failed attempts.
May be an attack by 192.151.148.122 as it has 234 failed attempts but only 2 successful attempts!
May be an attack by 108.185.92.137 as it has 103 failed attempts but only 1 successful attempts!

INFO.log has detailed information regarding the numberof failed/successful attempts for every client IP.


6. python argparser.py --inputfile partial-log-july.txt --analyser peak_hour
This analyser clusters the IP-address and peak usage hour for the client IP and performs K-means clustering on it. We use 
Scikit Learn since it is purely numeric data.

The file ATTACK.info has information regarding the clusters with the highest and least number of elements:
Sample result:
Cluster no. 18 has the least elements: 6
Check INFO.log to view its contents!
Cluster no. 17 has the maximum elements: 97
Check INFO.log to view its contents!
Check DEBUG.log to view contents of all clusters along with the main input X!

INFO.log has information regarding the cluster contents of the clusters with minimum and maximum number of elements.


7. python argparser.py --inputfile partial-log-july.txt --analyser response_size-kmeans
This analyser clusters the IP-address and average resonse size received by the client IP and performs K-means clustering on it. We use 
Scikit Learn since it is purely numeric data.

The file ATTACK.info has information regarding the clusters with the highest and least number of elements:
Sample result:
********    Printing Analysis #4: IP-Address and Response Size received: KMeans   ********
Cluster no. 22 has the least elements: 13
Check INFO.log to view its contents!
Cluster no. 13 has the maximum elements: 98
Check INFO.log to view its contents!
Check DEBUG.log to view contents of all clusters along with the main input X!

INFO.log has information regarding the cluster contents of the clusters with minimum and maximum number of elements.

8. python argparser.py --inputfile partial-log-july.txt --analyser hourly-req-host

Analysis #7: ####****** Prints per hour request stats for a given combination of : HOST/HOUR/DATE: ******###########
** Detects only in case the host makes more than 250 requests in 1 hour. For more detailed info, see INFO.log
Sample result:
162.209.168.83/20/01Jul: 295

9. python argparser.py --inputfile partial-log-july.txt --analyser hourly-requests
This prints the number of requests received by the server for an hour on a particular day.
####****** Printing net requests per hour stats at the Server with Key: Hour/DATE Value: Number of requests ******###########
** Note that this shows data in ATTACK if number of requests exceed 500. Displays an alert if the 
number exceeds 750. For detailed info, check INFO.log

Sample result:
08/03Jul received :637 requests!!
04/03Jul received :858 requests!!
ALERT! Abnormal behaviour!
04/02Jul received :702 requests!!
09/03Jul received :722 requests!!
14/03Jul received :617 requests!!
01/03Jul received :606 requests!!
06/03Jul received :716 requests!!
10/03Jul received :543 requests!!
00/03Jul received :802 requests!!
ALERT! Abnormal behaviour!
05/03Jul received :650 requests!!

10. python argparser.py --inputfile partial-log-july.txt --analyser num_param_ip
####****** Printing List of number of parameters requested by a Host-IP on a given day for urls.  *****#####
Every entry in the list corresponds to number of parameters requested for 1 url, if the count exceeds 5. 
Check INFO.log for entries with less number of parameter requests
ATTACK.log:
192.151.148.122/03Jul: 11
192.151.148.122/03Jul: 11
192.151.148.122/03Jul: 11
192.151.148.122/03Jul: 11
192.151.148.122/03Jul: 11


11. python argparser.py --inputfile partial-log-july.txt --analyser ip_url_param
This logs info regarding the length of parameters requested by a given IP. Helpful in detecting SQL injections.
If the length of parameter is higher than 50, it may be indicative of an attack, logged to ATTACK.info
##******** Analysis #10: Prints input and info of parameters requested by host for a url. Key of type- host: url and value is parameter count *******######:
ALERT!!!!! 
Huge length (62) of request parameter :ver with value 
4.6.4') UNION ALL SELECT 'qkkxq'||'Efbgpysnfd'||'qzzbq'-- LuCX
 by host:url combination 91.247.38.57 : /wp-content/plugins/sociable/css/sociable.css
 
ALERT!!!!! 
Huge length (81) of request parameter :ver with value 
4.6.4') UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- yvnT
 by host:url combination 91.247.38.57 : /wp-content/plugins/sociable/css/sociable.css
 
ALERT!!!!! 
Huge length (92) of request parameter :ver with value 
4.6.4') UNION ALL SELECT 'qkkxq'||'wGpHXpYFSEfnbBPKJSfzTNCLzbKYkDBkINhygtCf'||'qzzbq'-- VpMR

ALERT!!!!! 
Huge length (256) of request parameter :ver with value 
4.6.4') AND 1134=(SELECT UPPER(XMLType(CHR(60)||CHR(58)||CHR(113)||CHR(107)||CHR(107)||CHR(120)||CHR(113)||(SELECT (CASE WHEN (1134=1134) THEN 1 ELSE 0 END) FROM DUAL)||CHR(113)||CHR(122)||CHR(122)||CHR(98)||CHR(113)||CHR(62))) FROM DUAL) AND ('XuIb'='XuIb
 by host:url combination 91.247.38.57 : /wp-content/plugins/sociable/css/sociable.css


12. python argparser.py --inputfile partial-log-july.txt --analyser url_one_time_hit

##******** This analyser prints url and hosts with only one host requesting this url to ATTACK.log #####
URL :    /2012/07/25/year-of-security-for-java-week-30-authentication/comment-page-1/
is hit only by IP: 207.46.13.181
URL :    /pma2018/
is hit only by IP: 108.185.92.137
URL :    //libraries/joomla/web.php
is hit only by IP: 162.209.168.83
URL :    //images/w0rm.php
is hit only by IP: 162.209.168.83
URL :    /admin/pMA/
is hit only by IP: 108.185.92.137
URL :    /wordpress/
is hit only by IP: 35.187.198.105
URL :    /images/stories/a.php
is hit only by IP: 192.151.148.122
URL :    /php-myadmin/
is hit only by IP: 108.185.92.137
URL :    /tag/cross-site-request-forgery/feed/
is hit only by IP: 66.249.64.64
URL :    /wp-content/plugins/sociable/images/sprites/option2_64.png
is hit only by IP: 168.235.197.82


13. python argparser.py --inputfile partial-log-july.txt --analyser hosts_unique_url_hits

Logs to ATTACK.log if a particular IP hits more than 50 unique URLS. Logged to ATTACK.info. This may
indicate an attack. For eg. 108.185.92.137 has hit 104 unique urls, which is a huge number.
##******** Analysis #12:#####  Printing number of unique urls hit by client ips:   ###############
The host 216.244.66.246 has hit many unique urls!! 53 such hits!! That's huge!
The host 162.209.168.83 has hit many unique urls!! 81 such hits!! That's huge!
The host 168.235.197.82 has hit many unique urls!! 78 such hits!! That's huge!
The host 216.244.66.194 has hit many unique urls!! 41 such hits!! That's huge!
The host 108.185.92.137 has hit many unique urls!! 104 such hits!! That's huge!

14. python argparser.py --inputfile partial-log-july.txt --analyser missing_extra_params
Tries finding out missing and extra parameters. Suppose a client hits the url always requesting for parameters a, b
and c. Suppose in a few requests, it requests for a, b, c, d, 'd' becomes an extra parameter. If it only requests
a and b, 'c' becomes the mssing parameter. 

Sample result:
Analysis #13:#######**** Printing missing/extra parameters *******#########
Missing parameter: format for key : 180.76.15.157 : /wp-json/oembed/1.0/embed
Missing parameter: ver for key : 69.195.120.227 : /wp-cron.php
Extra parameter: z4 for key : 162.209.168.83 : //images/stories/0day.php
Extra parameter: z3 for key : 162.209.168.83 : //images/stories/0day.php
Extra parameter: z4 for key : 192.151.148.122 : /images/stories/0day.php
Extra parameter: z3 for key : 192.151.148.122 : /images/stories/0day.php

15. python argparser.py --inputfile partial-log-july.txt --analyser centroid-median-hac
*******  IP-Address and Response Size received: Centroid and Median Linkage Hierarchical Clustering  ********
'test-centroid-median.png': Graphically displays the results in this png file .Shoes the knee-point as well.

16. python argparser.py --inputfile partial-log-july.txt --analyser single-complete-hac
*******  IP-Address and Response Size received: Single and Complete Hierarchical Clustering  ********
'test-single-complete.png': Graphically displays the results in this png file .Shoes the knee-point as well.


17. python argparser.py --inputfile partial-log-july.txt --analyser ward-avg-hac
*******  IP-Address and Response Size received: Ward and Average Hierarchical Clustering  ********
'test-ward-average.png': Graphically displays the results in this png file .Shoes the knee-point as well.

18. python argparser.py --inputfile partial-log-july.txt --analyser meanshift
Sample result:
*******    Printing Analysis #4: IP-Address and Response Size received: MEAN SHIFT algorithm   ********
Please check the graph at test-mean-shift.png for more info!
number of estimated clusters : 3

19. python argparser.py --inputfile partial-log-july.txt --analyser knn
Sample result:
********    Printing Analysis #4 (2): IP-Address and Response Size received:  K-Nearest Neighbours ********
Printing KDE:
[-5.63111654 -5.63111654 -5.63111654 ..., -5.63111654 -5.63111654
 -5.63111654]

20. python argparser.py --inputfile partial-log-july.txt --analyser local-outlier
Sample result:
********   Analysis #4 (3) :  IP-Address and Response Size received: LocalOutlierFactor  ********
******** Please check the image test-save-outlier-LOF.png saved in your working directory for more info. ********

21. python argparser.py --inputfile partial-log-july.txt --analyser 
Check test-dbscan.png for results. 
INFO.log has this information:
Estimated number of clusters: 2
Homogeneity: 0.045
Completeness: 1.000
V-measure: 0.087
Adjusted Rand Index: 0.000
Adjusted Mutual Information: 0.000
Silhouette Coefficient: 0.240

22. python argparser.py --inputfile partial-log-july.txt --analyser elliptic
Check elliptic.png. (This algorithm works on 2 D numeric array data. However, it isn't worknig on our data)

23. python argparser.py --inputfile partial-log-july.txt --analyser default
Runs the default host_unique_url_hits analyser. Change the default from argparser.py if required.
