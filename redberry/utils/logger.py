import logging


def init_logger():
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    logger = logging.getLogger('redberry')

    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
