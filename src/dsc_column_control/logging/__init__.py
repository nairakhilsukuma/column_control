import os
import sys
import logging

# generic logging structure

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir,"logging.log")
os.makedirs(log_dir, exist_ok = True)

logging.basicConfig(
    level = logging.INFO,
    format = logging_str,
    
    handlers =[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout) #Allows rendering msgs which we put inside log_filepath when we run int erminal
    ]
)

logger = logging.getLogger("dscwinequalitylogger")