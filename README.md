# Sistema de Control de Inventario - Sin Palabras la 2000

Sistema web para el control y gestión de inventarios con backend en Flask y frontend en React.

## 🚀 Despliegue en Railway

### Prerrequisitos
- Cuenta en [Railway](https://railway.app)
- Repositorio Git con el código del proyecto

### Pasos para el despliegue

1. **Conectar repositorio a Railway:**
   - Ve a [Railway](https://railway.app) e inicia sesión
   - Haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

2. **Configurar variables de entorno:**
   En el dashboard de Railway, ve a la sección "Variables" y configura:
   ```
   DB_HOST=gondola.proxy.rlwy.net
   DB_USER=root
   DB_PASSWORD=vpHvlRYKRWqoUSZWULYplLTymXzoBspd
   DB_NAME=railway
   DB_PORT=10708
   FLASK_ENV=production
   ```

3. **El despliegue se realizará automáticamente** usando:
   - `railway.json` para la configuración
   - `Procfile` para el comando de inicio
   - `requirements.txt` para las dependencias

### 🔧 Estructura del proyecto

```
├── app/                    # Backend Flask
│   ├── app.py             # Aplicación principal
│   ├── conexionBD.py      # Configuración de base de datos
│   └── controller/        # Controladores
├── frontend/              # Frontend React
│   ├── src/               # Código fuente
│   └── public/            # Archivos estáticos
├── requirements.txt       # Dependencias Python
├── Procfile              # Comando de inicio para Railway
├── railway.json          # Configuración de Railway
└── .env.example          # Variables de entorno de ejemplo
```

### 📱 Funcionalidades

- ✅ Registro de inventario por bodega
- ✅ Consulta de inventarios por fecha
- ✅ Gestión de productos y unidades
- ✅ Interfaz responsive para móviles
- ✅ API REST para integración

### 🛠️ Desarrollo local

**Backend:**
```bash
cd app
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 🌐 URLs de la aplicación

- **Backend API:** `https://tu-app.railway.app/api/`
- **Frontend:** Se puede desplegar por separado en Vercel/Netlify

### 📞 Soporte

Para soporte técnico, contacta al equipo de desarrollo.
