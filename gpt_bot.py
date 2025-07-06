import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import openai
from dotenv import load_dotenv

# 🔐 Maxfiy kalitlarni yuklash
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenAI API sozlash
openai.api_key = OPENAI_API_KEY

# ChatGPT javob olish funksiyasi
async def ask_chatgpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # yoki "gpt-4" agar sizda mavjud bo‘lsa
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"

# Foydalanuvchi matnini qayta ishlovchi handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.chat.send_action(action="typing")
    response = await ask_chatgpt(user_input)
    await update.message.reply_text(response)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Men ChatGPT botman. Menga savolingizni yozing.")

# Botni ishga tushirish
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot ishga tushdi...")
    app.run_polling()
