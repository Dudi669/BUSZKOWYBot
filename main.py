import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6998345138

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# Start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("💎 Kryształ", "🥦 Buch")
    bot.send_message(message.chat.id, "Wybierz produkt / Choose product:", reply_markup=markup)

# Produkt
@bot.message_handler(func=lambda m: m.text in ["💎 Kryształ", "🥦 Buch"])
def choose_quantity(message):
    user_data[message.chat.id] = {'produkt': message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("1", "2", "3", "5")
    bot.send_message(message.chat.id, "Ile sztuk? / How many?", reply_markup=markup)

# Ilość
@bot.message_handler(func=lambda m: m.text in ["1", "2", "3", "5"])
def choose_delivery(message):
    if message.chat.id in user_data:
        user_data[message.chat.id]['ilosc'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🏠 Dowóz", "🏪 Stacjonarnie")
    bot.send_message(message.chat.id, "Wybierz sposób odbioru / Delivery method:", reply_markup=markup)

# Sposób odbioru
@bot.message_handler(func=lambda m: m.text in ["🏠 Dowóz", "🏪 Stacjonarnie"])
def finalize(message):
    if message.chat.id in user_data:
        user_data[message.chat.id]['odbior'] = message.text
        produkt = user_data[message.chat.id]['produkt']
        ilosc = user_data[message.chat.id]['ilosc']
        odbior = message.text

        if odbior == "🏪 Stacjonarnie":
            odbior += "\nBywam w różnych miejscach – pisz na @mordeczka420"
            bot.send_message(message.chat.id, "Bywam w różnych miejscach – pisz bezpośrednio na @mordeczka420")
            uwagi = "Brak"
            address = "Stacjonarnie"
        else:
            msg = bot.send_message(message.chat.id, "Podaj adres dostawy / Send delivery address:")
            bot.register_next_step_handler(msg, lambda m: finish_order(m, produkt, ilosc, m.text))

        if odbior == "🏪 Stacjonarnie":
            finish_order(message, produkt, ilosc, "Stacjonarnie – @mordeczka420")

def finish_order(message, produkt, ilosc, adres):
    zamowienie = f"""
🛒 Nowe zamówienie:
👤 Użytkownik: @{message.from_user.username or 'brak'} ({message.chat.id})
🧪 Produkt: {produkt}
📦 Ilość: {ilosc}
🚚 Odbiór: {adres}
    """
    bot.send_message(message.chat.id, "✅ Zamówienie przyjęte! / Order confirmed.")
    bot.send_message(ADMIN_ID, zamowienie)

bot.infinity_polling()