from models import db

class Pago(db.Model):
    __tablename__ = 'pagos'
    
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50))  # Efectivo, Tarjeta, Transferencia
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, completado, fallido
    referencia = db.Column(db.String(100))  # Número de transacción
    fecha_pago = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Pago {self.id} - ${self.monto}>'
    
    @property
    def paciente_nombre(self):
        from models.patient import Patient
        paciente = Patient.query.get(self.paciente_id)
        return f"{paciente.nombre} {paciente.apellidos}" if paciente else "Paciente"