# models/specialty.py
from .database import db
from datetime import datetime

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con doctores
    doctores = db.relationship('Doctor', backref='especialidad', lazy=True)
    
    def __repr__(self):
        return f'<Especialidad {self.nombre}>'