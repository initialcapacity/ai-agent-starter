import logging


def disable_logging(f):
    def wrapper(*args):
        logging.disable(logging.CRITICAL)
        result = f(*args)
        logging.disable(logging.NOTSET)

        return result

    return wrapper
