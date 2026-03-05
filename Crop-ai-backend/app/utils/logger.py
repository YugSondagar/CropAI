import logging
import os
from datetime import datetime

# Create logs folder if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name
log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y_%m_%d')}.log")

# Logger configuration
logging.basicConfig(
    filename=log_file,
    format="[ %(asctime)s ] %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

# Create logger object
logger = logging.getLogger("CropAI")