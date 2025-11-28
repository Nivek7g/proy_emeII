import os
import subprocess
import sys

def force_recreate():
    print("💥 Forzando recreación completa...")
    
    # Eliminar todo
    files_to_remove = ['consultorio.db']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ Eliminado: {file}")
    
    # Eliminar todos los __pycache__
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                path = os.path.join(root, dir)
                import shutil
                shutil.rmtree(path)
                print(f"✅ Eliminado: {path}")
    
    # Reinstalar dependencias (opcional)
    print("📦 Reinstalando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"])
    
    # Crear nueva aplicación
    from app import create_app
    app = create_app()
    
    print("✅ Recreación completada")
    return app

if __name__ == '__main__':
    app = force_recreate()
    
    # Verificar
    with app.app_context():
        from models import db
        from models.doctor import Doctor
        try:
            count = Doctor.query.count()
            print(f"✅ Consulta a doctores exitosa. Total: {count}")
        except Exception as e:
            print(f"❌ Error en consulta: {e}")