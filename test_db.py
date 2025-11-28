import os
import sqlite3
from app import create_app

print("🔍 Diagnóstico de la base de datos...")

# Verificar si existe la base de datos
if os.path.exists('consultorio.db'):
    print("✅ consultorio.db existe")
    
    # Conectar y verificar tablas
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    # Obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("📊 Tablas en la base de datos:")
    for table in tables:
        print(f"   - {table[0]}")
    
    conn.close()
else:
    print("❌ consultorio.db NO existe")

# Probar la aplicación Flask
print("\n🚀 Probando la aplicación Flask...")
try:
    app = create_app()
    with app.app_context():
        from models import db
        print("✅ SQLAlchemy configurado correctamente")
        
        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("📊 Tablas creadas por SQLAlchemy:")
        for table in tables:
            print(f"   - {table}")
            
except Exception as e:
    print(f"❌ Error: {e}")