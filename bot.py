import telebot
import sqlite3
import time
from telebot import types

BOT_TOKEN = "8993369092:AAHEt3JGqRCFOjjn1GSfba5OenCaX8UdMo0"
ADMIN_ID = 559583540

bot = telebot.TeleBot(BOT_TOKEN)

# Vercel-dan olingan to'g'ri havola
WEB_APP_URL = "https://sxhrobcoin-game.vercel.app" 

# Ma'lumotlar bazasini sozlash
def init_db():
    conn = sqlite3.connect("clicker_database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        coins REAL DEFAULT 0,
        diamonds REAL DEFAULT 0,
        energy INTEGER DEFAULT 500
    )
    """)
    conn.commit()
    conn.close()

init_db()

# /start bosilganda Web App tugmasini chiqarish
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    conn = sqlite3.connect("clicker_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    # Telegram pastki paneli uchun tugma sozlamasi
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_info = types.WebAppInfo(WEB_APP_URL)
    
    # Xuddi Yumicoin-dek chiroyli "Open" tugmasi
    open_button = types.KeyboardButton(text="✨ Open - Sxhrobcoin", web_app=web_app_info)
    markup.add(open_button)
    
    welcome_text = (
        "👋 *Sxhrob Coin Clicker o'yiniga xush kelibsiz!*\n\n"
        "🎮 Mini-ilovani ochish va tanga bosishni boshlash uchun pastdagi *✨ Open - Sxhrobcoin* tugmasini bosing!"
    )
    
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

print("🤖 Bot Web App rejimida muvaffaqiyatli ishga tushdi...")
bot.infinity_polling()
  
