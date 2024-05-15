import logging
import coloredlogs


def GetLogger(name: str):
    log = logging.getLogger(name)
    level = logging.DEBUG
    coloredlogs.install(logger=log, level=level)
    log.setLevel(level)
    # logging.basicConfig(
    #     format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    #     # level=logging.DEBUG,
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )
    # logging.setLoggerClass(ColoredLogger)
    return log
