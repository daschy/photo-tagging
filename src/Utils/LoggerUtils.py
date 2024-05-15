import logging
import coloredlogs


def GetLogger(name: str):
    log = logging.getLogger(name)
    level = logging.DEBUG
    coloredlogs.install(logger=log, level=level)
    log.setLevel(level)
    return log
