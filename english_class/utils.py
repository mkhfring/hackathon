# In the name of God

import logging


def get_logger():
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    return logger
