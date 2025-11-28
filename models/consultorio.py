from models import db

class Consultorio(db.Model):
    __tablename__ = 'consultorios'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False, unique=True)
    piso = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    equipamiento = db.Column(db.Text)  # Lista de equipos disponibles
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    citas = db.relationship('Appointment', backref='consultorio', lazy=True)
    
    def __repr__(self):
        return f'<Consultorio {self.numero}>'