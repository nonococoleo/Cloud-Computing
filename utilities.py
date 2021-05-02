import logging
import hashlib


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    FORMAT = '%(levelname)7s [%(asctime)s - %(filename)20s:%(lineno)3s] - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger.setLevel(level)
    return logger


def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()
