import os
from dotenv import load_dotenv

#Загружаю переменные из окружения
load_dotenv()

DSN = os.getenv('DSN')
TEST_DSN = os.getenv('TEST_DSN')