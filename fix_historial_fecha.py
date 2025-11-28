import sqlite3
import os

def fix_historial_fecha():
    print("🔄 Corrigiendo tipo de fecha en historiales_medicos...")
    
    if not os.path.exists('instance/consultorio.db'):
        print("❌ consultorio.db no existe")
        return
    
    conn = sqlite3.connect('consultorio.db')
    cursor = conn.cursor()
    
    try:
        # Verificar la estructura actual
        cursor.execute("PRAGMA table_info(historiales_medicos);")
        columns = cursor.fetchall()
        
        print("📋 Estructura actual de historiales_medicos:")
        for column in columns:
            print(f"   - {column[1]} ({column[2]})")
        
        # Verificar si fecha_consulta es DATE (necesita ser DATETIME)
        fecha_consulta_type = None
        for column in columns:
            if column[1] == 'fecha_consulta':
                fecha_consulta_type = column[2]
                break
        
        if fecha_consulta_type and 'DATE' in fecha_consulta_type.upper():
            print("🔄 Cambiando fecha_consulta de DATE a DATETIME...")
            
            # Crear tabla temporal
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historiales_medicos_temp (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paciente_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    cita_id INTEGER,
                    fecha_consulta DATETIME NOT NULL,
                    peso REAL,
                    altura REAL,
                    presion_arterial TEXT,
                    temperatura REAL,
                    sintomas TEXT NOT NULL,
                    diagnostico TEXT NOT NULL,
                    tratamiento TEXT,
                    medicamentos_recetados TEXT,
                    observaciones TEXT,
                    proxima_cita DATE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Copiar datos
            cursor.execute('''
                INSERT INTO historiales_medicos_temp 
                SELECT * FROM historiales_medicos
            ''')
            
            # Eliminar tabla original
            cursor.execute('DROP TABLE historiales_medicos')
            
            # Renombrar tabla temporal
            cursor.execute('ALTER TABLE historiales_medicos_temp RENAME TO historiales_medicos')
            
            print("✅ fecha_consulta cambiado a DATETIME")
        else:
            print("✅ fecha_consulta ya es DATETIME o no se encontró")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
    
    print("✅ Corrección completada")

if __name__ == '__main__':
    fix_historial_fecha()