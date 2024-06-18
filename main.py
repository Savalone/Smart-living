import telebot
from telebot import types
import serial
import time

#----  CONEXION API TELEGRAM  ------------------------------------------------------------

TOKEN = "6617458988:AAE2hZ3cbwAQqMNpkB796_cfJmBN0PuaIWU"
bot = telebot.TeleBot(TOKEN)
# Configurar la conexión serial con el Flipper Zero
ser = serial.Serial('COM3', 230400, timeout=1)

#---- FUNCIONES ------------------------------------------------------------------------

def send_ir_signal(signal):
    try:
        # Limpiar buffer de entrada/salida
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Enviar comando IR al Flipper Zero
        ser.write(signal.encode())
        time.sleep(2)  # Esperar un poco para asegurarse de que el comando se envíe

        # Leer respuesta
        response = ser.read(ser.in_waiting).decode()
        print("Respuesta del Flipper Zero:", response)
        
        return response
    except Exception as e:
        print("Error enviando la señal IR:", e)
        return None

#---  START  ---------------------------------------------------------------------------

# Funcion para enviar mensajes
@bot.message_handler(commands=['start'])
def send_welcome(message):
    texto = "Bienvenido al proyecto Smart-living!!\n\nEscribe  '/menu'  para ver las opciones disponibles."
    bot.reply_to(message, texto)

#---   MENU    ----------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['menu'])
def send_menu(message):
    menu = "Bienvenido al menu de Smart-living.\n\nFunciones disponibles:\n\n/TV\n/Projector\n/AC\n/Share"
    bot.reply_to(message, menu)

#---  CLEAR  ------------------------------------------------------------------------------------------------------------------------

# Funcion para limpiar la conversacion
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

#--------  CONTROL TV  ----------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['TV'])
def tv_controller(message):
    menu = types.InlineKeyboardMarkup(row_width=2)

    # Agregar botones
    btn_power = types.InlineKeyboardButton('Power', callback_data='Power')
    btn_mute = types.InlineKeyboardButton('Mute', callback_data='Mute')
    btn_chan_up = types.InlineKeyboardButton('▲', callback_data='Chan_up')
    btn_chan_down = types.InlineKeyboardButton('▼', callback_data='Chan_down')
    btn_vol_up = types.InlineKeyboardButton('+', callback_data='Vol_up')
    btn_vol_down = types.InlineKeyboardButton('-', callback_data='Vol_down')

    # Agrega los botones al menu
    menu.add(btn_power, btn_mute, btn_chan_up, btn_vol_up, btn_chan_down, btn_vol_down)
    bot.send_message(message.chat.id, "Control remoto del Televisor", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Power':
        tv_signal = "ir universal tv Power\r"
        send_ir_signal(tv_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón Power")
    elif call.data == 'Mute':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón Mute")
        tv_signal = "ir universal tv Mute\r"
        send_ir_signal(tv_signal)
    elif call.data == 'Chan_up':
        tv_signal = "ir universal tv Ch_next\r"
        send_ir_signal(tv_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de subir canal")
    elif call.data == 'Chan_down':
        tv_signal = "ir universal tv Ch_prev\r"
        send_ir_signal(tv_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de bajar canal")
    elif call.data == 'Vol_up':
        tv_signal = "ir universal tv Vol_up\r"
        send_ir_signal(tv_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de subir volumen")
    elif call.data == 'Vol_down':
        tv_signal = "ir universal tv Vol_dn\r"
        send_ir_signal(tv_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de bajar volumen")

#------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    bot.polling(none_stop=True)
