import time
import pandas as pd
from io import StringIO
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def limpiar_decimal(valor):
    if isinstance(valor, str):
        return float(valor.replace('.', '').replace(',', '.'))
    return valor



# ======== CONFIGURACIÓN ========
FECHA_CONSULTA = "2025-07-07"
EMAIL = "fzabala07@gmail.com"
PASSWORD = "Fz199006*"

# Conexión MySQL - REEMPLAZA con tus datos de Railway
conn = mysql.connector.connect(
    host="gondola.proxy.rlwy.net",
    user="root",
    password="vpHvlRYKRWqoUSZWULYplLTymXzoBspd",
    database="railway",
       port=10708  
)
cursor = conn.cursor()


# ======== CONFIGURAR NAVEGADOR ========
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # opcional si no deseas ver la ventana
driver = webdriver.Chrome(options=options)

# ======== LOGIN EN VECTOR POS ========
login_url = f"https://pos.vectorpos.com.co/index.php?r=insumos%2Fsaldos&idSyA=A01071100100001&filtro=0"
driver.get(login_url)

wait = WebDriverWait(driver, 15)
usuario_input = wait.until(EC.presence_of_element_located((By.ID, "txtUser")))
clave_input = driver.find_element(By.ID, "txtPw")

usuario_input.send_keys(EMAIL)
clave_input.send_keys(PASSWORD)
driver.find_element(By.NAME, "yt0").click()

# ======== ESPERAR CARGA DE TABLA DE SALDOS =========
tabla_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-hover"))
)

# ======== EXTRAER HTML DE LA TABLA Y CONVERTIR A DATAFRAME ========
#tabla_html = tabla_element.get_attribute("outerHTML")
#df = pd.read_html(tabla_html)[0]

tabla_html = tabla_element.get_attribute("outerHTML")
df = pd.read_html(StringIO(tabla_html))[0]

print("✅ Tabla obtenida:")
print(df.head())

# ======== INSERTAR EN MYSQL ========
for _, row in df.iterrows():
    # Buscar el código en la tabla de materias primas
    cursor.execute("SELECT CodMPSys FROM MateriasPrimas WHERE DscSys = %s", (row['Nombre'],))
    resultado = cursor.fetchone()

    if resultado:
        id_materia_prima = resultado[0]
        
        cursor.execute("""
            INSERT INTO Saldos (
              CodMP,Nombre,Saldo,FechaRegistro
            ) VALUES (%s, %s, %s, %s)
        """, (
            id_materia_prima,                   # viene de materias_primas
          # 1,
            row['Nombre'],
            limpiar_decimal(row['Saldo Actual']),
            datetime.now()                      # fecha actual en Python
        ))
    #else:
       # print(f"⚠️ No se encontró materia prima para: {row['Nombre']}")

conn.commit()
cursor.close()
conn.close()
driver.quit()
print("✅ Datos insertados exitosamente en Railway 🚀")

