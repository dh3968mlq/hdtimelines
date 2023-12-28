# hdtimelines

A Python package for creating graphical timelines of historical data using [Plotly](https://plotly.com/python/)

Github: https://github.com/dh3968mlq/hdtimelines

Example outputs: https://historicaldate.com/

Some starter datasets (.csv): https://github.com/dh3968mlq/historicaldate-data

![Example timeline image](https://historicaldate.com/wp-content/uploads/2023/05/basic_timeline_example.png)

Uses the [historicaldate](https://historicaldate.readthedocs.io/en/stable/) package for dates:
   * Dates in input files are in a natural readable format, such as '25 Dec 1066'
   * Dates can be uncertain (e.g. 'circa 1028') and can be BC (e.g. '525 BC')
   * It is possible to specify start and end dates of persistent events, such as a wars or monarchs' reigns, and/or birth and death dates of persons

In the timeline display:

![Timeline explanation image](https://historicaldate.com/wp-content/uploads/timeline_explanation1.png)

## To create a timeline:
   * Install this package: *pip install hdtimelines*
   * Download sample data from https://github.com/dh3968mlq/historicaldate-data, and/or
   * Create .csv files of data (see below for column names and date formats)
   * Create and run a Python program, similar to below, or see sample timeline code in the *timelines* folder in this repository

### Sample code:

```python
# Sample code for a timeline of British monarchs and Prime Ministers
# The folder that historicaldate-data has been downloaded to...
dataroot = "/svol1/pishare/users/pi/repos/timelines2/historicaldate-data" 

from hdtimelines import pltimeline
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
```

## Input file format

Dataframes passed to *add_topic_from_df* have one row per event or life, and specific column names. *label* must be present, together with either *hdate* or both of *hdate_birth* and *hdate_death*. All other columns are optional.

| Column | Usage |
| ------ | ----- |
| label   | Event label, appears on the timeline  |
| description | Extended description, used for hovertext |
| hdate | Date of event, or start date if it is a persistent event |
| hdate_end | End date of a persistent event |
| hdate_birth | A person's birth date |
| hdate_death | A person's date of death, defaults to *alive* if *hdate_birth* is present|
| htext_end | Hover text linked to the marker drawn at *hdate_end* |
| color (or colour) | Colour to draw the event or life
| url | hyperlink, active by clicking on the displayed label |
| rank | An integer, use together with *max_rank* to control which rows are displayed

## Date formats

Date formats are described in detail at https://historicaldate.readthedocs.io/en/stable/

In brief:
* Two core formats are supported by default:
    * 25 Dec 1066 (and variants)
    * 1066-12-25
* Additional non-default formats available:
    * 25/12/1066
    * 12/25/1066
    * Dec 25 1066
* Imprecise dates, such as '1066' or 'circa 1066' are allowed
* BC dates are supported such as '385 BC'
* Ongoing events and lives are supported by setting *hdate_end* or *hdate_death* to 'ongoing'. A blank value of *hdate_death* isinterprested as meaning a person is still alive.

## Changes

### New in 0.0.7

Split from historicaldate package (https://github.com/dh3968mlq/historicaldate)

### New in 0.0.6

*add_event_set* renamed to *add_topic_from_df*

### New in 0.0.5

   * BC dates can now be displayed on timelines (*xmode=years*)
   * X-axis (date axis) labels moved to top 

### New in 0.0.4

*add_event_set()* now updates yaxes to fit the displayed data

New method *plTimeLine().fit_xaxis(self, mindate=None, maxdate=None)* that fits the X axis either to the data or to a specified range of dates

X axis date labels moved to top of display

Study range filtering added, parameters *study_range_start* and *study_range_end* of the *add_event_set* method. Event sets lying entirely outside the study range are not displayed.

Filtering on the value of a *rank* column in input data, parameter *max_rank* of the *add_event_set* method. 

### New in 0.0.3

   * New English Football timeline code (*english_football.py*)
   * New *hover_datetype* parameter to *add_event_set*
   * New *htext_end* column supported
   