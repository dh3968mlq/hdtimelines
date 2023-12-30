from hdtimelines import hdtimeline

def test_hdtimeline():
    hd = hdtimeline.hdTimeLine("Test timeline")
    hd.add_topic_csv('Monarchs extract','./test_data/British Monarchs_extract_ok.csv')
    daterange = hd.get_date_range()

    assert hd.title == "Test timeline"
    assert len(hd.topics) == 1
    assert daterange == (373444, 740710)
    assert hd.topics[0].title == 'Monarchs extract'
    dtest = {'label': 'William I', 
            'hdate': '1066-12-25', 
            'hdate_end': '1087-09-09', 
            'hdate_birth': 'c. 1028', 
            'hdate_death': '1087-09-09', 
            'url': 'https://en.wikipedia.org/wiki/William_the_Conqueror'}
    assert hd.topics[0].events[0] == dtest

    return