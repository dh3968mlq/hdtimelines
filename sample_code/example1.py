# Sample code for a timeline of British monarchs and Prime Ministers
# The folder that historicaldate-data has been downloaded to...
dataroot = "/svol1/pishare/users/pi/repos/timelines2/historicaldate-data" 

import sys
sys.path.insert(0,".")

from hdtimelines import pltimeline
import pandas as pd

df1 = pd.read_csv(f"{dataroot}/data/History/europe/British Monarchs.csv",
                 na_filter=False)
df2 = pd.read_csv(f"{dataroot}/data/History/europe/British Prime Ministers.csv",
                 na_filter=False)

pltl = pltimeline.plTimeLine()
pltl.add_topic_from_df(df1, title="British Monarchs from 1066")
pltl.add_topic_from_df(df2, title="British Prime Ministers") 
pltl.show() # Show in a browser, or...
pltl.write_html("/home/pi/example_timeline.html")