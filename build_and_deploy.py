#!/usr/bin/env python3
"""
Script para construir el frontend React y prepararlo para deployment en Railway
"""

import os
import subprocess
import shutil
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ Error ejecutando: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def main():
    # Obtener el directorio del proyecto
    project_dir = Path(__file__).parent
    frontend_dir = project_dir / "frontend"
    app_dir = project_dir / "app"
    static_dir = app_dir / "static"
    
    print("🚀 Iniciando build del frontend React...")
    
    # Cambiar al directorio del frontend
    os.chdir(frontend_dir)
    
    # Instalar dependencias
    print("📦 Instalando dependencias del frontend...")
    run_command("npm install --legacy-peer-deps")
    
    # Construir el frontend
    print("🔨 Construyendo el frontend...")
    run_command("npm run build")
    
    # Limpiar directorio static anterior
    if static_dir.exists():
        print("🧹 Limpiando directorio static anterior...")
        shutil.rmtree(static_dir)
    
    # Crear directorio static
    static_dir.mkdir(exist_ok=True)
    
    # Copiar archivos del build
    print("📁 Copiando archivos del build...")
    dist_dir = frontend_dir / "dist"
    
    if dist_dir.exists():
        for item in dist_dir.iterdir():
            if item.is_dir():
                shutil.copytree(item, static_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, static_dir)
        print("✅ Archivos copiados exitosamente")
    else:
        print("❌ No se encontró el directorio dist")
        sys.exit(1)
    
    print("🎉 Build completado exitosamente!")
    print("📋 Archivos listos para deployment en Railway")
    print(f"📂 Archivos estáticos en: {static_dir}")
    
    # Mostrar instrucciones para Railway
    print("\n📝 Para deployar en Railway:")
    print("1. Commit y push los cambios a tu repositorio")
    print("2. Railway detectará automáticamente los cambios")
    print("3. La aplicación se rebuildeará con el frontend integrado")

if __name__ == "__main__":
    main()