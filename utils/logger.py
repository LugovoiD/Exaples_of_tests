import logging
import os


def get_logger(name='ui_tests_logger'):
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
    return logging.getLogger(name)


def configure_logging(name="ui_tests_logger", level=logging.DEBUG, format='%(asctime)-18s %(levelname)-4s %(message)s',
                      file_name="log.txt"):
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
    filename = os.path.join(path,
                            f'tests/reports/log', file_name)

    logging.basicConfig(level=level, format=format)

    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(logging.Formatter(fmt=format))
    logger.addHandler(file_handler)
