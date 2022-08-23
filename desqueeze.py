import os
from PIL import Image
import PIL
import sys
import telepot
from dotenv import load_dotenv

load_dotenv()

try:
    BOT_TOKEN = os.getenv('TOKEN')
except KeyError:
    BOT_TOKEN = sys.argv[1]

# endpoint = f'https://api.telegram.org/bot{BOT_TOKEN}'
# file_endpoint = f'https://api.telegram.org/file/bot{BOT_TOKEN}'


def resize_image(path):
    img = Image.open(path)
    width, height = img.size
    if (width == 4032 and height == 3024) or (width == 1280 and height == 960):
        new_image = img.resize((6250, 3024), PIL.Image.Resampling.LANCZOS)
        new_image.save(path, quality='high')
    else:
        new_image = img.resize((3024, 6250), PIL.Image.Resampling.LANCZOS)
        new_image.save(path, quality='high')
    return path


def chat_handler(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    if "reply_to_message" in msg and "/crop" in msg["text"]:
        msg = msg["reply_to_message"]
        msg_type, chat_type, chat_id = telepot.glance(msg)
    elif msg_type not in ["document", "photo"]:
        return

    # Handle compressed/uncompressed images
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
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Instantiate bot
    bot = telepot.Bot(BOT_TOKEN)

    # New message listener
    bot.message_loop({'chat': chat_handler},
                     run_forever="Bot Running...")
