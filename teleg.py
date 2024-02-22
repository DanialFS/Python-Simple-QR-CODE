import config
import telebot
import qrcode
from telebot import types

qr_function = False

def generate_qr_code(word):
    content = word
    qr = qrcode.make(content)
    qr.save("last_qr_code.png")

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start','back'])
def start_message(message):
    global qr_function
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup(row_width=2)

    bot.send_message(message.chat.id, f"Привет, {user_name} 👊")
    bot.send_message(message.chat.id, "Я предназначен для создания QR-кодов 😎")

    button1 = types.InlineKeyboardButton("Создать QR-Код", callback_data='button1')
    button2 = types.InlineKeyboardButton("Выйти из программы", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global qr_function
    if call.data == 'button1':
        bot.answer_callback_query(call.id, text="Введите ссылку или слово, для которого нужно создать QR-Код")
        qr_function = True
    elif call.data == 'button2':
        bot.answer_callback_query(call.id, text="До скорой встречи, для того чтобы вернуться - /back")

@bot.message_handler(func=lambda message: qr_function)
def handle_qr_code_request(message):
    global qr_function
    user_request = message.text
    if user_request == '/stop':
        qr_function = False
    bot.send_message(message.chat.id, f"QR-Код для вашего текста: {message.text}")
    generate_qr_code(user_request)
    with open('D:/Visual Studio(Code)/Python/TelegramBotQr/last_qr_code.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
bot.infinity_polling()
