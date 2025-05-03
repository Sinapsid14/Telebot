import telebot
import requests
# Шаг 1.задаем начальные параметры бота в системе,его апи и бот токен

API_KEY = '3c0360cf35eddb15a7d2728e8285d723'  # Твой API-ключ
bot = telebot.TeleBot('7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ')


#Шаг 2 делаем команду для начала работы с ботом. Все начинается с команды старт.

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Введи название города для получения прогноза погоды.')


# Обработчик любого текстового сообщения (запрос города)
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
            # Делаем вывод погоды на основе данных
            weather_desc = data['list'][0]['weather'][0]['description']
            temperature = data['list'][0]['main']['temp']
            feels_like = data['list'][0]['main']['feels_like']
            weather_info = (
                f'Прогноз для города {city}:\n'
                f'Описание погоды: {weather_desc}\n'
                f'Температура: {temperature}°C\n'
                f'Ощущается как: {feels_like}°C\n'
            )
            bot.send_message(message.chat.id, weather_info)
        else:
            bot.send_message(message.chat.id, "Не удалось найти информацию о погоде для этого города. Попробуй снова.")

    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, "Ошибка при подключении к серверу. Попробуй позже.")


# Запуск бота
bot.polling(none_stop=True)

TOKEN = '7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ'
API_KEY = 'f7a12a13b8b25f2650572806487eb3a4'


