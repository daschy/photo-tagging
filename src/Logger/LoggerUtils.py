import logging
import coloredlogs
import re


# To control logging level for various modules used in the application:
def _set_global_logging_level(level=logging.ERROR, prefices=[""]):
    """
    Override logging levels of different modules based on their name as a prefix.
    It needs to be invoked after the modules have been loaded so that their loggers have been initialized.

    Args:
        - level: desired level. e.g. logging.INFO. Optional. Default is logging.ERROR
        - prefices: list of one or more str prefices to match (e.g. ["transformers", "torch"]). Optional.
          Default is `[""]` to match all active loggers.
          The match is a case-sensitive `module_name.startswith(prefix)`
    """
    prefix_re = re.compile(rf'^(?:{ "|".join(prefices) })')
    for name in logging.root.manager.loggerDict:
        if re.match(prefix_re, name):
            logging.getLogger(name).setLevel(level)


def GetLogger(name: str):
    _set_global_logging_level(
        logging.ERROR,
        ["transformers", "nlp", "torch", "tensorflow", "tensorboard", "wandb", "gliner", "sqlalchemy"],
    )
    log = logging.getLogger(name)
    level = logging.DEBUG
    coloredlogs.install(logger=log, level=level)
    log.setLevel(level)
    return log
