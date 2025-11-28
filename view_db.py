import os
import sqlite3

def view_database():
    db_path = 'instance/consultorio.db'
    
    print(f"📁 Ruta: {os.path.abspath(db_path)}")
    print(f"📏 Tamaño: {os.path.getsize(db_path)} bytes")
    print(f"¿Existe?: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print(f"\n📊 Tablas ({len(tables)}):")
            for table in tables:
                table_name = table[0]
                print(f"  - {table_name}")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    Registros: {count}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    view_database()