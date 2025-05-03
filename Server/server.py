from flask import Flask, request
import telebot


API_KEY = '3c0360cf35eddb15a7d2728e8285d723'
TOKEN = '7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + '7824623081:AAGTBVknUPH2-9u203zGdx5vry6GsnxY5JQ', methods=['POST'])
def get_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'http://127.0.0.1:5000/{TOKEN}')
    return 'Webhook set', 200

if __name__ == "__main__":
    app.run(debug=True)
