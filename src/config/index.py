import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME', 'default')
MASTER_DATA_API_DIR = os.getenv('MASTER_DATA_API_DIR', '/mnt/c/Users/default')
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY', 'default:fx')
