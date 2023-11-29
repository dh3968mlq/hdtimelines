try:
    import historicaldate.hdate as hdate
    import historicaldate.hdateutils as hdateutils
    import hdtimelines.hdpl as hdpl
except:
    import historicaldate.historicaldate.hdate as hdate
    import historicaldate.historicaldate.hdateutils as hdateutils
    import hdtimelines.hdtimelines.hdpl as hdpl

def calc_date_ordinals(hd, dprefix="", dateformat=None, missingasongoing=False):
    """
    Calculate ordinals for a single date, return as a dictionary with keys
    <dprefix>_early, <dprefix>_mid, <dprefix>_late, <dprefix>_ongoing

    * *hd* (str): A string representing a date in a format recognised by HDate()
    * *dateformat*, *missingasongoing*: as for HDate()

    Other code assumes that any entry in d of type int is an ordinal date
    """
    pd = hdate.HDate(hd, missingasongoing=missingasongoing, dateformat=dateformat).pdates
    if pd:
        d = {f"{dprefix}_early":pd["ordinal_early"],
            f"{dprefix}_mid":pd["ordinal_mid"],
            f"{dprefix}_late":pd["ordinal_late"]}
        d[f"{dprefix}_ongoing"] = (pd['slmid'] == 'o')
    else:
        d = {}
    return d
# ------------------------------------------------------------------------------------------------------------------
def calc_event_ordinals(event, dateformat=None):
    """
    Calculate ordinals for all the dates in an event, return as a dictionary with keys:

    start_early, start_mid, start_late, start_ongoing,
    end_early, end_mid, end_late, end_ongoing,
    birth_early, birth_mid, birth_late, birth_ongoing,
    death_early, death_mid, death_late, death_ongoing,
    earliest, latest, label

    All dictionary values are (int) ordinals, except for ..._ongoing, which are bool
    """
    d = {}
    if (hd := event.get("hdate", None)) is not None: 
        d.update(calc_date_ordinals(hd, "start", dateformat=dateformat))
    if (hd := event.get("hdate_end", None)) is not None: 
        d.update(calc_date_ordinals(hd, "end", dateformat=dateformat))
    if (hd := event.get("hdate_birth", None)) is not None: 
        d.update(calc_date_ordinals(hd, "birth", dateformat=dateformat))
    if (hd := event.get("hdate_death", None)) is not None: 
        d.update(calc_date_ordinals(hd, "death", dateformat=dateformat, 
                        missingasongoing=(d.get("birth_mid", None) is not None)))

    d["earliest"] = min({val for val in d.values() if type(val)==int})
    d["latest"] = max({val for val in d.values() if type(val)==int})

    # -- Calculate the label date
    if d.get("start_mid", None) is not None:
        if d.get("end_mid", None) is not None:
            labeldate = d['start_mid'] + int((d['end_mid'] - d['start_mid'])/2.0)
        else:
            labeldate = d['start_mid']
    elif d.get("birth_mid", None) is not None:
        if d.get("death_mid", None) is not None:
            labeldate = d['birth_mid'] + int((d['death_mid'] - d['birth_mid'])/2.0)
        else:
            labeldate = d['birth_mid']
    d["label"] = labeldate
    return d
# -----------------------------------------------------------------------------------
def calc_age(ymd_birth, ymd_ref):
    """
    Calculate a person's age from ymd of birth and death

    *ymd_birth*, *ymd_death* must be named tuples, as returned by *hdateutils.to_ymd*
    """
    age = ymd_ref.year - ymd_birth.year
    if ymd_birth.year < 0 and ymd_ref.year > 0:
        age = age - 1   # there is no year 0
    if (ymd_ref.month < ymd_birth.month) or (ymd_ref.month < ymd_birth.month and ymd_ref.day < ymd_birth.day):
        age = age - 1 
    if age < 0:
        raise ValueError("Age calculated as less than 0")
    return age
# ------------------------------------------------------------------------------------
def calc_agetext(pdates_birth, pdates_ref):
    "Calculate age text, including ? to indicate uncertainty, from *plTimeLine().pdates* properties"
    ymd_birth_early = hdateutils.to_ymd(pdates_birth['ordinal_early'])
    ymd_birth_mid = hdateutils.to_ymd(pdates_birth['ordinal_mid'])
    ymd_birth_late = hdateutils.to_ymd(pdates_birth['ordinal_late'])
    ymd_ref_early = hdateutils.to_ymd(pdates_ref['ordinal_early'])
    ymd_ref_mid = hdateutils.to_ymd(pdates_ref['ordinal_mid'])
    ymd_ref_late = hdateutils.to_ymd(pdates_ref['ordinal_late'])

    years_largest = calc_age(ymd_birth_early, ymd_ref_late)
    years_smallest = calc_age(ymd_birth_late, ymd_ref_early)
    uncertain = '?' if years_largest > years_smallest else ""

    years = calc_age(ymd_birth_mid, ymd_ref_mid)
    return f"{years}{uncertain}"
# -----------------------------------------------------------------------------------
def calc_yeartext(pdates, hover_datetype='day'):
    """
    Calculate text to represent a date, including representation of uncertainty,
    from a *plTimeLine().pdates* property
    """
    if hover_datetype not in {'year','month','day'}:
        raise ValueError(f"hover_datetype must be year, month or day. Found:{hover_datetype}")
    
    ymd_early = hdateutils.to_ymd(pdates['ordinal_early'])
    ymd_mid = hdateutils.to_ymd(pdates['ordinal_mid'])
    ymd_late = hdateutils.to_ymd(pdates['ordinal_late'])

    ytext = str(ymd_mid.year) if ymd_mid.year > 0 else str(-ymd_mid.year) + "BCE"
    if (ymd_early.year != ymd_late.year):
        ytext = ytext + "?"             # Show uncertain year
    if (ymd_early.month == ymd_late.month) and (ymd_early.year == ymd_late.year) and hover_datetype != 'year':
        months = ["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        ytext = f"{months[ymd_mid.month - 1]} {ytext}"
    if (ymd_early == ymd_late) and hover_datetype == 'day':
        ytext = f"{ymd_mid.day} {ytext}"      # Show exact date
    return ytext
# -----------------------------------------------------------------------------------
def check_dataframe(df, study_range_start=None, study_range_end=None, dateformat="default"):
    "Check if a dataframe will successfully add as a plTimeLine topic"
    pltl = hdpl.plTimeLine(mindate="2000 BC", maxdate="2200", xmode="years", dateformat=dateformat)
    message = ""
    try:
        added = pltl.add_topic_from_df(df, study_range_start=study_range_start, study_range_end=study_range_end)
        if not added:
            message = "No events found in study range"
    except Exception as e:
        added = False
        message = f"Error: {repr(e)}"
    return added, message
