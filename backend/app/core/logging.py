import logging
import sys

def setup_logging():
    logger = logging.getLogger("safespeak")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()
