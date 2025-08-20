import os
from dotenv import load_dotenv

#Загружаю переменные из окружения
load_dotenv()

DSN = os.getenv('DSN')