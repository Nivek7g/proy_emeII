# check_db.py
import os
import sqlite3
from pathlib import Path

def check_database_structure():
    print("📍 Verificando estructura de la base de datos...")
    
    # Rutas posibles donde podría estar la base de datos
    possible_paths = [
        'instance/consultorio.db',
        './instance/consultorio.db',
        'consultorio.db',
        './consultorio.db'
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            print(f"✔ Base de datos encontrada en: {path}")
            break
    
    if not db_path:
        print("✕ No se encontró la base de datos en ninguna ubicación esperada")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"✔ Conexión exitosa a {db_path}")
        print(f"📊 Tablas encontradas ({len(tables)}):")
        
        for table in tables:
            table_name = table[0]
            print(f"   - {table_name}")
            
            # Obtener estructura de cada tabla
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"     Columnas: {len(columns)}")
            for col in columns:
                print(f"       • {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"✕ Error al conectar con la base de datos: {e}")
        return False

if __name__ == "__main__":
    check_database_structure()