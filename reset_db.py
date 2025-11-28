# reset_db.py
import os
import shutil
from app import create_app, setup_database
from models.database import db

def reset_database():
    print("🔄 Reiniciando base de datos...")
    
    # Limpiar archivos existentes
    files_to_remove = [
        'instance/consultorio.db',
        '__pycache__',
        'models/__pycache__',
        'controllers/__pycache__',
        'utils/__pycache__'
    ]
    
    for item in files_to_remove:
        if os.path.exists(item):
            if os.path.isfile(item):
                os.remove(item)
                print(f"✅ Eliminado: {item}")
            else:
                shutil.rmtree(item)
                print(f"✅ Eliminado: {item}")
    
    print("✅ Limpieza completada")
    
    # Crear aplicación y configurar BD
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Nueva base de datos creada")
        
        # Crear datos iniciales
        from app import create_initial_data
        create_initial_data()
        
        # Mostrar tablas creadas
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print("📊 Tablas creadas:")
        for table in tables:
            print(f"   - {table}")

if __name__ == "__main__":
    reset_database()