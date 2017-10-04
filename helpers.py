import logging
from logging.handlers import RotatingFileHandler
from subprocess import Popen, PIPE

def setup_logging(file_path, max_size):
    """
    Setup handlers to log events
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create rotating file handler that logs info, warn, error & critical messages
    fh = RotatingFileHandler(file_path,
                             mode="a",
                             maxBytes=max_size*1024*1024,
                             backupCount=0)
    fh.setLevel(logging.INFO)

    # Create console handler with the same log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

def package_exists(pkg):
    """
    Checks if a given package exists on the os
    """
    proc = Popen(["which", pkg], stdout=PIPE, stderr=PIPE)
    exit_code = proc.wait()

    if exit_code == 0:
        return True

    return False