# Sample code for a timeline of British monarchs and Prime Ministers
# The folders that historicaldate and historicaldate-data have been downloaded to...
hdroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate" 
dataroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate-data" 
import sys
sys.path.append(hdroot)
from hdtimelines import pltimeline  # Timelines using Plotly
import pandas as pd

df1 = pd.read_csv(f"{dataroot}/data/history/europe/British Monarchs.csv",
                 na_filter=False)
df2 = pd.read_csv(f"{dataroot}/data/history/europe/British Prime Ministers.csv",
                 na_filter=False)

pltl = pltimeline.plTimeLine()
pltl.add_topic_from_df(df1, title="British Monarchs from 1066")
pltl.add_topic_from_df(df2, title="British Prime Ministers") 
pltl.show() # Show in a browser, or...
pltl.write_html("/home/pi/example_timeline.html")