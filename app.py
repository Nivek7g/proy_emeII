from flask import Flask
from config import Config
from models.database import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, template_folder='views')
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_controller.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints PRIMERO
    try:
        from controllers.auth_controller import bp as auth_bp
        from controllers.dashboard_controller import bp as dashboard_bp
        from controllers.pacientes_controller import bp as pacientes_bp
        from controllers.doctores_controller import bp as doctores_bp
        from controllers.citas_controller import bp as citas_bp
        from controllers.historiales_controller import bp as historiales_bp
        from controllers.usuarios_controller import bp as usuarios_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
        app.register_blueprint(doctores_bp, url_prefix='/doctores')
        app.register_blueprint(citas_bp, url_prefix='/citas')
        app.register_blueprint(historiales_bp, url_prefix='/historiales')
        app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
        
    except ImportError as e:
        print(f"⚠️  Algunos controladores no están implementados: {e}")
    
    return app

def setup_database(app):
    """Configurar la base de datos y crear datos iniciales"""
    with app.app_context():
        # Importar modelos DENTRO del contexto para evitar importaciones circulares
        from models.user import User
        from models.patient import Patient
        from models.doctor import Doctor
        from models.appointment import Appointment
        from models.medical_record import MedicalRecord
        from models.prescription import Prescription
        from models.specialty import Especialidad
        from models.schedule import HorarioDoctor
        from models.medication import Medicamento
        from models.payment import Pago
        
        # Crear todas las tablas
        db.create_all()
        create_initial_data()

def create_initial_data():
    from models.user import User
    from models.doctor import Doctor
    from models.specialty import Especialidad
    
    # Crear especialidades si no existen
    if Especialidad.query.count() == 0:
        especialidades = [
            Especialidad(nombre="Cardiología", descripcion="Enfermedades del corazón"),
            Especialidad(nombre="Pediatría", descripcion="Medicina para niños"),
            Especialidad(nombre="Dermatología", descripcion="Enfermedades de la piel"),
            Especialidad(nombre="Ginecología", descripcion="Salud femenina"),
            Especialidad(nombre="Ortopedia", descripcion="Enfermedades óseas y musculares")
        ]
        db.session.add_all(especialidades)
        db.session.commit()
        print("✅ Especialidades creadas")
    
    # Crear usuario admin si no existe
    if not User.query.filter_by(usuario='admin').first():
        admin = User(
            usuario='admin',
            correo='admin@consultorio.com',
            celular='77712345',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Crear doctor de ejemplo
        doctor_user = User(
            usuario='drgarcia',
            correo='drgarcia@consultorio.com',
            celular='77754321',
            rol='doctor'
        )
        doctor_user.set_password('doctor123')
        db.session.add(doctor_user)
        
        db.session.commit()
        
        # Asignar doctor (usando la primera especialidad)
        primera_especialidad = Especialidad.query.first()
        doctor = Doctor(
            usuario_id=doctor_user.id,
            especialidad=primera_especialidad.nombre if primera_especialidad else 'Medicina General',
            licencia='MG-12345',
            experiencia='5 años de experiencia',
            horario='Lunes a Viernes: 8:00-17:00'
        )
        db.session.add(doctor)
        db.session.commit()
        print("✅ Usuario admin y doctor de ejemplo creados")

if __name__ == '__main__':
    app = create_app()
    
    # Configurar base de datos después de crear la app
    setup_database(app)
    
    print("✅ Aplicación Flask iniciada correctamente")
    print("✅ Base de datos creada")
    print("🌐 Servidor ejecutándose en: http://127.0.0.1:5000")
    app.run(debug=True)