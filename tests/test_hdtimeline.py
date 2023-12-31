import sys
sys.path.insert(0,".") # For Github

from hdtimelines import hdtimeline

def test_hdtimeline():
    hd = hdtimeline.hdTimeLine("Test timeline")
    hd.add_topic_csv('Monarchs extract','./test_data/British Monarchs_extract_ok.csv')
    daterange = hd.get_date_range()

    assert hd.title == "Test timeline"
    assert len(hd.topics) == 1
    assert daterange[0] == 373444
    assert daterange[1] >= 740710    # The data contains a living person, so this moves forward as time passes
    assert hd.topics[0].title == 'Monarchs extract'
    dtest = {'label': 'William I', 
            'hdate': '1066-12-25', 
            'hdate_end': '1087-09-09', 
            'hdate_birth': 'c. 1028', 
            'hdate_death': '1087-09-09', 
            'url': 'https://en.wikipedia.org/wiki/William_the_Conqueror'}
    assert hd.topics[0].events[0] == dtest

    hd.add_topic_csv('Playwrights extract','./test_data/Playwrights_extract_ok.csv')
    hd.move_topic(id=1, indexshift=1)   # Move Monarchs down
    assert [topic.id for topic in hd.topics] == [2, 1]

    assert hd.get_topic_index(2) == 0

    hd.remove_topic(2)
    assert len(hd.topics) == 1
    assert hd.get_topic_index(1) == 0

    d = hd.to_dict()
    hd2 = hdtimeline.hdTimeLine(d=d)
    d2 = hd2.to_dict()
    assert d == d2
    assert d["topics"][0]["events"][0] == dtest

    for key, value in hd.__dict__.items():
        if key not in {"topics", "_maxid"}:
            assert hd2.__dict__[key] == value, f"Failed on {key}, {value}"

    for topic1, topic2 in zip(hd.topics, hd2.topics):
        for key, value in topic1.__dict__.items():
            assert topic2.__dict__[key] == value, f"Topic failed on {key}, {value}"

    return