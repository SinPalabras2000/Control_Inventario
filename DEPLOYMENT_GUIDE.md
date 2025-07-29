# Guía de Deployment - Sistema de Inventario Integrado

## 🚀 Deployment en Railway (Frontend + Backend Integrado)

Este proyecto ahora incluye tanto el backend Flask como el frontend React en una sola aplicación deployada en Railway.

### Estructura del Proyecto
```
├── app/                    # Backend Flask
│   ├── static/            # Frontend React compilado
│   ├── app.py            # Aplicación Flask principal
│   └── requirements.txt  # Dependencias Python
├── frontend/             # Código fuente React
│   ├── src/
│   ├── package.json
│   └── dist/            # Build compilado
├── railway.json         # Configuración Railway
└── build_and_deploy.py  # Script de build automatizado
```

### Configuración Automática

El proyecto está configurado para:
1. **Build automático**: Railway ejecuta automáticamente el build del frontend
2. **Servir archivos estáticos**: Flask sirve los archivos React desde `/static`
3. **Rutas SPA**: Todas las rutas del frontend redirigen a `index.html`
4. **API endpoints**: Disponibles en `/api/*`

### URLs de la Aplicación

- **Aplicación principal**: `https://tu-app.railway.app/`
- **Página de inventario**: `https://tu-app.railway.app/inventario`
- **API**: `https://tu-app.railway.app/api/*`

### Proceso de Deployment

1. **Commit y Push**:
   ```bash
   git add .
   git commit -m "Update frontend and backend"
   git push origin main
   ```

2. **Railway Build Process**:
   - Instala dependencias del frontend (`npm install`)
   - Compila React (`npm run build`)
   - Copia archivos a `app/static/`
   - Instala dependencias Python
   - Inicia servidor con Gunicorn

### Build Local

Para probar localmente:

```bash
# Opción 1: Script automatizado
python build_and_deploy.py

# Opción 2: Manual
cd frontend
npm install
npm run build
cd ..
python app/app.py
```

### Variables de Entorno Requeridas

En Railway, configura:
- `DATABASE_URL`: URL de la base de datos MySQL
- `PORT`: Puerto del servidor (automático en Railway)
- `FLASK_ENV`: `production`

### Estructura de Rutas

#### Frontend (React)
- `/` → Página principal
- `/inventario` → Sistema de inventario
- `/inventario/*` → Rutas SPA

#### Backend (API)
- `/api` → Status de la API
- `/api/products/<warehouse_id>` → Productos por bodega
- `/api/inventory` → Guardar inventario
- `/api/inventory/<date>` → Consultar inventario
- `/api/inventory-report/<date>` → Reporte de inventario

### Solución de Problemas

#### Error: "Module not found"
- Verificar que `requirements.txt` esté actualizado
- Revisar logs de Railway para errores de build

#### Frontend no se actualiza
- Ejecutar `python build_and_deploy.py` localmente
- Commit y push los cambios en `app/static/`

#### Base de datos no conecta
- Verificar `DATABASE_URL` en variables de entorno
- Revisar configuración de MySQL en Railway

### Desarrollo Local

#### Modo Desarrollo (Separado)
```bash
# Terminal 1: Backend
cd app
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

#### Modo Producción (Integrado)
```bash
python build_and_deploy.py
cd app
python app.py
# Visitar: http://localhost:5000
```

### Ventajas del Deployment Integrado

✅ **Una sola URL**: Frontend y backend en el mismo dominio
✅ **Sin CORS**: No hay problemas de cross-origin
✅ **Simplicidad**: Un solo deployment en Railway
✅ **Costo**: Menor costo que deployments separados
✅ **Velocidad**: Menor latencia entre frontend y backend

### Próximos Pasos

1. Configurar dominio personalizado en Railway
2. Implementar SSL/HTTPS automático
3. Configurar monitoring y logs
4. Optimizar build para producción