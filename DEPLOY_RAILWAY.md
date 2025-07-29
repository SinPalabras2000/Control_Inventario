# 🚀 Guía de Despliegue en Railway

## ✅ Estado del Proyecto
Tu proyecto está **LISTO** para desplegarse en Railway. Todos los archivos de configuración han sido creados y las dependencias están instaladas.

## 📋 Pasos para Desplegar

### 1. Preparar el Repositorio Git
```bash
# Si no tienes git inicializado
git init
git add .
git commit -m "Preparar proyecto para despliegue en Railway"

# Subir a GitHub/GitLab
git remote add origin <URL_DE_TU_REPOSITORIO>
git push -u origin main
```

### 2. Conectar a Railway
1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con GitHub/GitLab
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige tu repositorio

### 3. Configurar Variables de Entorno
En el dashboard de Railway, ve a la pestaña "Variables" y agrega:

```
DB_HOST=tu_host_de_base_de_datos
DB_USER=tu_usuario_de_bd
DB_PASSWORD=tu_contraseña_de_bd
DB_NAME=tu_nombre_de_bd
DB_PORT=3306
FLASK_ENV=production
```

### 4. Configurar Base de Datos
Puedes usar:
- **Railway MySQL**: Agrega un servicio MySQL desde el dashboard
- **Base de datos externa**: Configura las variables con tus credenciales

## 📁 Archivos de Configuración Creados

- ✅ `Procfile` - Comando de inicio para Railway
- ✅ `railway.json` - Configuración específica de Railway
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `.env.example` - Plantilla de variables de entorno
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ `README.md` - Documentación del proyecto

## 🔧 Configuraciones Aplicadas

### Backend (Flask)
- ✅ CORS configurado para dominios de Railway y Vercel
- ✅ Variables de entorno para base de datos
- ✅ Gunicorn como servidor WSGI

### Estructura del Proyecto
```
├── app/
│   ├── app.py              # Aplicación Flask principal
│   ├── conexionBD.py       # Configuración de BD con variables de entorno
│   └── requirements.txt    # Dependencias (corregido)
├── frontend/               # Aplicación React
├── Procfile               # Comando de inicio
├── railway.json           # Configuración Railway
├── requirements.txt       # Dependencias principales
└── .env.example          # Plantilla de variables
```

## 🌐 URLs Esperadas
Después del despliegue:
- **Backend API**: `https://tu-app.railway.app`
- **Frontend**: Despliega por separado en Vercel/Netlify

## 🔍 Verificación Post-Despliegue
1. Verifica que la API responda: `https://tu-app.railway.app/productos`
2. Revisa los logs en Railway si hay errores
3. Confirma la conexión a la base de datos

## 🆘 Solución de Problemas

### Error de Conexión a BD
- Verifica las variables de entorno
- Confirma que la BD esté accesible desde Railway

### Error 500
- Revisa los logs en Railway
- Verifica que todas las dependencias estén en `requirements.txt`

### CORS Errors
- Actualiza la configuración CORS en `app.py` con tu dominio de frontend

---

¡Tu proyecto está listo para conquistar la nube! 🚀