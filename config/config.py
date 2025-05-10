from dotenv import load_dotenv
from os import getenv
from secrets import token_hex

load_dotenv()

SECRET_KET = getenv("SECRET_KEY")
TOKEN = str(token_hex(64))

