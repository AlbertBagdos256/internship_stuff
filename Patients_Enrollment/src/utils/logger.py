import logging


"""
    Create and configure a logger instance.

    Parameters
    ----------
    name : str
        Logger name, typically __name__.

    Returns
    -------
    logging.Logger
        Configured logger instance.
"""
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.propagate = False

    return logger