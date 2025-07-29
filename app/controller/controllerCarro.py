from random import sample

from flask import request
from telegram import Bot

from conexionBD import *  #Importando conexion BD
import asyncio
from datetime import datetime, timedelta

def listaProductosxBodega(IdBodega):
        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        
        query ="""  SELECT MateriasPrimas.CodMP,MateriasPrimas.DscNegocio MP, MateriasPrimas.UdeM, MateriasPrimas.TpoInventario 
                            FROM MateriasPrimas 
                                        INNER JOIN 
                                 MateriasPrimasxBodega ON MateriasPrimas.CodMP = MateriasPrimasxBodega.CodMP 
                            WHERE MateriasPrimas.Estado = 0  AND MateriasPrimasxBodega.Estado = 0 AND MateriasPrimasxBodega.CodBod = %s
                            ORDER BY MateriasPrimasxBodega.OrderIngreso ASC
                       """
                        
        
        cursor.execute(query, (IdBodega,))
        resultadoQuery = cursor.fetchall()
        cursor.close() #cerrando conexion de la consulta sql
        conexion_MySQLdb.close() #cerrando conexion de la BD
        
        return resultadoQuery


def guardar_inventario_masivo(inventario,Bodega,Usuario,FechaInv):
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)

         # Preparar una consulta SQL de inserción
        insert_query_Enc = """
        INSERT INTO EncInventario (CodBod,IdFotoPapa,Estado,FechaRegistro,UsuarioRegistro)
        VALUES (%s, %s, %s, %s, %s)
        """
         # Lista para almacenar los valores a insertar
        valores_a_insertar_Enc = []

             # Añadir los valores a la lista
        valores_a_insertar_Enc.append((Bodega, 0, 0,FechaInv,Usuario))
       
        # Ejecutar inserciones en la base de datos
        try:
                # Ejecutar la inserción en lotes para mejorar el rendimiento
                cursor.executemany(insert_query_Enc, valores_a_insertar_Enc)

                last_id = cursor.lastrowid

                insert_query_Dtlle = """
                INSERT INTO DtlleInventario (IdFoto,CodMP,Pquetes,Uds)
                VALUES (%s, %s, %s, %s)
                """
                
                valores_a_insertar_Dtlle = []
               
                # Crear un diccionario para agrupar los datos por producto
                productos_data = {}
                
                for key, value in inventario.items():
                    if 'Paquetes' in key:
                        CodMP = key.split('_')[1]
                        if CodMP not in productos_data:
                            productos_data[CodMP] = {'Paquetes': 0, 'Unidades': 0}
                        productos_data[CodMP]['Paquetes'] = value if value else 0
                    elif 'Unidades' in key:
                        CodMP = key.split('_')[1]
                        if CodMP not in productos_data:
                            productos_data[CodMP] = {'Paquetes': 0, 'Unidades': 0}
                        productos_data[CodMP]['Unidades'] = value if value else 0
                
                # Insertar los datos agrupados
                for CodMP, data in productos_data.items():
                    valores_a_insertar_Dtlle.append((last_id, CodMP, data['Paquetes'], data['Unidades']))

                cursor.executemany(insert_query_Dtlle, valores_a_insertar_Dtlle)

                 # Confirmar los cambios en la base de datos
                conexion_MySQLdb.commit()

                return last_id  
        
        except mysql.connector.Error as err:
                print(f"Error: {err}")
                conexion_MySQLdb.rollback()  # Revertir los cambios en caso de error
                return 0 
        finally:
                # Cerrar el cursor y la conexión
                cursor.close()
                conexion_MySQLdb.close()



# Función para ejecutar la consulta y formatear el mensaje
def InventarioSurtir():

    # Conexión a la base de datos en Railway
    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cursor      = conexion_MySQLdb.cursor()

    crear_tabla_temp = """ 
    CREATE TEMPORARY TABLE TempExistencia 
    (
        CodMP INT,
        Descripcion VARCHAR(100),
        Uds DECIMAL(7, 2),
        Pquetes DECIMAL(10, 2),
        Stock_xSemana DECIMAL(7,2),
        MinxCompra DECIMAL(7,2)
    );
    """
    cursor.execute(crear_tabla_temp)

    Insert_tabla_temp = """ 

    INSERT INTO TempExistencia (CodMP,Descripcion,Uds,Pquetes,Stock_xSemana,MinxCompra)
    SELECT D.CodMP, 
        M.DscNegocio,
        SUM(D.Uds) Uds,
        IF( TpoInventario IN (1,2), SUM(D.Pquetes)*M.MinxCompra,  SUM(D.Pquetes) )Pquetes,
        SUM(MxB.Stock_xSemana)Stock_xSemana, 
        M.MinxCompra
    FROM EncInventario E
            INNER JOIN 
        DtlleInventario D ON E.IdFoto = D.IdFoto
            INNER JOIN 
        MateriasPrimas M ON M.CodMP =  D.CodMP
            INNER JOIN 
        MateriasPrimasxBodega MxB ON MxB.CodMP = D.CodMP AND MxB.CodBod = E.CodBod
    WHERE E.CodBod in (2,4) AND E.Estado = 0
    GROUP BY D.CodMP,M.DscNegocio,M.MinxCompra;

    """
    cursor.execute(Insert_tabla_temp)

    Select_tabla_temp = """ 
        SELECT CodMP,
            Descripcion,
            (Uds+Pquetes)TotalUds,
            Stock_xSemana,
            MinxCompra,
            ((Stock_xSemana - (Uds+Pquetes))/MinxCompra) Falta,
            ROUND(
                CASE 
                WHEN ((Stock_xSemana - (Uds + Pquetes)) / MinxCompra) - FLOOR((Stock_xSemana - (Uds + Pquetes)) / MinxCompra) >= 0.4
                THEN ((Stock_xSemana - (Uds + Pquetes)) / MinxCompra) + 0.1
                ELSE (Stock_xSemana - (Uds + Pquetes)) / MinxCompra
                END
                ) AS Pedir
           # ROUND(((Stock_xSemana - (Uds+Pquetes))/MinxCompra))Pedir
        FROM TempExistencia
    """
    cursor.execute(Select_tabla_temp)

    resultados = cursor.fetchall()

    mensaje = "Productos a pedir:\n\n"
    for row in resultados:
            CodMP, Descripcion,TotalUds,Stock_xSemana,MinxCompra,Falta, Pedir = row

             #print(f"Código MP: {CodMP}, MP: {DscNegocio}, Total Unidades: {TotalUds}, Stoct x Semana: {Stock_xSemana}, MinxCompra: {MinxCompra}, Falta: {Falta}, Pedir: {Pedir}")
            print(f"Código MP: {CodMP}, MP: {Descripcion}, Total Unidades: {TotalUds}, Stoct x Semana: {Stock_xSemana}, MinxCompra: {MinxCompra}, Falta: {Falta}, Pedir: {Pedir}")
            if Pedir is not None and Pedir > 0:                         
                    mensaje += (f" {Pedir} - {Descripcion} \n")
    # Cerrar conexión
    cursor.close()
    conexion_MySQLdb.close

    return mensaje



# Función para ejecutar la consulta y formatear el mensaje
def FotoInventarioxBodega(IdFoto):

    # Conexión a la base de datos en Railway
    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cursor      = conexion_MySQLdb.cursor()

    Select_tabla_temp = """ 
    SELECT 
        M.DscNegocio,
        D.Pquetes,
        D.Uds,  
        B.Nombre,
        E.FechaRegistro,
        E.UsuarioRegistro
    FROM EncInventario E
            INNER JOIN 
        DtlleInventario D ON E.IdFoto = D.IdFoto
            INNER JOIN 
        MateriasPrimas M ON M.CodMP =  D.CodMP
            INNER JOIN 
        BodegasxFranquicia B ON (E.CodBod = B.CodBod)
    WHERE E.IdFoto = %s
    """

    cursor.execute(Select_tabla_temp, (IdFoto,))

    resultados = cursor.fetchall()

    if not resultados:
        cursor.close()
        conexion_MySQLdb.close()
        return "No se encontraron registros para el IdFoto proporcionado."

    mensaje = ""
    primer_registro = resultados[0]
    DscNegocio,Pquetes,Uds,Nombre,FechaRegistro,UsuarioRegistro = primer_registro
    mensaje += (f" {UsuarioRegistro}  con fecha   {FechaRegistro}  hizo inventario de  {Nombre}  \n\n")


    for row in resultados:
            DscNegocio,Pquetes,Uds,Nombre,FechaRegistro,UsuarioRegistro  = row
            mensaje += (f"Pqts: {Pquetes} | Uds: {Uds} - {DscNegocio} \n\n")
    # Cerrar conexión
    cursor.close()
    conexion_MySQLdb.close

    return mensaje



# Función para ejecutar la consulta y formatear el mensaje
def InventarioSurtir_xDia(IdFoto, DiaFtvo):
    # Conexión a la base de datos en Railway
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor()

    crear_tabla_temp = """ 
    CREATE TEMPORARY TABLE TempExistencia 
    (
        CodMP INT,
        Descripcion VARCHAR(100),
        Uds DECIMAL(7, 2),
        Pquetes int,
        MinxConsumo DECIMAL(7,2)
    );
    """
    cursor.execute(crear_tabla_temp)

    Insert_tabla_temp = """ 
    INSERT INTO TempExistencia (CodMP,Descripcion,Uds,Pquetes,MinxConsumo)
    SELECT D.CodMP, 
        M.DscNegocio,
        D.Uds,
        IF( TpoInventario IN (1,2), (D.Pquetes*M.MinxConsumo), D.Pquetes)Pquetes,
        M.MinxConsumo
    FROM EncInventario E
            INNER JOIN 
        DtlleInventario D ON E.IdFoto = D.IdFoto
            INNER JOIN 
        MateriasPrimas M ON M.CodMP =  D.CodMP
    WHERE E.IdFoto = %s
    """
    cursor.execute(Insert_tabla_temp, (IdFoto,))

    Select_tabla_temp = """ 
    SELECT F.CodMP,
        F.Descripcion,
        StockMax_xDiaFtvo,
        StockMax_xDiaNmal,
        (Uds+Pquetes)TotalUds,
        StockMin,
        
        ROUND(
        CASE 
            WHEN %s = 1 
                THEN 
                    CASE 
                        WHEN ((StockMax_xDiaFtvo - (Uds + Pquetes)) / MinxConsumo) - FLOOR((StockMax_xDiaFtvo - (Uds + Pquetes)) / MinxConsumo) >= 0.4 
                             THEN ((StockMax_xDiaFtvo - (Uds + Pquetes)) / MinxConsumo) + 0.1
                        ELSE (StockMax_xDiaFtvo - (Uds + Pquetes)) / MinxConsumo
                    END
                ELSE 
                    CASE 
                        WHEN ((StockMax_xDiaNmal - (Uds + Pquetes)) / MinxConsumo) - FLOOR((StockMax_xDiaNmal - (Uds + Pquetes)) / MinxConsumo) >= 0.4 
                            THEN ((StockMax_xDiaNmal - (Uds + Pquetes)) / MinxConsumo) + 0.1
                        ELSE (StockMax_xDiaNmal - (Uds + Pquetes)) / MinxConsumo
                    END
            END
) AS     Traer
    FROM TempExistencia F
         INNER JOIN 
    MateriasPrimasxBodega MxB ON MxB.CodMP = F.CodMP AND MxB.CodBod = 4 AND CAST( (Uds+Pquetes) AS SIGNED) <= StockMin
    """
    cursor.execute(Select_tabla_temp, (DiaFtvo,))
    
    resultados = cursor.fetchall()

    insertar_sql = """
        INSERT INTO Kardex (TipoMov,CodBod,CodMP,Uds,IdFotoRef,FechaRegistro,UsuarioRegistro)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    mensaje = "Traer:\n\n"
    for row in resultados:
        CodMP, Descripcion,StockMax_xDiaFtvo,StockMax_xDiaNmal,TotalUds, StockMin,Traer = row
             
        print(f"Código MP: {CodMP}, MP: {Descripcion}, Total Unidades: {TotalUds},  StockMax_xDiaFtvo: {StockMax_xDiaFtvo}, StockMax_xDiaNmal: {StockMax_xDiaNmal}, TotalUds: {TotalUds}, Traer: {Traer}")   
        if Traer is not None and Traer > 0:
            #mensaje += f"{Traer} - {Descripcion}- {StockMax_xDiaFtvo}- {StockMax_xDiaNmal}- {TotalUds}- {StockMin}\n"
                # Insertar en tabla real
            cursor.execute(insertar_sql, ("Consumo", 2, CodMP, Traer,IdFoto,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'Sys' ))
            mensaje += f"{Traer} - {Descripcion}\n"

    # Cerrar conexión
    conexion_MySQLdb.commit()
    cursor.close()
    conexion_MySQLdb.close()

    return mensaje





# Función para ejecutar la consulta y formatear el mensaje
def InformeInventario(fecha):
    # Conexión a la base de datos en Railway
     
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    cursor.execute("DELETE FROM InformeInvxDia;")
    conexion_MySQLdb.commit()

    fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
    fecha_actual = fecha_dt.strftime('%Y-%m-%d')
    fecha_dia_anterior = (fecha_dt - timedelta(days=1)).strftime('%Y-%m-%d')


    queries = [
        ("""
        INSERT INTO InformeInvxDia (CodMP,InventarioFinal_DiaAnt,Consumos_Dia,InventarioInicial_Dia,InventarioFinal_Dia)
        SELECT D.CodMP, 0, 0, 0, (D.Uds + D.Pquetes)
        FROM EncInventario E
        INNER JOIN DtlleInventario D ON (E.IdFoto = D.IdFoto)
        WHERE E.CodBod = 2 AND LEFT(E.FechaRegistro, 10) = %s
        """, (fecha_actual,)),

        ("""
        UPDATE InformeInvxDia I
        JOIN (
            SELECT D.CodMP, (D.Uds + D.Pquetes) AS InventarioFinal
            FROM EncInventario E
            INNER JOIN DtlleInventario D ON E.IdFoto = D.IdFoto
            WHERE E.CodBod = 2 AND LEFT(E.FechaRegistro, 10) = %s
        ) AS T ON I.CodMP = T.CodMP
        SET I.InventarioFinal_DiaAnt = T.InventarioFinal
        """, (fecha_dia_anterior,)),

        ("""
        UPDATE InformeInvxDia I
        JOIN (
            SELECT C.CodMP, C.Uds AS Consumo
            FROM EncInventario E
            INNER JOIN Kardex C ON C.IdFotoRef = E.IdFoto
            WHERE C.CodBod = 2 AND LEFT(E.FechaRegistro, 10) = %s
        ) AS T ON I.CodMP = T.CodMP
        SET I.Consumos_Dia = T.Consumo
        """, (fecha_actual,)),

        ("""
        UPDATE InformeInvxDia I
        SET I.InventarioInicial_Dia = I.InventarioFinal_DiaAnt + I.Consumos_Dia
        """, ())
    ]

    # Ejecutar todas las consultas con sus parámetros
    for query, params in queries:
        cursor.execute(query, params)

    # Cerrar conexión
    conexion_MySQLdb.commit()

    cursor.execute("SELECT DscNegocio,InventarioFinal_DiaAnt,Consumos_Dia,InventarioInicial_Dia,InventarioFinal_Dia  FROM InformeInvxDia I INNER JOIN MateriasPrimas M ON I.CodMP =  M.CodMP ")
    resultados = cursor.fetchall()

    cursor.close()
    conexion_MySQLdb.close()

    return resultados


def InformeSaldoInventario(fecha):
    # Conexión a la base de datos en Railway
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    # Limpiar tabla antes de insertar
    cursor.execute("DELETE FROM InformeSaldosInventario;")
    conexion_MySQLdb.commit()

    # Formatear fechas
    fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
    fecha_actual = fecha_dt.strftime('%Y-%m-%d')
    fecha_dia_anterior = (fecha_dt - timedelta(days=1)).strftime('%Y-%m-%d')

    # Consultas SQL a ejecutar
    queries = [
        ("""
        INSERT INTO InformeSaldosInventario (CodMP,CodMPSys,Nombre,InvPreparacion,InvBodega,SaldoActual)
        SELECT Mp.CodMP,Mp.CodMPSys, Mp.DscNegocio, 0, 0, 0        
        FROM MateriasPrimas Mp
        WHERE Mp.Estado = 0
        """, ()),

        ("""
        UPDATE InformeSaldosInventario I
        JOIN (
            SELECT D.CodMP, 
             CASE
                    WHEN Mp.TpoInventario IN (0,2) THEN (D.Uds + D.Pquetes) * Mp.MinxInventario
                    WHEN Mp.TpoInventario IN (1,3) THEN ((D.Pquetes * Mp.MinxInventario) + D.Uds)
            ELSE 0
            END AS InventarioFinal
            FROM EncInventario E
            INNER JOIN DtlleInventario D ON E.IdFoto = D.IdFoto
            INNER JOIN MateriasPrimas Mp ON D.CodMP = Mp.CodMP	
            WHERE E.CodBod = 2 AND DATE(E.FechaRegistro) = %s
        ) AS T ON I.CodMP = T.CodMP
        SET I.InvPreparacion = T.InventarioFinal
        """, (fecha_actual,)),

        ("""
        UPDATE InformeSaldosInventario I
        JOIN (
            SELECT D.CodMP, 
                CASE
                        WHEN Mp.TpoInventario IN (0,2) THEN (D.Uds + D.Pquetes) * Mp.MinxInventario
                        WHEN Mp.TpoInventario IN (1,3) THEN ((D.Pquetes * Mp.MinxInventario) + D.Uds)
                ELSE 0
                END AS InventarioFinal  
            FROM EncInventario E
            INNER JOIN DtlleInventario D ON E.IdFoto = D.IdFoto
            INNER JOIN MateriasPrimas Mp ON D.CodMP = Mp.CodMP	
            WHERE E.CodBod = 4 AND DATE(E.FechaRegistro) = %s
        ) AS T ON I.CodMP = T.CodMP
        SET I.InvBodega = T.InventarioFinal
        """, (fecha_actual,)),

        ("""
        UPDATE InformeSaldosInventario I
        JOIN (
            SELECT CodMP, Saldo
            FROM Saldos 
            WHERE DATE(FechaRegistro) = %s
        ) AS S ON I.CodMPSys = S.CodMP
        SET I.SaldoActual = S.Saldo
        """, (fecha_actual,)),
    ]

    # Ejecutar todas las consultas con sus parámetros
    for query, params in queries:
        cursor.execute(query, params)

    # Obtener resultados
    conexion_MySQLdb.commit()
    cursor.execute("""
        SELECT X.CodMPSys,X.Nombre, X.InvPreparacion , 
              X.InvBodega, 
              X.InvFisico, 
              X.SaldoActual,
              X.Diferencia
        FROM
                (
                select I.CodMPSys, Nombre, 
                        InvPreparacion, 
                        InvBodega,
                        (InvPreparacion + InvBodega) InvFisico, 
                        SaldoActual, 
                        ((InvPreparacion + InvBodega)-SaldoActual) Diferencia, 
                        TpoInventario, 
                        MinxInventario

                from InformeSaldosInventario I 
                inner join MateriasPrimas M ON I.CodMP = M.CodMP
                )X
    """)
    resultados = cursor.fetchall()

    # Cerrar conexión
    cursor.close()
    conexion_MySQLdb.close()

    return resultados



# Función para enviar mensaje a Telegram
async def enviar_mensaje(mensaje):
    TOKEN = '7864913768:AAGT-6Z0sHEgcSgvvGjHyqZBg8WrJsNsJIY'  # Reemplaza con tu token de Telegram
    chat_id = '1174112681'  # Reemplaza con el chat_id del destinatario
    
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=chat_id, text=mensaje)


