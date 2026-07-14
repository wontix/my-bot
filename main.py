import os
import telebot
from telebot import types
import yt_dlp
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Токен твоего бота
TOKEN = "7330089069:AAGD6v5oD0M_Z83_p6qscF9hVp9zT262DYo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url="https://example.com")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на видео YouTube, и я помогу тебе его скачать.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        try:
            bot.reply_to(message, "Начиныю скачивание видео...")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
                
            os.remove('video.mp4')
            
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при скачивании: {str(e)}")
    else:
        bot.reply_to(message, "Пожалуйста, отправь корректную ссылку на YouTube видео.")

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
