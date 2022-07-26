from yaml import load 
from yaml import CLoader as Loader
import os

class Config():
    def __init__(self):
        conff = os.environ.get("CONF_FILE")
        self.pipelines = load(open(conff), Loader=Loader)

        self.kafka_server = os.environ.get('KAFKA_SERVER', 'kafka') 
        self.kafka_clientgroup = os.environ.get('KAFKA_CLIENTGROUP', 'value_add')
        self.topics = os.environ.get('KAFKA_TOPICS', 'workspaceevents').split(',')
        self.max_handler_failures = 3


