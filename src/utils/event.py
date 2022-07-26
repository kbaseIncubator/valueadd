from .kafka import init_consumer
from typing import Dict

class Event():
    def __init__(self, event: Dict):
        self.evtype = event["evtype"]
        self.wsid = event["wsid"]
        self.objid = event["objid"]
        self.ver = event["ver"]
        self.upa = None
        if self.wsid and self.objid and self.ver:
            self.upa = "%d/%d/%d" % (self.wsid, self.objid, self.ver)
        self.objtype = None
        if "objtype" in event and event['objtype']:
            self.objtype = event["objtype"].split("-")[0]


#        event = {
#          "user": "auser",
#          "wsid": 52407,
#          "objid": 29,
#          "ver": 1,
#          "time": 1658208187000,
#          "evtype": "NEW_VERSION",
#          "objtype": "KBaseGenomes.Genome-17.0"
#        }
#        return Event(event)

