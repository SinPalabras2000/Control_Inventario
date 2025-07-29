from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controller.controllerCarro import *


#Para subir archivo tipo foto al servidor
import os
from werkzeug.utils import secure_filename 
from datetime import datetime, timedelta, timezone
import asyncio


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app

# Configurar CORS
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://*.railway.app",
    "https://*.vercel.app"
]
CORS(app, origins=allowed_origins, supports_credentials=True)

msg  =''
tipo =''


#RUTAS

# API REST ENDPOINTS
@app.route('/api/products/<warehouse_id>', methods=['GET'])
def get_products_by_warehouse(warehouse_id):
    try:
        products = listaProductosxBodega(warehouse_id)
        # Transformar los datos para que coincidan con el formato esperado por el frontend
        formatted_products = []
        for product in products:
            # Mapear TpoInventario numérico a string
            tipo_inventario = product['TpoInventario']
            if tipo_inventario == 0:
                type_str = 'Unidades'  # Solo unidades
            elif tipo_inventario == 1:
                type_str = 'Unidades'  # Solo unidades
            elif tipo_inventario == 2:
                type_str = 'Ambos'     # Paquetes y unidades
            else:
                type_str = 'Ambos'     # Por defecto
                
            formatted_products.append({
                'id': product['CodMP'],
                'name': product['MP'],
                'unit': product['UdeM'],
                'type': type_str,
                'inventoryType': tipo_inventario  # Agregamos el tipo numérico original
            })
        return jsonify(formatted_products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory', methods=['POST'])
def save_inventory_api():
    try:
        data = request.get_json()
        warehouse = data.get('warehouse')
        user = data.get('user')
        date = data.get('date')
        items = data.get('items', [])
        
        # Convertir los items al formato esperado por la función existente
        inventory_data = {}
        for item in items:
            product_id = item.get('productId')
            inventory_data[f'Paquetes_{product_id}'] = item.get('packages', 0)
            inventory_data[f'Unidades_{product_id}'] = item.get('units', 0)
            inventory_data[f'opciones_{product_id}'] = item.get('condition', 'bueno')
        
        last_id = guardar_inventario_masivo(inventory_data, warehouse, user, date)
        
        if last_id != 0:
            return jsonify({'success': True, 'message': 'Inventario guardado exitosamente', 'id': last_id})
        else:
            return jsonify({'success': False, 'message': 'Error al guardar el inventario'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory/<date>', methods=['GET'])
def get_inventory_by_date(date):
    try:
        results = InformeInventario(date)
        return jsonify(results if results else [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventory-report/<date>', methods=['GET'])
def get_inventory_report_by_date(date):
    try:
        results = InformeSaldoInventario(date)
        # Formatear los datos para el frontend
        formatted_results = []
        for item in results:
            # Determinar el estado basado en la diferencia
            diferencia = float(item['Diferencia']) if item['Diferencia'] else 0
            if diferencia > 0:
                estado = 'Exceso'
            elif diferencia < 0:
                estado = 'Faltante'
            else:
                estado = 'Correcto'
                
            formatted_results.append({
                'CodMPSys': item['CodMPSys'],
                'CodMP': item['CodMPSys'],  # Usar el mismo valor para compatibilidad
                'Nombre': item['Nombre'],
                'DscNegocio': item['Nombre'],  # Usar el mismo valor para compatibilidad
                'UdeM': 'Unidad',  # Valor por defecto
                'CantidadPaquetes': float(item['InvPreparacion']) if item['InvPreparacion'] else 0,
                'CantidadUnidades': float(item['InvBodega']) if item['InvBodega'] else 0,
                'InvFisico': float(item['InvFisico']) if item['InvFisico'] else 0,
                'SaldoActual': float(item['SaldoActual']) if item['SaldoActual'] else 0,
                'Diferencia': diferencia,
                'Observaciones': estado
            })
        return jsonify(formatted_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Servir archivos estáticos del frontend React
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('static/assets', filename)

# Servir la aplicación React para todas las rutas del frontend
@app.route('/')
@app.route('/inventario')
@app.route('/inventario/<path:path>')
def serve_react_app(path=None):
    return send_file('static/index.html')

@app.route('/api')
def inicio():
    return "API ingrese"

@app.route('/registrar-InventarioxBodega', methods=['POST'])
def addConteoInventario():
    
    if request.method == 'POST':
         Bodega = request.form['Bodega']
         Usuario = request.form['Usuario']
         FechaInv = request.form['FechaInv']
         
         # Determinar el nombre de la bodega
         nombre_bodega = 'Preparación' if Bodega == '2' else 'Bodega' if Bodega == '4' else f'Bodega {Bodega}'
         
         # Crear mensaje para Telegram
         mensaje = f"🚀 INICIO DE INVENTARIO\n\n" \
                  f"👤 Usuario: {Usuario}\n" \
                  f"🏢 Bodega: {nombre_bodega}\n" \
                  f"📅 Fecha: {FechaInv}\n\n" \
                  f"El usuario {Usuario} acaba de comenzar con el inventario en {nombre_bodega} el día {FechaInv}."
         
         # Enviar mensaje a Telegram
         try:
             asyncio.run(enviar_mensaje(mensaje))
         except Exception as e:
             print(f"Error al enviar mensaje a Telegram: {e}")

    return render_template('public/acciones/InventarioxBodega.html',miData = listaProductosxBodega(Bodega),Usuario = Usuario, Bodega = Bodega ,FechaInv = FechaInv )


@app.route('/guardar_inventario', methods=['POST'])
def guardar_inventario():

    if request.method == 'POST':
         Bodega = request.form['Bodega']
         Usuario = request.form['Usuario']
         FechaInv = request.form['FechaInv']
         
     # Crear un diccionario para almacenar los datos del inventario
    inventario = {}

    # Recorrer los elementos enviados en el formulario
    for key in request.form.keys():
        if 'Paquetes' in key or 'Unidades' in key or 'opciones' in key:
            inventario[key] = request.form[key]

    last_id = guardar_inventario_masivo(inventario,Bodega,Usuario,FechaInv)

    if last_id != 0:
    # Llamar a la función para guardar los datos (desde otro archivo .py)
        mensaje = FotoInventarioxBodega(last_id)

         # Enviar el mensaje a Telegram
        asyncio.run(enviar_mensaje(mensaje))

        return render_template('public/layout.html', msg = 'El inventario fue almacenado exitosamente', tipo=1)   
    else:
            # Si hubo un error
        return render_template('public/layout.html', msg='Error al almacenar el inventario. Por favor, inténtelo de nuevo.', tipo=1)



@app.route('/Consultar-InventarioxDia', methods=['GET', 'POST'])
def ConsultaInventarioxDia():
    resultados = None 
    fecha = ''

    if request.method == 'POST':
        fecha = request.form['FechaDiaInv']
        resultados = InformeSaldoInventario(fecha)

    return render_template('public/acciones/InformeInventarioDia.html',miData = resultados,FechaDiaInv=fecha)



#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('inicio'))
    

#if __name__ == "__main__":
 #   app.run(debug=True, port=8000)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)