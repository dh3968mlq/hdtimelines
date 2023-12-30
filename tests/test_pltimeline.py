from hdtimelines import pltimeline
from historicaldate import hdateutils

def test1():
    pltl = pltimeline.plTimeLine("Hello world",mindate="1900-01-01", maxdate="2025", 
                 dateformat="mdy")
    assert pltl.mindate == hdateutils.to_ordinal("1 jan 1900")
    assert pltl.maxdate == hdateutils.to_ordinal("15 Jun 2025")
    assert pltl._dateformat == "mdy"
    assert pltl.fig_config == {'scrollZoom': True}
    assert pltl._xmode == "date"
    assert pltl.max_y_used == 0.0
    return