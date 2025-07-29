from telegram import Bot
import asyncio
from controller.controllerCarro import *

import schedule
import time
import random
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Función principal para ejecutar todo el flujo
async def ejecutar_flujo_1():
    # Obtener los resultados de la consulta
    mensaje = InventarioSurtir()
    
    # Si el mensaje no está vacío, enviarlo a Telegram
    if mensaje.strip() != "Productos a pedir:\n":
        await enviar_mensaje(mensaje)


async def ejecutar_flujo_2(IdFoto,DiaFtvo):
    # Obtener los resultados de la consulta
    mensaje = InventarioSurtir_xDia(IdFoto,DiaFtvo)
    
    # Si el mensaje no está vacío, enviarlo a Telegram
    if mensaje.strip() != "Traer:\n":
       await enviar_mensaje(mensaje)
    #print(mensaje)

# Ejecutar el flujo
#asyncio.run(ejecutar_flujo_1())
asyncio.run(ejecutar_flujo_2(7,0))




TOKEN = '7864913768:AAGT-6Z0sHEgcSgvvGjHyqZBg8WrJsNsJIY'
bot = Bot(token=TOKEN)
CHAT_ID = '1174112681'  # Reemplaza con el chat ID del destinatario


'''
# Autenticación con Google Sheets
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("ChainCartBot.json", scope)
    client = gspread.authorize(creds)
    return client

# Cargar el contenido desde Google Sheets
def cargar_contenido():
    client = conectar_google_sheets()
    sheet = client.open("Material_GrupoTelegram")  # Cambia con el nombre de tu archivo en Google Sheets

    # Lee los datos de cada hoja
    Imagen = [row[0] for row in sheet.worksheet("Imagenes").get_all_values()]
    texto = [row[0] for row in sheet.worksheet("TipsFinancieros").get_all_values()]
    video = [row[0] for row in sheet.worksheet("VideosInteres").get_all_values()]
    audio = [row[0] for row in sheet.worksheet("Audios").get_all_values()]

    return {
        "Imagen": Imagen,
        "texto": texto,
        "video": video,
        "audio": audio
    }

# Cargar el contenido dinámico
contenido = cargar_contenido()

mensaje_Foto = "🚀"
mensaje_Video = "🚀"

# Funciones que envían contenido aleatorio
async def enviar_Imagen():
   url_imagen = random.choice(contenido["Imagen"])
   try:
    await bot.send_photo(chat_id=CHAT_ID, photo=url_imagen, caption=mensaje_Foto)
   except Exception as e:
        print(f"Error al enviar la imagen: {e}")


async def enviar_texto():
    mensaje = random.choice(contenido["texto"])
    await bot.send_message(chat_id=CHAT_ID, text=mensaje)


async def enviar_video():
    url_video = random.choice(contenido["video"])
    try:
        await bot.send_video(chat_id=CHAT_ID, video=url_video, caption=mensaje_Video)
    except Exception as e:
        print(f"Error al enviar el video: {e}")


async def enviar_audio():
    url_audio = random.choice(contenido["audio"])
    try:
        await bot.send_audio(chat_id=CHAT_ID, audio=url_audio, caption="🎶 Aquí tienes un audio especial para ti.")
    except Exception as e:
        print(f"Error al enviar el audio: {e}")


async def enviar_encuesta():
    encuestas = cargar_encuestas()  # Cargar las encuestas desde Google Sheets
    pregunta, opciones = random.choice(encuestas)  # Seleccionar una encuesta aleatoriamente

    await bot.send_poll(chat_id=CHAT_ID, question=pregunta, options=opciones)


def cargar_encuestas():
    client = conectar_google_sheets()
    sheet = client.open("Material_GrupoTelegram")  # Cambia con el nombre de tu archivo en Google Sheets

    # Leer las preguntas y opciones
    datos = sheet.worksheet("Encuestas").get_all_values()  # Esto obtiene todas las filas
    encuestas = []

    for fila in datos[1:]:  # Asumiendo que la primera fila es de encabezados
        pregunta = fila[0]  # Suponiendo que la pregunta está en la primera columna
        opciones = fila[1:]  # Las opciones están en las siguientes columnas
        encuestas.append((pregunta, opciones))
    
    return encuestas


# Función principal que se ejecuta en el bucle de eventos
async def main():
    # Programar los envíos
    #schedule.every().day.at("11:35").do(lambda: asyncio.create_task(enviar_audio()))
    #schedule.every().day.at("11:05").do(lambda: asyncio.create_task(enviar_video()))
    #schedule.every().day.at("11:06").do(lambda: asyncio.create_task(enviar_texto()))
    #schedule.every().day.at("11:07").do(lambda: asyncio.create_task(enviar_Imagen()))
    schedule.every().day.at("11:56").do(lambda: asyncio.create_task(enviar_encuesta()))

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Espera un minuto entre verificaciones

# Ejecutar el bucle de eventos
#asyncio.run(main())
'''