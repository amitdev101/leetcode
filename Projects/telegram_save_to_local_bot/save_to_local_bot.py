import os
import hashlib
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import json

# Configurable Constants
BOT_TOKEN = "YOUR_BOT_TOKEN"
BASE_DIR = "TelegramBotFiles"
LOG_FILE = "bot_activity.log"
OFFSET_FILE = "last_update_offset.txt"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3  # Number of backup log files

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Configure Logging
logger = logging.getLogger("TelegramBot")
logger.setLevel(logging.INFO)

# File Handler with Rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_COUNT)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Utility Functions
def get_user_directory(chat_id):
    """Create and return a directory for the given user."""
    user_dir = os.path.join(BASE_DIR, str(chat_id))
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def save_offset(update_id):
    """Save the last update ID to a file."""
    with open(OFFSET_FILE, "w") as file:
        file.write(str(update_id))

def load_offset():
    """Load the last update ID from a file."""
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as file:
            return int(file.read().strip())
    return None

def save_text_message(chat_id, text):
    """Save text messages to a JSON file with proper Unicode support."""
    user_dir = get_user_directory(chat_id)
    message_file = os.path.join(user_dir, "messages.json")

    # Load existing messages if the file exists
    messages = []
    if os.path.exists(message_file):
        with open(message_file, "r", encoding="utf-8") as file:
            messages = json.load(file)

    # Add the new message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append({"timestamp": timestamp, "message": text})

    # Save back to the JSON file
    with open(message_file, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

    logger.info(f"Saved text message for User ID: {chat_id}")


async def download_file_with_progress(file, filepath, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Download a file with progress updates."""
    file_url = file.file_path
    response = requests.get(file_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024 * 1024  # 1 MB
    downloaded_size = 0

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                percent = int((downloaded_size / total_size) * 100)
                if percent % 10 == 0:
                    await context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f"Downloading {os.path.basename(filepath)}: {percent}% complete..."
                    )

async def save_file(file, user_dir, extension, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save a file with its hash as the filename."""
    # Temporary download path
    temp_filepath = os.path.join(user_dir, f"temp.{extension}")
    await download_file_with_progress(file, temp_filepath, update, context)

    # Calculate hash and determine final path
    file_hash = hashlib.md5(open(temp_filepath, "rb").read()).hexdigest()
    final_filepath = os.path.join(user_dir, f"{file_hash}.{extension}")

    if os.path.exists(final_filepath):
        # File already exists
        os.remove(temp_filepath)  # Clean up temporary file
        logger.info(
            f"Duplicate file detected. User ID: {update.message.chat_id}, File Hash: {file_hash}"
        )
        return None, None, "Duplicate file detected."

    # Rename temp file to hash-based name
    os.rename(temp_filepath, final_filepath)
    logger.info(
        f"File saved. User ID: {update.message.chat_id}, File Hash: {file_hash}, Path: {final_filepath}"
    )
    return final_filepath, file_hash, "File saved successfully."

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text(
        "Hello! Send me any file or message, and I will save it securely.\n"
        "I support:\n"
        "- Text messages\n"
        "- Photos\n"
        "- Videos"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and files."""
    chat_id = update.message.chat_id

    if update.message.text:
        # Save text message
        save_text_message(chat_id, update.message.text)
        await update.message.reply_text("Your message has been saved!")

    elif update.message.photo:
        # Save the highest resolution photo
        user_dir = get_user_directory(chat_id)
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        filepath, file_hash, status = await save_file(file, user_dir, "jpg", update, context)

        if filepath:
            await update.message.reply_text(
                f"Photo saved!\n\nFilename: {os.path.basename(filepath)}\nHash: {file_hash}\nSaved at: {filepath}"
            )
        else:
            await update.message.reply_text(f"Photo not saved: {status}")

    elif update.message.video:
        # Save video
        user_dir = get_user_directory(chat_id)
        file = await context.bot.get_file(update.message.video.file_id)
        filepath, file_hash, status = await save_file(file, user_dir, "mp4", update, context)

        if filepath:
            await update.message.reply_text(
                f"Video saved!\n\nFilename: {os.path.basename(filepath)}\nHash: {file_hash}\nSaved at: {filepath}"
            )
        else:
            await update.message.reply_text(f"Video not saved: {status}")

    else:
        await update.message.reply_text("Unsupported content type!")
        logger.info("unsupported content : " + update.message)
    
    # Save the last update offset after processing the message
    save_offset(update.update_id)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

# Main Function
def main():
    """Start the bot."""

    application = Application.builder().token(BOT_TOKEN).build()


    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    application.add_error_handler(error_handler)

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
