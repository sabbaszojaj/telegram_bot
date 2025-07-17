
import os
import logging
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

# توکن از محیط گرفته می‌شود
TOKEN = os.getenv("BOT_TOKEN")

# آیدی عددی گروه اصلی (Zojajclub)
GROUP_ID = -1002098307027

# شناسه عددی مدیر (دکتر زجاجی)
ADMIN_IDS = [328462927]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_voice_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: Message = update.message

    if not message or not message.voice:
        return

    if not message.reply_to_message or not message.reply_to_message.text:
        return

    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        return

    question = message.reply_to_message.text
    voice = message.voice.file_id

    caption = f"❓ {question}\n\n🎤 پاسخ دکتر زجاجی:"
    await context.bot.send_chat_action(chat_id=GROUP_ID, action=ChatAction.UPLOAD_VOICE)
    await context.bot.send_voice(chat_id=GROUP_ID, voice=voice, caption=caption)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_reply))
    app.run_polling()

if __name__ == "__main__":
    main()
