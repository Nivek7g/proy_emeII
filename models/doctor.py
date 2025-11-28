from models import db

class Doctor(db.Model):
    __tablename__ = 'doctores'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('especialidades.id'), nullable=True)  # ← NUEVO
    licencia = db.Column(db.String(50), unique=True)
    experiencia = db.Column(db.String(100))
    biografia = db.Column(db.Text)  # ← NUEVO
    activo = db.Column(db.Boolean, default=True)  # ← NUEVO
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones existentes
    citas = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    historiales = db.relationship('MedicalRecord', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
    # Nuevas relaciones
    horarios = db.relationship('HorarioDoctor', backref='doctor', lazy=True, cascade='all, delete-orphan')  # ← NUEVO
    
    def __repr__(self):
        return f'<Doctor {self.especialidad}>'
    
    @property
    def nombre_completo(self):
        from models.user import User
        user = User.query.get(self.usuario_id)
        return f"Dr. {user.usuario}" if user else "Doctor"
    
    @property
    def especialidad_nombre(self):
        from models.especialidad import Especialidad
        if self.especialidad_id:
            especialidad = Especialidad.query.get(self.especialidad_id)
            return especialidad.nombre if especialidad else "Sin especialidad"
        return "Sin especialidad"