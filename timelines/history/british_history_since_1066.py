# The path the data repo (https://github.com/dh3968mlq/historicaldate-data) has been downloaded to
dataroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate-data"

import sys
sys.path.insert(0,'.')

from hdtimelines import pltimeline
import pandas as pd

df1 = pd.read_csv(f"{dataroot}/data/History/Europe/British Monarchs.csv",
                 na_filter=False)
df2 = pd.read_csv(f"{dataroot}/data/History/Europe/Events in British History.csv",
                 na_filter=False)
df3 = pd.read_csv(f"{dataroot}/data/History/Europe/British Prime Ministers.csv",
                 na_filter=False)

xmode = 'date'
xmode = 'years'
pltl = pltimeline.plTimeLine(xmode=xmode)
pltl.add_topic_from_df(df1, title="British Monarchs from 1066", showbirthanddeath=True)
pltl.add_topic_from_df(df2,title="Events in British History")
pltl.add_topic_from_df(df3, title="British Prime Ministers") 
pltl.show() 

pltl.write_html("html/tl_ukhistory.html")
