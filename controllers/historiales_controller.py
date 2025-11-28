from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # ← Agregar session aquí
from models import db
from models.medical_record import MedicalRecord
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from utils.helpers import login_required
from datetime import datetime

bp = Blueprint('historiales_controller', __name__)

@bp.route('/')
@login_required
def index():
    # Si es doctor, mostrar solo sus historiales
    if session.get('user_rol') == 'doctor':  # ← Ahora session está definido
        from models.user import User
        user = User.query.filter_by(usuario=session['usuario']).first()
        if user and user.doctor:
            doctor = Doctor.query.filter_by(usuario_id=user.id).first()
            historiales = MedicalRecord.query.filter_by(doctor_id=doctor.id).order_by(MedicalRecord.fecha_consulta.desc()).all()
        else:
            historiales = []
    else:
        # Admin ve todos los historiales
        historiales = MedicalRecord.query.order_by(MedicalRecord.fecha_consulta.desc()).all()
    
    return render_template('historiales/list.html', historiales=historiales)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            # Convertir fecha y hora
            fecha_consulta_str = f"{request.form['fecha_consulta']} {request.form['hora_consulta']}"
            fecha_consulta = datetime.strptime(fecha_consulta_str, '%Y-%m-%d %H:%M')
            
            historial = MedicalRecord(
                paciente_id=request.form['paciente_id'],
                doctor_id=request.form['doctor_id'],
                cita_id=request.form.get('cita_id') or None,
                fecha_consulta=fecha_consulta,
                peso=float(request.form['peso']) if request.form['peso'] else None,
                altura=float(request.form['altura']) if request.form['altura'] else None,
                presion_arterial=request.form['presion_arterial'],
                temperatura=float(request.form['temperatura']) if request.form['temperatura'] else None,
                sintomas=request.form['sintomas'],
                diagnostico=request.form['diagnostico'],
                tratamiento=request.form['tratamiento'],
                medicamentos_recetados=request.form['medicamentos_recetados'],
                observaciones=request.form['observaciones'],
                proxima_cita=request.form['proxima_cita'] if request.form['proxima_cita'] else None
            )
            
            db.session.add(historial)
            db.session.commit()
            flash('Historial médico creado correctamente.', 'success')
            return redirect(url_for('historiales_controller.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear historial médico: {str(e)}', 'error')
    
    return render_template('historiales/add.html', 
                         pacientes=Patient.query.all(),
                         doctores=Doctor.query.all(),
                         citas=Appointment.query.filter_by(estado='completada').all())

@bp.route('/view/<int:id>')
@login_required
def view(id):
    historial = MedicalRecord.query.get_or_404(id)
    return render_template('historiales/view.html', historial=historial)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    historial = MedicalRecord.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Convertir fecha y hora
            fecha_consulta_str = f"{request.form['fecha_consulta']} {request.form['hora_consulta']}"
            fecha_consulta = datetime.strptime(fecha_consulta_str, '%Y-%m-%d %H:%M')
            
            historial.paciente_id = request.form['paciente_id']
            historial.doctor_id = request.form['doctor_id']
            historial.cita_id = request.form.get('cita_id') or None
            historial.fecha_consulta = fecha_consulta
            historial.peso = float(request.form['peso']) if request.form['peso'] else None
            historial.altura = float(request.form['altura']) if request.form['altura'] else None
            historial.presion_arterial = request.form['presion_arterial']
            historial.temperatura = float(request.form['temperatura']) if request.form['temperatura'] else None
            historial.sintomas = request.form['sintomas']
            historial.diagnostico = request.form['diagnostico']
            historial.tratamiento = request.form['tratamiento']
            historial.medicamentos_recetados = request.form['medicamentos_recetados']
            historial.observaciones = request.form['observaciones']
            historial.proxima_cita = request.form['proxima_cita'] if request.form['proxima_cita'] else None
            
            db.session.commit()
            flash('Historial médico actualizado correctamente.', 'success')
            return redirect(url_for('historiales_controller.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar historial médico.', 'error')
    
    return render_template('historiales/edit.html', 
                         historial=historial,
                         pacientes=Patient.query.all(),
                         doctores=Doctor.query.all(),
                         citas=Appointment.query.filter_by(estado='completada').all())

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        historial = MedicalRecord.query.get_or_404(id)
        db.session.delete(historial)
        db.session.commit()
        flash('Historial médico eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar historial médico.', 'error')
    
    return redirect(url_for('historiales_controller.index'))

@bp.route('/paciente/<int:paciente_id>')
@login_required
def por_paciente(paciente_id):
    """Ver todos los historiales de un paciente específico"""
    paciente = Patient.query.get_or_404(paciente_id)
    historiales = MedicalRecord.query.filter_by(paciente_id=paciente_id).order_by(MedicalRecord.fecha_consulta.desc()).all()
    
    return render_template('historiales/por_paciente.html', 
                         paciente=paciente, 
                         historiales=historiales)