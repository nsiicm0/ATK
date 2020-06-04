import os
import sys
import json
import logging.config
from dotenv import load_dotenv

class MetaClass(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args)
        # Logging Setup
        # Explicit name mangling
        #logger_attribute_name = '_' + cls.__name__ + '__logger'
        logger_attribute_name = 'log_as'

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = '.'.join([c.__name__ for c in cls.mro()[-2::-1]])
        MetaClass.setup_logging(**kwargs)
        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))

        # Config Setup
        config_loaded_name = 'config_loaded'
        load_dotenv()
        setattr(cls, config_loaded_name, True)

    @staticmethod
    def setup_logging(log_config: str = 'logging.json', default_level: int = logging.INFO) -> None:
        """Setup logging configuration
        """
        path = os.path.join(os.path.dirname(sys.argv[0]), log_config)
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
