import sys

# -- General idea: improves chances of tests and Sphinx builds working if this is included as a submodule
def add_submodule(path):
    if f"./{path}" not in sys.path:
        sys.path.insert(0,f"../../{path}") # -- Needed for Sphinx builds, usually run in the docs subdirectory
        sys.path.insert(0,f"./{path}")  # -- For normall running. Add second so it will go first in the search order
add_submodule("hdtimelines")

from hdtimelines import pltimeline

def check_dataframe(df, study_range_start=None, study_range_end=None, dateformat="default"):
    "Check if a dataframe will successfully add as a plTimeLine topic"
    pltl = pltimeline.plTimeLine(mindate="2000 BC", maxdate="2200", xmode="years", dateformat=dateformat)
    message = ""
    try:
        added = pltl.add_topic_from_df(df, study_range_start=study_range_start, study_range_end=study_range_end)
        if not added:
            message = "No events found in study range"
    except Exception as e:
        added = False
        message = f"Error: {repr(e)}"
    return added, message
