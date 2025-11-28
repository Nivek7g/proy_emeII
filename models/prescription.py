from models import db

class Prescription(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    historial_id = db.Column(db.Integer, db.ForeignKey('historiales_medicos.id'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)  # ← ACTUALIZADO
    dosis = db.Column(db.String(100))
    frecuencia = db.Column(db.String(100))
    duracion = db.Column(db.String(50))
    instrucciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Prescription {self.medicamento_id}>'
    
    @property
    def medicamento_nombre(self):
        from models.medicamento import Medicamento
        medicamento = Medicamento.query.get(self.medicamento_id)
        return medicamento.nombre if medicamento else "Medicamento"