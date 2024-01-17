'''
hdTimeline class definition
'''
import sys
import pandas as pd

# -- General idea: improves chances of tests and Sphinx builds working if this is included as a submodule
def add_submodule(path):
    if f"./{path}" not in sys.path:
        sys.path.insert(0,f"../../{path}") # -- Needed for Sphinx builds, usually run in the docs subdirectory
        sys.path.insert(0,f"./{path}")  # -- For normal running. Add second so it will go first in the search order
add_submodule("hdtimelines")
add_submodule("historicaldate")

from hdtimelines import hdtopic

# ----------    
class hdTimeLine():
    '''
    Holds a timeline specification
    
    Properties:

    * title (str) : timeline title
    * topics (list of hdTopic): Topics in this timeline
    '''
    def __init__(self, title="", d=None):
        """
        * title (str): timeline title
        * d (dict) (optional): dictionary (as created by *to_dict()*) from which to construct the timeline
        """
        self.topics = []   # List of topics : hdTopic()
        self.title = title
        self._maxid = 0
        self.action_applied = None  # Used to record the last operation. Not updated by methods here, but can be used by clients
        self.xrange_breakpoints = set()
        if d:
            self.from_dict(d)
        return
    # ----------    
    def from_dict(self, d):
        """
        Populate an existing hdTimeLine object from a dictionary d (as created by *to_dict()*)
        """
        self.title = d["title"]
        self.topics = []
        self._maxid = 0
        for dtopic in d["topics"]:
            topic = hdtopic.hdTopic()
            topic.from_dict(dtopic)
            self.topics.append(topic)
            self._maxid = max(self._maxid, topic.id)
        self.xrange_breakpoints = self._xrange_breakpoints()
    # ----------    
    def to_dict(self):
        """
        Convert hdTimeLine object to a dictionary
        """
        d = {"title":self.title,
             "topics":[topic.to_dict() for topic in self.topics]}
        return d
    # ----------    
    def add_topic_df(self, title, df):
        """
        Add a topic passed as Pandas DataFrame *df*
        Returns ID of added topic
        """
        events = df.to_dict(orient='records')
        return self.add_topic_dict(title, events)
    # ----------
    def add_topic_csv(self, title, filename):
        """
        Read .csv file and add topic based on its contents.
        Returns ID of added topic
        """
        df = pd.read_csv(filename, na_filter=False)
        return self.add_topic_df(title, df)
    # ----------
    def add_topic_dict(self, title, events):
        """
        Add topic based on a dictionary of its events.
        Returns ID of added topic
        """
        self._maxid = self._maxid + 1
        self.topics.append(hdtopic.hdTopic(title, events, id=self._maxid))
        self.xrange_breakpoints = self._xrange_breakpoints()
        return self._maxid
    # ----------
    def get_date_range(self):
        """
        Calculate earliest and latest date in this timeline, and return them as 
        a duple (earliest, latest) of ordinals
        """
        if self.topics:
            topic_ranges = [topic.get_date_range() for topic in self.topics]
            mindate = min([topic_range[0] for topic_range in topic_ranges])
            maxdate = max([topic_range[1] for topic_range in topic_ranges])
            return mindate, maxdate
        else:
            return None, None
    # ----------
    def get_topic_index(self, id=None):
        "Find the position of a topic in the list, given its id"
        if id:
            for index, topic in enumerate(self.topics):
                if topic.id == id:
                    return index
            return None
        else:
            return None
    # ----------
    def remove_topic(self, id=None):
        '''
        Remove a topic, given its id. Returns True if an item is removed, False otherwise
        This leaves _maxid unchanged, even if the topic with this ID is removed
        ... has the knock-on consequence that hd2 = hdTimeLine(d=hd.to_dict()) can change _maxid
        '''
        index = self.get_topic_index(id) if id else None

        if index is not None:
            self.topics.pop(index)
            self.xrange_breakpoints = self._xrange_breakpoints()
            return True
        else:
            return False
    # ----------
    def move_topic(self, id=None, indexshift=1):
        """
        Move a topic up or down in the list. indexshift > 0 means move down
        """
        index = self.get_topic_index(id) if id else None
        if index is not None:
            new_index = max(min(index + indexshift, len(self.topics)), 0)
            topic = self.topics[index]
            self.topics.pop(index)
            self.topics.insert(new_index, topic)
            return True
        else:
            return False
    # ----------
    def reorder_topics(self, topic_order):
        '''
        topic_order is a list of topic ids, in the required order
        '''
        current_order = [topic.id for topic in self.topics]

        # -- index_order is a list of current index positions, in the required new order
        index_order = [current_order.index(topic_id) for topic_id in topic_order]

        # -- reorder the topic list
        topics_neworder = [self.topics[index] for index in index_order]
        self.topics = topics_neworder
    # ---------
    def _xrange_breakpoints(self):
        bpoints = {None}
        for topic in self.topics:
            bpoints = bpoints | topic.xrange_breakpoints()
        return bpoints - {None}

