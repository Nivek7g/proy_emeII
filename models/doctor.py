from models import db

class Doctor(db.Model):
    __tablename__ = 'doctores'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia = db.Column(db.String(50), unique=True)
    horario = db.Column(db.Text)  # Ej: "Lunes a Viernes: 8:00-17:00"
    experiencia = db.Column(db.String(100))  # Ej: "5 años"
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    citas = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    historiales = db.relationship('MedicalRecord', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Doctor {self.especialidad}>'
    
    @property
    def nombre_completo(self):
        from models.user import User
        user = User.query.get(self.usuario_id)
        return f"Dr. {user.usuario}" if user else "Doctor"