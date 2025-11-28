from flask import Flask
from config import Config
from models import db, login_manager

def create_app():
    app = Flask(__name__, template_folder='views')
    app.config.from_object(Config)
    
    # Inicializar extensiones PRIMERO
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_controller.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints DESPUÉS de inicializar extensiones
    try:
        from controllers.auth_controller import bp as auth_bp
        from controllers.dashboard_controller import bp as dashboard_bp
        from controllers.pacientes_controller import bp as pacientes_bp
        from controllers.doctores_controller import bp as doctores_bp
        from controllers.citas_controller import bp as citas_bp
        from controllers.historiales_controller import bp as historiales_bp
        from controllers.usuarios_controller import bp as usuarios_bp
        from controllers.especialidades_controller import bp as especialidades_bp
        from controllers.medicamentos_controller import bp as medicamentos_bp
        from controllers.consultorios_controller import bp as consultorios_bp
        from controllers.pagos_controller import bp as pagos_bp
        from controllers.horarios_controller import bp as horarios_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
        app.register_blueprint(doctores_bp, url_prefix='/doctores')
        app.register_blueprint(citas_bp, url_prefix='/citas')
        app.register_blueprint(historiales_bp, url_prefix='/historiales')
        app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
        app.register_blueprint(especialidades_bp, url_prefix='/especialidades')
        app.register_blueprint(medicamentos_bp, url_prefix='/medicamentos')
        app.register_blueprint(consultorios_bp, url_prefix='/consultorios')
        app.register_blueprint(pagos_bp, url_prefix='/pagos')
        app.register_blueprint(horarios_bp, url_prefix='/horarios')

    except ImportError as e:
        print(f"⚠️  Algunos controladores no están implementados: {e}")
    
    return app

def setup_database(app):
    """Función separada para configurar la base de datos"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas correctamente")
        
        # Crear datos iniciales
        create_initial_data()

def create_initial_data():
    """Crear datos iniciales - DEBE ejecutarse dentro de un contexto de aplicación"""
    from models.user import User
    from models.doctor import Doctor
    from models.especialidad import Especialidad
    from models.consultorio import Consultorio
    from models.medicamento import Medicamento
    
    print("📦 Creando datos iniciales...")
    
    # Crear especialidades
    especialidades = [
        'Medicina General', 'Pediatría', 'Ginecología', 'Cardiología',
        'Dermatología', 'Ortopedia', 'Oftalmología', 'Psiquiatría'
    ]
    
    for esp_nombre in especialidades:
        if not Especialidad.query.filter_by(nombre=esp_nombre).first():
            especialidad = Especialidad(nombre=esp_nombre)
            db.session.add(especialidad)
            print(f"✅ Especialidad creada: {esp_nombre}")
    
    db.session.commit()
    
    # Crear consultorios
    for i in range(1, 6):
        if not Consultorio.query.filter_by(numero=f"C-{i}").first():
            consultorio = Consultorio(
                numero=f"C-{i}",
                piso=1,
                descripcion=f"Consultorio {i} - Primer piso"
            )
            db.session.add(consultorio)
            print(f"✅ Consultorio creado: C-{i}")
    
    db.session.commit()
    
    # Crear medicamentos de ejemplo
    medicamentos = [
        {'nombre': 'Paracetamol 500mg', 'principio_activo': 'Paracetamol', 'stock': 100},
        {'nombre': 'Ibuprofeno 400mg', 'principio_activo': 'Ibuprofeno', 'stock': 80},
        {'nombre': 'Amoxicilina 500mg', 'principio_activo': 'Amoxicilina', 'stock': 50},
    ]
    
    for med in medicamentos:
        if not Medicamento.query.filter_by(nombre=med['nombre']).first():
            medicamento = Medicamento(**med)
            db.session.add(medicamento)
            print(f"✅ Medicamento creado: {med['nombre']}")
    
    db.session.commit()
    
    # Crear usuario admin
    if not User.query.filter_by(usuario='admin').first():
        admin = User(
            usuario='admin',
            correo='admin@consultorio.com',
            celular='77712345',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ Usuario admin creado")
    
    # Crear doctor de ejemplo
    if not User.query.filter_by(usuario='drgarcia').first():
        doctor_user = User(
            usuario='drgarcia',
            correo='drgarcia@consultorio.com',
            celular='77754321',
            rol='doctor'
        )
        doctor_user.set_password('doctor123')
        db.session.add(doctor_user)
        db.session.commit()
        print("✅ Usuario doctor creado")
        
        # Asignar doctor
        medicina_general = Especialidad.query.filter_by(nombre='Medicina General').first()
        doctor = Doctor(
            usuario_id=doctor_user.id,
            especialidad_id=medicina_general.id if medicina_general else None,
            licencia='MG-12345',
            experiencia='5 años de experiencia',
            biografia='Especialista en medicina general con amplia experiencia.'
        )
        db.session.add(doctor)
        db.session.commit()
        print("✅ Doctor asignado")
    
    print("🎉 Datos iniciales creados exitosamente")

if __name__ == '__main__':
    app = create_app()
    setup_database(app)
    print("🌐 Servidor ejecutándose en: http://127.0.0.1:5000")
    app.run(debug=True)