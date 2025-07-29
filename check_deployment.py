#!/usr/bin/env python3
"""
Script para verificar que el proyecto esté listo para el despliegue en Railway
"""

import os
import sys

def check_files():
    """Verifica que todos los archivos necesarios existan"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'railway.json',
        'app/app.py',
        'app/conexionBD.py',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Todos los archivos necesarios están presentes")
        return True

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import flask
        print("✅ Dependencias principales instaladas (Flask disponible)")
        return True
    except ImportError:
        print("❌ Flask no está instalado")
        return False

def check_environment():
    """Verifica las variables de entorno"""
    env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT']
    missing_vars = []
    
    for var in env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Variables de entorno no configuradas (se usarán valores por defecto):")
        for var in missing_vars:
            print(f"   - {var}")
    else:
        print("✅ Variables de entorno configuradas")
    
    return True

def main():
    print("🚀 Verificando configuración para despliegue en Railway...\n")
    
    checks = [
        check_files(),
        check_dependencies(),
        check_environment()
    ]
    
    if all(checks):
        print("\n🎉 ¡El proyecto está listo para desplegarse en Railway!")
        print("\n📋 Próximos pasos:")
        print("1. Sube el código a un repositorio Git")
        print("2. Conecta el repositorio a Railway")
        print("3. Configura las variables de entorno en Railway")
        print("4. ¡Disfruta tu aplicación desplegada!")
    else:
        print("\n❌ Hay problemas que resolver antes del despliegue")
        sys.exit(1)

if __name__ == "__main__":
    main()