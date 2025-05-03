import os
import telebot
from flask import Flask, request
import requests

API_KEY = '3c0360cf35eddb15a7d2728e8285d723'
TOKEN = '7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def get_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://telebot-olive-chi.vercel.app/7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ')
    return 'Webhook set', 200

# Настройка обработчиков команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Введи название города для получения прогноза погоды.')

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text.strip()  # Получаем название города от пользователя
    if not city:
        bot.send_message(message.chat.id, "Пожалуйста, введите название города.")
        return
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_desc = data['list'][0]['weather'][0]['description']
            temperature = data['list'][0]['main']['temp']
            feels_like = data['list'][0]['main']['feels_like']
            weather_info = f'Прогноз для города {city}:\nОписание погоды: {weather_desc}\nТемпература: {temperature}°C\nОщущается как: {feels_like}°C\n'
            bot.send_message(message.chat.id, weather_info)
        else:
            bot.send_message(message.chat.id, "Не удалось найти информацию о погоде для этого города.")
    except requests.exceptions.RequestException:
        bot.send_message(message.chat.id, "Ошибка при подключении к серверу. Попробуй позже.")

if __name__ == "__main__":
    app.run(debug=True)
