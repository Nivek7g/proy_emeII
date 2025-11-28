from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# Importar todos los modelos
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.prescription import Prescription

# Nuevos modelos
from models.especialidad import Especialidad
from models.horario_doctor import HorarioDoctor
from models.medicamento import Medicamento
from models.pago import Pago
from models.consultorio import Consultorio