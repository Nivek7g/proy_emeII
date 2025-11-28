from models import db

class Appointment(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorios.id'), nullable=True)  # ← NUEVO
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    tipo_consulta = db.Column(db.String(50))
    motivo = db.Column(db.Text)
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Nueva relación
    pago = db.relationship('Pago', backref='cita', uselist=False, cascade='all, delete-orphan')  # ← NUEVO
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.fecha} {self.hora}>'
    
    @property
    def paciente_nombre(self):
        from models.patient import Patient
        paciente = Patient.query.get(self.paciente_id)
        return f"{paciente.nombre} {paciente.apellidos}" if paciente else "Paciente"
    
    @property
    def doctor_nombre(self):
        from models.doctor import Doctor
        doctor = Doctor.query.get(self.doctor_id)
        return doctor.nombre_completo if doctor else "Doctor"
    
    @property
    def consultorio_numero(self):
        from models.consultorio import Consultorio
        if self.consultorio_id:
            consultorio = Consultorio.query.get(self.consultorio_id)
            return consultorio.numero if consultorio else "Sin asignar"
        return "Sin asignar"