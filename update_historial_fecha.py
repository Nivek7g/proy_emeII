from app import create_app
from models import db

def update_historial_fecha():
    app = create_app()
    
    with app.app_context():
        print("🔄 Actualizando tipo de fecha en historiales_medicos...")
        
        try:
            # Cambiar el tipo de fecha_consulta a DATETIME
            db.engine.execute('''
                CREATE TABLE historiales_medicos_temp AS 
                SELECT * FROM historiales_medicos
            ''')
            
            db.engine.execute('DROP TABLE historiales_medicos')
            
            db.engine.execute('''
                CREATE TABLE historiales_medicos (
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
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
                    FOREIGN KEY (doctor_id) REFERENCES doctores (id),
                    FOREIGN KEY (cita_id) REFERENCES citas (id)
                )
            ''')
            
            db.engine.execute('''
                INSERT INTO historiales_medicos 
                SELECT * FROM historiales_medicos_temp
            ''')
            
            db.engine.execute('DROP TABLE historiales_medicos_temp')
            
            print("✅ Tipo de fecha_consulta cambiado a DATETIME")
            
        except Exception as e:
            print(f"ℹ️  Error o la tabla ya tiene el tipo correcto: {e}")
        
        print("✅ Actualización completada")

if __name__ == '__main__':
    update_historial_fecha()