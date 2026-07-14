import os
import threading
import http.server
import socketserver
import telebot
import yt_dlp

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

def run_dummy_server():
    with socketserver.TCPServer(("", int(os.environ.get("PORT", 10000))), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку на YouTube-видео, и я скачаю его для тебя.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    try:
        bot.reply_to(message, "Скачиваю видео, подожди немного...")
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove('video.mp4')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при скачивании: {str(e)}")

print("Бот успешно запущен и готов к работе!")
bot.infinity_polling()
