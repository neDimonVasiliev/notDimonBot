import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [

]

PAYMASTER_TOKEN = ""
# https://www.youtube.com/watch?v=yZj4ieTMvr0

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}


DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_NAME = str(os.getenv("DB_NAME"))
DB_HOST = str(os.getenv("DB_HOST"))

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

no_image_pic_url = "https://telegra.ph//file/94fc414bd9f195140d1a9.jpg"
