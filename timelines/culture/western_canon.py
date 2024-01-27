# The path the data repo (https://github.com/dh3968mlq/historicaldate-data) has been downloaded to
dataroot = "/svol1/pishare/users/pi/repos/timelines/historicaldate-data"

import sys
sys.path.insert(0,'.')

from hdtimelines import pltimeline
import pandas as pd

df_monarchs = pd.read_csv(f"{dataroot}/data/History/europe/British Monarchs.csv",
                 na_filter=False)
df_playwrights = pd.read_csv(f"{dataroot}/data/Culture/western_canon/Playwrights.csv",
                 na_filter=False)
df_authors = pd.read_csv(f"{dataroot}/data/Culture/western_canon/Authors.csv",
                 na_filter=False)
df_composers = pd.read_csv(f"{dataroot}/data/Culture/western_canon/Classical Composers.csv",
                 na_filter=False)

pltl = pltimeline.plTimeLine(#mindate=datetime.date(1,1,1), maxdate=datetime.date(500,1,1),
                       title="Culture: Western Canon", xmode="years")
pltl.add_topic_from_df(df_monarchs, title="British Monarchs", showbirthanddeath=True)
pltl.add_topic_from_df(df_playwrights, title="Playwrights", showbirthanddeath=True)
pltl.add_topic_from_df(df_authors, title="Authors", showbirthanddeath=True)
pltl.add_topic_from_df(df_composers, title="Classical Composers", showbirthanddeath=True)
pltl.show() 

pltl.write_html("html/tl_western_canon.html")
