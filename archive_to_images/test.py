import logging

from transformer import Transformer

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
i = Transformer(["/home/user/Desktop/imgbck/ciao"], "archivio", 1024 * 1000)
i.process()
