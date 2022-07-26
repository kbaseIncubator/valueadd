from utils.config import Config
from utils.event import Event
from utils.event_loop import start_loop
from utils.pipeline import run_pipeline
import utils.kafka as kafka
import atexit
import signal

def _log_err(msg, err=None):
    """Log an indexing error in an elasticsearch index."""
    # The key is a hash of the message data body
    # The index document is the error string plus the message data itself
    print(msg)


def _exit_handler(consumer):
    def handler(signum, stack_frame):
        kafka.close_consumer(consumer)

    def handler_noargs():
        kafka.close_consumer(consumer)

    return (handler, handler_noargs)

def confg_update():
    pass

def looper(conf):
    # Initialize and run the Kafka consumer
    consumer = kafka.init_consumer(conf)
    (handler, handler_noargs) = _exit_handler(consumer)
    atexit.register(handler_noargs)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    # Run the main thread
    start_loop(
            conf,
            consumer,
            _handle_msg
            )
#        on_config_update=es_indexer.reload_aliases)
#        on_success=_log_msg_to_elastic,
#        on_failure=_log_err_to_es,

def _handle_msg(msg, config=None):
    event = Event(msg)
    if event.evtype == "NEW_VERSION":
        for pname in config.pipelines:
            pipeline = config.pipelines[pname]
            if event.objtype in pipeline["trigger_on"]:
                run_pipeline(pipeline, event)

if __name__ == "__main__":
    conf = Config()
    looper(conf) 
