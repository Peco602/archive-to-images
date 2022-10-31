import logging

from recover import Recover
from transformer import Transformer

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
i = Transformer(["/home/user/Desktop/imgbck/ciao"], "amore", 1024 * 1000)
i.process()

r = Recover(["/home/user/Desktop/archive_to_images/amore"])
r.process()
