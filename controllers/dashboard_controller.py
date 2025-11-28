from flask import Blueprint, render_template, session
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from utils.helpers import login_required
from datetime import date

bp = Blueprint('dashboard_controller', __name__)

@bp.route('/')
@login_required
def index():
    pacientes_count = Patient.query.count()
    doctores_count = Doctor.query.count()
    citas_count = Appointment.query.count()
    historiales_count = MedicalRecord.query.count()
    
    # Citas de hoy
    citas_hoy = Appointment.query.filter_by(fecha=date.today()).count()
    
    # Si es doctor, mostrar solo sus estadísticas
    if session.get('user_rol') == 'doctor':
        from models.user import User
        user = User.query.filter_by(usuario=session['usuario']).first()
        if user and user.doctor:
            doctor = Doctor.query.filter_by(usuario_id=user.id).first()
            citas_count = Appointment.query.filter_by(doctor_id=doctor.id).count()
            citas_hoy = Appointment.query.filter_by(doctor_id=doctor.id, fecha=date.today()).count()
            historiales_count = MedicalRecord.query.filter_by(doctor_id=doctor.id).count()
    
    return render_template('dashboard/index.html', 
                         pacientes_count=pacientes_count,
                         doctores_count=doctores_count,
                         citas_count=citas_count,
                         citas_hoy=citas_hoy,
                         historiales_count=historiales_count)