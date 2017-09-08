INSTALLATION:
1. Install Scikit learn 0.19.0 with:(Mac OS X)
    pip install -U scikit-learn
2. Scikit learn requires: 
Python (>= 2.7 or >= 3.3),
NumPy (>= 1.8.2),
SciPy (>= 0.13.3).   
Step 1 installs these dependencies automatically.
3. Install kmodes for python:
(A) kmodes can be installed using pip:

pip install kmodes
(B) To upgrade to the latest version:

pip install --upgrade kmodes
(C) Alternatively, you can build the latest development version from source:

git clone https://github.com/nicodv/kmodes.git
cd kmodes
python setup.py install
kmodes would already be up to date, hence an update for it may not be required. 


4. Run:  pip install --upgrade scikit-learn
This will upgrade scikit learn

5. Install matplotlib:
pip install matplotlib

6. Install python-tk:
apt-get install python-tk


7. Besides these, we import json, urlparse, re, argparse, sys, os, etc. These are installed by default. If not, a pip install would install it.




TESTING:
1. Create a directory and cd into it: (I'm calling it test-attack).
    mkdir test-attack
    cd test-attack
    
1. For running the analysis, clone or download the repository 'Analysis'.
Uncompress this folder and cd into it.
cd Analysis
This folder has an input file called 'partial-july-log.txt'.
2. Call the argparser.py script this way:
python argparser.py --inputfile partial-log-july.txt --analyser hac

Check the INFO.log, ATTACK.log and DEBUG.log files that get created in the repo for more info. PNG files with plots also get created in the directory for more than half the analysers.

This example runs the elliptic analyser for IP address-response size tuple.

Besides these, a number of other analysers are available :

List of available analysers is:

1. dbscan 

2. hac 

3. local-outlier 

4. elliptic 

5. knn

6. meanshift

7. centroid-median-hac

8. single-complete-hac

9. ward-avg-hac

10. response_size-kmeans

11. response_status-kmeans

12. response_code

13. peak_hour

14. verb-kproto

15. url-kproto

16. hourly-req-host

17. hourly-requests

18. num_param_ip

19. ip_url_param

20. url_one_time_hit

21. hosts_unique_url_hits

22. missing_extra_params

23. default
