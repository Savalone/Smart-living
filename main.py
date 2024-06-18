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
    img_url = "https://thesustainabilist.ae/wp-content/uploads/2018/07/smart4.jpg"
    texto = "Bienvenido al proyecto Smart-living!!\n\n\nFunciones disponibles:\n\n/TV\n/Projector\n/AC\n/Clear"
    imagen = bot.send_photo(chat_id=message.chat.id, photo=img_url, caption=texto)
    bot.reply_to(message, imagen)

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
    
    elif call.data == 'Mute':
        tv_signal = "ir universal tv Mute\r"
        send_ir_signal(tv_signal)
    
    elif call.data == 'Chan_up':
        tv_signal = "ir universal tv Ch_next\r"
        send_ir_signal(tv_signal)
    
    elif call.data == 'Chan_down':
        tv_signal = "ir universal tv Ch_prev\r"
        send_ir_signal(tv_signal)
       
    elif call.data == 'Vol_up':
        tv_signal = "ir universal tv Vol_up\r"
        send_ir_signal(tv_signal)
        
    elif call.data == 'Vol_down':
        tv_signal = "ir universal tv Vol_dn\r"
        send_ir_signal(tv_signal)
        

#----  Air Conditioner   --------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['AC'])
def tv_controller(message):
    menu = types.InlineKeyboardMarkup(row_width=2)

    # Agregar botones
    btn_power = types.InlineKeyboardButton('Power', callback_data='Power')
    btn_max = types.InlineKeyboardButton('Max', callback_data='Max')
    btn_min = types.InlineKeyboardButton('Min', callback_data='Min')

    # Agrega los botones al menu
    menu.add(btn_max, btn_min, btn_power)
    bot.send_message(message.chat.id, "Control remoto del Aire acondicionado", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Power':
        ac_signal = "ir universal ac Off\r"
        send_ir_signal(ac_signal)
    
    elif call.data == 'Max':
        ac_signal = "ir universal ac Cool_hi\r"
        send_ir_signal(ac_signal)
    
    elif call.data == 'Min':
        ac_signal = "ir universal ac Cool_lo\r"
        send_ir_signal(ac_signal)
    

#---  Projectors  -----------------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['Projector'])
def tv_controller(message):
    menu = types.InlineKeyboardMarkup(row_width=2)

    # Agregar botones
    btn_power = types.InlineKeyboardButton('Power', callback_data='Power')
    btn_Mute = types.InlineKeyboardButton('Mute', callback_data='Mute')
    btn_Vol_down = types.InlineKeyboardButton('-', callback_data='Vol_down')
    btn_Vol_up = types.InlineKeyboardButton('+', callback_data='Vol_up')
    
    # Agrega los botones al menu
    menu.add(btn_power, btn_Mute, btn_Vol_down, btn_Vol_up)
    bot.send_message(message.chat.id, "Control remoto del Proyector", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Power':
        pr_signal = "ir universal projector Power\r"
        send_ir_signal(pr_signal)
    
    elif call.data == 'Mute':
        pr_signal = "ir universal projector Mute\r"
        send_ir_signal(pr_signal)
    
    elif call.data == 'Vol_down':
        pr_signal = "ir universal projector Vol_down\r"
        send_ir_signal(pr_signal)

    elif call.data == 'Vol_up':
        pr_signal = "ir universal projector Vol_up\r"
        send_ir_signal(pr_signal)

#--------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    bot.polling(none_stop=True)
