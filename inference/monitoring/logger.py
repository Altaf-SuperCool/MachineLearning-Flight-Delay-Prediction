import logging
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("inference")
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s"
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.propagate = False
