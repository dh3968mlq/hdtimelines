
# The path this repo (https://github.com/dh3968mlq/historicaldate) has been downloaded to
hdroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate"
# The path the data repo (https://github.com/dh3968mlq/historicaldate-data) has been downloaded to
dataroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate-data"

import sys
sys.path.append(hdroot)
from hdtimelines import pltimeline
import pandas as pd
import datetime

df_charlotte = pd.read_csv(f"{dataroot}/data/culture/western_canon/brontes/Charlotte Bronte.csv",
                 na_filter=False)
df_emily = pd.read_csv(f"{dataroot}/data/culture/western_canon/brontes/Emily Bronte.csv",
                 na_filter=False)
df_anne = pd.read_csv(f"{dataroot}/data/culture/western_canon/brontes/Anne Bronte.csv",
                 na_filter=False)
df_other = pd.read_csv(f"{dataroot}/data/culture/western_canon/brontes/Other Brontes.csv",
                 na_filter=False)
df_history = pd.read_csv(f"{dataroot}/data/history/europe/Events in British History.csv",
                 na_filter=False)


pltl = pltimeline.plTimeLine(mindate=datetime.date(1800,1,1), maxdate=datetime.date(1870,1,1),
                       title="The Brontës")
pltl.add_topic_from_df(df_charlotte, title="Charlotte Brontë", showbirthanddeath=True)
pltl.add_topic_from_df(df_emily,title="Emily Brontë")
pltl.add_topic_from_df(df_anne, title="Anne Brontë") 
pltl.add_topic_from_df(df_other, title="Brontë Family") 
pltl.add_topic_from_df(df_history,title="Events in British History")
pltl.show() 

pltl.write_html("historicaldate/html/tl_brontes.html")
