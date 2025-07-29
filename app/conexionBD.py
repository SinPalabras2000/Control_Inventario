
#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector
import os

print ("ingrese")

def connectionBD():
    mydb = mysql.connector.connect(
        host = os.environ.get('DB_HOST', 'mysql.railway.internal'),
        user = os.environ.get('DB_USER', 'root'),
        passwd = os.environ.get('DB_PASSWORD', 'password'),
        database = os.environ.get('DB_NAME', 'railway'),
        port = int(os.environ.get('DB_PORT', '3306'))
        )
    if mydb:
        print ("Conexion exitosa a BD")
        return mydb
    else:
        print("Error en la conexion a BD")
    

    
    
    