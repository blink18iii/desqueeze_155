import os
from PIL import Image
import numpy as np
import cv2
import pillow_heif
from pillow_heif import register_heif_opener
import PIL
import sys
import telepot
from dotenv import load_dotenv

load_dotenv()
register_heif_opener()


try:
    BOT_TOKEN = os.getenv('TOKEN')
except KeyError:
    BOT_TOKEN = sys.argv[1]


def resize_image(path):
    img = Image.open(path)
    width, height = img.size
    if width > height:
        new_image = img.resize((int(width * 1.55), height), PIL.Image.Resampling.LANCZOS)
        new_image.save(path)
    else:
        new_image = img.resize((width, int(height * 1.55)), PIL.Image.Resampling.LANCZOS)
        new_image.save(path)
    return path


def chat(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    if msg_type not in ["document", "photo"]:
        return

    if msg_type == "document":
        if msg["document"]["mime_type"] in ["image/png", "image/jpeg", "image/heic", "image/heif"]:
            file_id = msg["document"]["file_id"]
    elif msg_type == "photo":
        file_id = msg["photo"][-1]["file_id"]
    else:
        return

    file_path = "photos/" + bot.getFile(file_id)["file_path"].split("/")[1]

    # Download file
    bot.download_file(file_id, file_path)

    # Resize and send file
    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        bot.sendDocument(chat_id, f)

    # Clean up working directory
    os.remove(file_path)
    # os.remove(new_file_path)


if __name__ == "__main__":
    if not os.path.exists("photos"):
        os.makedirs("photos")

    # Instantiate bot
    bot = telepot.Bot(BOT_TOKEN)

    # New message listener
    bot.message_loop({'chat': chat},
                     run_forever="Bot Running...")