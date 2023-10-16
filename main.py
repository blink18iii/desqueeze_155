import os
from PIL import Image
import PIL
import sys
import telepot


try:
    BOT_TOKEN = 'YOUR_TOKEN'
except KeyError:
    BOT_TOKEN = sys.argv[1]


def resize_image(path):
    img = Image.open(path)
    width, height = img.size
    if width > height:
        new_image = img.resize((int(width * 1.55), height), PIL.Image.ANTIALIAS)
        new_image.save(path, quality='high')
    else:
        new_image = img.resize((width, int(height * 1.55)), PIL.Image.ANTIALIAS)
        new_image.save(path, quality='high')
    return path


def chat_handler(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    if "reply_to_message" in msg and "/crop" in msg["text"]:
        msg = msg["reply_to_message"]
        msg_type, chat_type, chat_id = telepot.glance(msg)
    elif msg_type not in ["document", "photo"]:
        return

    if msg_type == "document":
        if msg["document"]["mime_type"] in ["image/png", "image/jpeg"]:
            file_id = msg["document"]["file_id"]
        else:
            return
    elif msg_type == "photo":
        file_id = msg["photo"][-1]["file_id"]
    else:
        return

    file_path = "downloads/" + bot.getFile(file_id)["file_path"].split("/")[1]

    bot.download_file(file_id, file_path)

    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        bot.sendDocument(chat_id, f)

    os.remove(file_path)


if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Instantiate bot
    bot = telepot.Bot(BOT_TOKEN)

    # New message listener
    bot.message_loop({'chat': chat_handler},
                     run_forever="Running....")
