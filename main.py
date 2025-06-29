import os
import telebot
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("💎 Kryształ", "🥦 Buch")
    bot.send_message(message.chat.id, "Wybierz produkt:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["💎 Kryształ", "🥦 Buch"])
def choose_quantity(message):
    user_data[message.chat.id] = {'produkt': message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("1", "2", "3", "5")
    bot.send_message(message.chat.id, f"Ile sztuk {message.text} chcesz?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["1", "2", "3", "5"])
def choose_delivery(message):
    if message.chat.id in user_data:
        user_data[message.chat.id]['ilosc'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🏠 Dowóz", "🏪 Stacjonarnie")
    bot.send_message(message.chat.id, "Wybierz sposób odbioru:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["🏠 Dowóz", "🏪 Stacjonarnie"])
def final_order(message):
    if message.chat.id in user_data:
        user_data[message.chat.id]['odbior'] = message.text
        produkt = user_data[message.chat.id]['produkt']
        ilosc = user_data[message.chat.id]['ilosc']
        odbior = user_data[message.chat.id]['odbior']

        if odbior == "🏠 Dowóz":
            msg = bot.send_message(message.chat.id, "Podaj adres dowozu:")
            bot.register_next_step_handler(msg, get_address)
        else:
            bot.send_message(message.chat.id,
                             f"✅ Zamówienie:\nProdukt: {produkt}\nIlość: {ilosc}\nOdbiór: {odbior}\n\nBędę bywał w różnych miejscach, więc pisz do mnie bezpośrednio na @mordeczka420.")
            # Tutaj możesz wysłać zamówienie do admina

def get_address(message):
    address = message.text
    chat_id = message.chat.id
    produkt = user_data[chat_id]['produkt']
    ilosc = user_data[chat_id]['ilosc']
    odbior = user_data[chat_id]['odbior']

    bot.send_message(chat_id,
                     f"✅ Zamówienie:\nProdukt: {produkt}\nIlość: {ilosc}\nOdbiór: {odbior}\nAdres dowozu: {address}\n\nDziękujemy!")
    # Tutaj wyślij dane do admina @mordeczka420
    admin_id = 6998345138
    bot.send_message(admin_id,
                     f"Nowe zamówienie:\nProdukt: {produkt}\nIlość: {ilosc}\nOdbiór: {odbior}\nAdres: {address}\nUżytkownik: @{message.from_user.username or message.from_user.first_name}")

bot.infinity_polling()