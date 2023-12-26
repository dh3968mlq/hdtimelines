"""
Utilities for figure manipulation in Plotly
"""
import sys
import datetime
import plotly.graph_objects as go
from math import ceil

# -- General idea: improves chances of tests and Sphinx builds working if this is included as a submodule
def add_submodule(path):
    if f"./{path}" not in sys.path:
        sys.path.insert(0,f"../../{path}") # -- Needed for Sphinx builds, usually run in the docs subdirectory
        sys.path.insert(0,f"./{path}")  # -- For normall running. Add second so it will go first in the search order
add_submodule("historicaldate")

from historicaldate import hdateutils

# ------------------------------------------------------------------------------------------------    
# -- Now for functions that create the figure
# ------------------------------------------------------------------------------------------------    
def _add_trace_marker(fig, pdate=None, label="", y=0.0, 
                   color=None, size=8, symbol='diamond', showlegend=False,
                   hovertext=None, hyperlink=None, xmode="date"):
    """
    Add a single marker to a plot
    """
    pltdate = hdateutils.to_python_date(pdate) if xmode == "date" else hdateutils.to_years(pdate)
    fig.add_trace(go.Scatter(x = [pltdate], y=[y], name=label, legendgroup=label,
                        mode="markers", marker={'color':color, 'size':size,'symbol':symbol}, 
                        hoverinfo='text',
                        hovertext=hovertext if hovertext else label,
                        hoverlabel={'namelength':-1}, showlegend=showlegend))
# ------------------------------------------------------------------------------------------------
def _add_trace_label(fig, pdate=None, label="", y=0.0, hyperlink=None, xmode="date"):
    "Add a label to a plot"
    hlinkedtext = f'<a href="{hyperlink}">{label}</a>' if hyperlink else label
    pltdate = hdateutils.to_python_date(pdate) if xmode == "date" else hdateutils.to_years(pdate)
    fig.add_trace(go.Scatter(x = [pltdate], y=[y+0.04], 
                                name=label, legendgroup=label,
                                mode="text", text=hlinkedtext, 
                                textposition='bottom center',
                                hoverinfo='skip', hoverlabel={'namelength':-1}, showlegend=False))
# ------------------------------------------------------------------------------------------------
def _add_trace_part(figure, pdate_start=None, pdate_end=None, label="", y=0.0, 
                color=None, width=4, dash=None, 
                hovertext=None, hovertext_end=None, 
                xmode="date", dateformat="default", pointinterval=200
                ):
    "Add a line to the figure"
    
    # BC dates are ignored if xmode == "date"
    if xmode == "date" and hdateutils.to_ordinal(pdate_start, dateformat=dateformat) <= 0:
        return

    if hovertext_end is None:
        hovertext_end = hovertext

    if (pdate_start <= pdate_end): 
        if xmode == "date":
            pointinterval = datetime.timedelta(days=pointinterval)
            xs = [hdateutils.to_python_date(pdate_start, dateformat=dateformat) + n * pointinterval for n in 
                range(ceil((hdateutils.to_python_date(pdate_end, dateformat=dateformat) - 
                                    hdateutils.to_python_date(pdate_start, dateformat=dateformat)).total_seconds()/
                                pointinterval.total_seconds()))] + [hdateutils.to_python_date(pdate_end, dateformat=dateformat)]
        else:
            xs = [hdateutils.to_years(hdateutils.to_ordinal(pdate_start, dateformat=dateformat) + n * pointinterval) for n in 
                    range(ceil((hdateutils.to_ordinal(pdate_end, dateformat=dateformat) - 
                                            hdateutils.to_ordinal(pdate_start, dateformat=dateformat))/
                                pointinterval))] + [hdateutils.to_years(pdate_end, dateformat=dateformat)]
        ys = [y for _ in xs]
        hovertexts = label if not hovertext \
                        else hovertext if hovertext == hovertext_end \
                        else [hovertext for _ in range(len(xs) - 1)] + [hovertext_end]
        figure.add_trace(go.Scatter(x = xs, y=ys, name=label, legendgroup=label,
                            mode="lines", line={'color':color,'width':width,'dash':dash}, 
                            hoverinfo='text',
                            hovertext=hovertexts,
                            hoverlabel={'namelength':-1}, showlegend=False))


