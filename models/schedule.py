from .database import db
from datetime import datetime, time

class HorarioDoctor(db.Model):
    __tablename__ = 'horarios_doctores'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 1=Lunes, 2=Martes, etc.
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HorarioDoctor {self.doctor_id} - Dia {self.dia_semana}>'