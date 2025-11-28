from models import db
from datetime import datetime  # ← AGREGAR ESTE IMPORT

class MedicalRecord(db.Model):
    __tablename__ = 'historiales_medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctores.id'), nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=True)
    fecha_consulta = db.Column(db.DateTime, nullable=False)  # ← CAMBIAR A DateTime
    peso = db.Column(db.Float)  # kg
    altura = db.Column(db.Float)  # cm
    presion_arterial = db.Column(db.String(20))  # Ej: "120/80"
    temperatura = db.Column(db.Float)  # °C
    sintomas = db.Column(db.Text, nullable=False)
    diagnostico = db.Column(db.Text, nullable=False)
    tratamiento = db.Column(db.Text)
    medicamentos_recetados = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    proxima_cita = db.Column(db.Date)  # ← Date para fecha futura
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<MedicalRecord {self.id} - Paciente {self.paciente_id}>'
    
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
    def imc(self):
        """Calcular Índice de Masa Corporal"""
        if self.peso and self.altura:
            altura_m = self.altura / 100  # Convertir cm a m
            return round(self.peso / (altura_m ** 2), 2)
        return None
    
    @property
    def fecha_consulta_formateada(self):
        """Fecha formateada para mostrar"""
        return self.fecha_consulta.strftime('%d/%m/%Y %H:%M') if self.fecha_consulta else ""
    
    @property
    def proxima_cita_formateada(self):
        """Próxima cita formateada"""
        return self.proxima_cita.strftime('%d/%m/%Y') if self.proxima_cita else ""