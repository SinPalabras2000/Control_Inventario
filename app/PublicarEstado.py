import os
import tkinter as tk
import time
import threading
import requests
from datetime import datetime

# ========== CONFIGURACIÓN ==========

INTERVALO_MINUTOS = 2  # Intervalo entre recordatorios

TELEGRAM_BOT_TOKEN = '7864913768:AAGT-6Z0sHEgcSgvvGjHyqZBg8WrJsNsJIY'
TELEGRAM_CHAT_ID = '1174112681'

# ========== FUNCIONES ==========

def enviar_mensaje_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    try:
        requests.post(url, data=payload)
        print("✅ Mensaje enviado a Telegram.")
    except Exception as e:
        print("❌ Error enviando mensaje:", e)

def mostrar_recordatorio():
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕒 Mostrando recordatorio a las {hora}")

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='black')

    label = tk.Label(
        root,
        text="📢 Es hora de publicar un estado en WhatsApp del negocio.\nPor favor hazlo antes de continuar usando el PC.",
        font=('Arial', 24),
        fg='white',
        bg='black'
    )
    label.pack(expand=True)

    def cerrar():
        root.destroy()
        enviar_mensaje_telegram(f"✅ Estado publicado a las {datetime.now().strftime('%H:%M:%S')}")

    btn = tk.Button(root, text="Ya publiqué", font=('Arial', 16), command=cerrar)
    btn.pack(pady=20)

    root.mainloop()

def iniciar_recordatorios():
    while True:
        mostrar_recordatorio()
        time.sleep(INTERVALO_MINUTOS * 60)

# ========== INICIO ==========

if __name__ == "__main__":
    threading.Thread(target=iniciar_recordatorios).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("⛔ Programa detenido manualmente.")
