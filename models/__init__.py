from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# Importar todos los modelos para que SQLAlchemy los reconozca
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.prescription import Prescription  # Opcional
# models/__init__.py
from .user import User
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment
from .medical_record import MedicalRecord
from .prescription import Prescription
# Agregar los nuevos modelos
from .specialty import Especialidad
from .schedule import HorarioDoctor
from .medication import Medicamento
from .payment import Pago

__all__ = [
    'User', 'Patient', 'Doctor', 'Appointment', 
    'MedicalRecord', 'Prescription', 'Especialidad',
    'HorarioDoctor', 'Medicamento', 'Pago'
]