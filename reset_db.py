import os
import shutil
import sqlite3

def reset_database():
    print("🔄 Reiniciando base de datos...")
    
    # Eliminar archivos de base de datos
    db_files = ['consultorio.db', 'instance/consultorio.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Eliminado: {db_file}")
        else:
            print(f"ℹ️  No encontrado: {db_file}")
    
    # Eliminar cache
    cache_dirs = ['__pycache__', 'models/__pycache__', 'controllers/__pycache__', 'utils/__pycache__']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
            print(f"✅ Eliminado: {cache_dir}")
        else:
            print(f"ℹ️  No encontrado: {cache_dir}")
    
    print("✅ Limpieza completada")
    
    # Crear nueva base de datos usando el método correcto
    try:
        from app import create_app, setup_database
        app = create_app()
        setup_database(app)
        print("✅ Nueva base de datos creada exitosamente")
        
        # Verificar tablas
        with app.app_context():
            from models import db
            from sqlalchemy import inspect
            
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("📊 Tablas en la base de datos:")
            for table in tables:
                print(f"   - {table}")
                
    except Exception as e:
        print(f"❌ Error al crear base de datos: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = reset_database()
    if success:
        print("\n🎉 Base de datos reiniciada correctamente!")
        print("🚀 Ahora puedes ejecutar: python app.py")
    else:
        print("\n💥 Hubo un error al reiniciar la base de datos")