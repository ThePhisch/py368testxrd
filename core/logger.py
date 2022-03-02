import logging

def setup_logging(chosen_level: int) -> None:
    """
    Sets up logging depending on the chosen log level
    : chosen_level
    -> minimum level for log to become visible: 0 warning; 1 info; 2 debug
    """
    if chosen_level == 0:
        logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s:%(message)s")
        logging.debug("Logging remains at WARNING")
    elif chosen_level == 1:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
        logging.info("Logging has been set to INFO")
    elif chosen_level == 2:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s")
        logging.info("Logging has been set to DEBUG")
    
    # other cases have already been ruled out by argparse