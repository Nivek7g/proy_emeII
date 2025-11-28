from models import db

class Prescription(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    historial_id = db.Column(db.Integer, db.ForeignKey('historiales_medicos.id'), nullable=False)
    medicamento = db.Column(db.String(200), nullable=False)
    dosis = db.Column(db.String(100))
    frecuencia = db.Column(db.String(100))
    duracion = db.Column(db.String(50))
    instrucciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Prescription {self.medicamento}>'