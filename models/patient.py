from models import db

class Patient(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    alergias = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    citas = db.relationship('Appointment', backref='paciente', cascade='all, delete-orphan')
    historiales = db.relationship('MedicalRecord', backref='paciente', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Patient {self.nombre} {self.apellidos}>'