import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_api_keys = {}

WELCOME_MSG = """
👋 Halo! Selamat datang di **NexaAI Generator Bot**!

Untuk mulai generate video AI dengan Freepik, ikuti langkah berikut:

1️⃣ Daftar akun Freepik Developer & aktifkan Paid Plan  
2️⃣ Dapatkan API Key dari: https://www.freepik.com/developers/dashboard/api-key  
3️⃣ Kirim perintah:  
   `/addprivatekey API_KEY_ANDA`

Pilih menu di bawah untuk mulai 👇
"""

def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎬 Generate Video", callback_data='generate')],
        [InlineKeyboardButton("🔑 Add Private Key", callback_data='addkey'),
         InlineKeyboardButton("📊 Status", callback_data='status')],
        [InlineKeyboardButton("❓ Help", callback_data='help'),
         InlineKeyboardButton("🚫 Cancel", callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MSG, reply_markup=build_main_menu(), parse_mode='Markdown')

async def add_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("UsageId: `/addprivatekey YOUR_API_KEY`", parse_mode='Markdown')
        return
    user_id = update.effective_user.id
    user_api_keys[user_id] = context.args[0]
    await update.message.reply_text("✅ API Key berhasil disimpan!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = "🟢 API Key aktif." if user_id in user_api_keys else "🔴 Belum ada API Key."
    await update.message.reply_text(msg)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'generate':
        await query.edit_message_text("🎥 Kirim prompt teks atau upload gambar untuk mulai!")
    elif query.data == 'addkey':
        await query.edit_message_text("🔑 Kirim: `/addprivatekey YOUR_API_KEY`", parse_mode='Markdown')
    elif query.data == 'status':
        user_id = update.effective_user.id
        msg = "🟢 API Key aktif." if user_id in user_api_keys else "🔴 Belum ada API Key."
        await query.edit_message_text(msg)
    elif query.data == 'help':
        await query.edit_message_text("❓ Bantuan: Kirim /start untuk menu utama.")
    elif query.data == 'cancel':
        await query.edit_message_text("❌ Dibatalkan.")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN tidak ditemukan! Tambahkan di Render sebagai environment variable.")
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addprivatekey", add_private_key))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("✅ Bot sedang berjalan...")
    app
