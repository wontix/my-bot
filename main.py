from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os
import telebot
from yt_dlp import YoutubeDL

# Сюда вставьте ваш токен от BotFather
TOKEN = "8923474171:AAGg84iUEelvNaOti6L3jrWBQCEg4fK3_Qo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне ссылку на видео (TikTok, YouTube, VK), и я попробую его скачать.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if not url.startswith(("http://", "https://")):
        bot.reply_to(message, "Отправьте правильную ссылку, начинающуюся с http:// или https://")
        return

    status_msg = bot.reply_to(message, "⏳ Начинаю скачивание, подождите...")

    outtmpl = f"{message.chat.id}_video.mp4"
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': outtmpl,
        'max_filesize': 45 * 1024 * 1024, # Лимит 45 МБ для бесплатных ботов
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        bot.edit_message_text("🚀 Видео скачано! Отправляю в чат...", chat_id=message.chat.id, message_id=status_msg.message_id)
        with open(outtmpl, 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Ошибка при скачивании. Возможно, файл слишком большой или ссылка не поддерживается.", chat_id=message.chat.id, message_id=status_msg.message_id)
    
    finally:
        if os.path.exists(outtmpl):
            os.remove(outtmpl)

class WebServer(BaseHTTPRequestHandler):
def do_GET(self):
self.send_response(200)
self.send_header("Content-type", "text/html")
self.end_headers()
self.wfile.write(b"Bot is alive!")

def run_web_server():
port = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", port), WebServer)
server.serve_forever()

if __name__ == '__main__':
threading.Thread(target=run_web_server, daemon=True).start()
print("Бот успешно запущен и готов к работе!")
bot.infinity_polling()
