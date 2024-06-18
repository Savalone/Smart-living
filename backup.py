import telebot, subprocess, time, os, pyautogui
from telebot import types


TOKEN = "6617458988:AAE2hZ3cbwAQqMNpkB796_cfJmBN0PuaIWU"
bot = telebot.TeleBot(TOKEN)

# Funcion para enviar mensajes
@bot.message_handler(commands=['start'])
def send_welcome(message):
    texto = "Bienvenido al proyecto Smart-living!!\n\nEscribe '/menu' para ver las opciones disponibles."
    bot.reply_to(message, texto)


# Se establece que el mensaje enviado es de tipo str
#@bot.message_handler(func=lambda message: True)
#def echo_message(message):
#    bot.reply_to(message, message.text)

# Funcion para agregar un menu con botones


@bot.message_handler(commands=['clear'])
def clear_conversation(message):
    chat_id = message.chat.id
    message_id = message.message_id

    # Definir cuántos mensajes recientes quieres intentar eliminar
    num_messages_to_delete = 100

    # Intentar eliminar los mensajes recientes
    for i in range(num_messages_to_delete):
        try:
            bot.delete_message(chat_id, message_id - i)
        except telebot.apihelper.ApiException as e:
            print(f"Error al eliminar el mensaje {message_id - i}: {e}")
    
    bot.reply_to(message, "La conversación ha sido limpiada.")


@bot.message_handler(commands=['Aire'])
def control_aire(message):
   
    # Crea el menu
    menu = types.InlineKeyboardMarkup(row_width=2)

    # Agregar los botones del menu
    btn_on = types.InlineKeyboardButton('On', callback_data='Encender')
    btn_off = types.InlineKeyboardButton('off', callback_data='off')

    # Agrega ambos botones al menu
    menu.add(btn_on, btn_off)

    # Envia el menu
    bot.send_message(message.chat.id, "Control remoto del aire acondicionado", reply_markup=menu)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == "Encender":
        
        bot.answer_callback_query(call.id, "Aire encendido!")
    if call.data == "off": 
        
        bot.answer_callback_query(call.id, "Aire apagado!")
        

@bot.message_handler(commands=['Tv'])
def control_tv(message):

    # crear menu
    menu = types.InlineKeyboardMarkup(row_width=1)

    # Agregar botones
    btn_power = types.InlineKeyboardButton('Power', callback_data='Power')
    btn_mute = types.InlineKeyboardButton('Mute', callback_data='Mute')

    # Agrega los botones al menu
    menu.add(btn_power, btn_mute)

    # Envia el menu
    bot.send_message(message.chat.id, "Control remoto del Televisor", reply_markup=menu)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data == "Power":
        pyautogui.write("ir universal tv Power")
        pyautogui.press('ENTER')
        bot.answer_callback_query(call.id, "Senal enviada!!")



if __name__ == "__main__":
    bot.polling(none_stop=True)