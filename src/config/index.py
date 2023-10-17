import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME', 'default')
MASTER_DATA_API_DIR = os.getenv('MASTER_DATA_API_DIR', 'C:\\Users\\default')
