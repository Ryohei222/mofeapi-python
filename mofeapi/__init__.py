from logging import NullHandler, getLogger

logger = getLogger(__name__)
logger.addHandler(NullHandler())
