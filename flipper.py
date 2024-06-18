import telebot
from telebot import types
import serial
import time

# Reemplaza 'YOUR_API_KEY' con el token de tu bot
bot = telebot.TeleBot('6617458988:AAE2hZ3cbwAQqMNpkB796_cfJmBN0PuaIWU')

# Configurar la conexión serial con el Flipper Zero
ser = serial.Serial('COM3', 230400, timeout=1)

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

    # Agregar los botones al menú
    menu.add(btn_power, btn_mute, btn_chan_up, btn_vol_up, btn_chan_down, btn_vol_down)

    # Enviar el menú al usuario
    bot.send_message(message.chat.id, "Controla tu TV:", reply_markup=menu)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Power':
        tv_power_signal = "ir universal tv Power\r"
        send_ir_signal(tv_power_signal)
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón Power. Respuesta del Flipper Zero: ")
    elif call.data == 'Mute':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón Mute")
    elif call.data == 'Chan_up':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de subir canal")
    elif call.data == 'Chan_down':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de bajar canal")
    elif call.data == 'Vol_up':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de subir volumen")
    elif call.data == 'Vol_down':
        bot.send_message(call.message.chat.id, "Ha sido presionado el botón de bajar volumen")

bot.infinity_polling()

# Cerrar la conexión serial al finalizar
ser.close()
