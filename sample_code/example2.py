# Sample code for a timeline of British monarchs and Prime Ministers
# ...using the hdTimeLine() class
# The folder that historicaldate-data has been downloaded to...
dataroot = "/svol1/pishare/users/pi/repos/timelines2/historicaldate-data" 

import sys
sys.path.insert(0,".")

from hdtimelines import pltimeline, hdtimeline
import pandas as pd

hdtl = hdtimeline.hdTimeLine() 
hdtl.add_topic_csv("British Monarchs",
                   f"{dataroot}/data/history/europe/British Monarchs.csv")
hdtl.add_topic_csv("British Prime Ministers",
                   f"{dataroot}/data/history/europe/British Prime Ministers.csv")

pltl = pltimeline.plTimeLine.from_hdtimeline(hdtl)
pltl.show() 
