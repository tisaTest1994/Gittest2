import logging
from loguru import logger
from Function.api_function import *


class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="{time:YYYY-MM-DD at HH:mm:ss} | {message}")
