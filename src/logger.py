import logging
import os
from datetime import datetime

def get_logger(name: str) -> logging.Logger:      # -> logging.logger tells that this fuction will return a logger object
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    log_path = os.path.join(logs_dir, log_file)

    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    return logging.getLogger(name)
