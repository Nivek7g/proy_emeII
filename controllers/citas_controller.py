from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.consultorio import Consultorio
from utils.helpers import login_required
from datetime import datetime, date

bp = Blueprint('citas_controller', __name__)

@bp.route('/')
@login_required
def index():
    # Si es doctor, mostrar solo sus citas
    if session.get('user_rol') == 'doctor':
        from models.user import User
        user = User.query.filter_by(usuario=session['usuario']).first()
        if user and user.doctor:
            doctor = Doctor.query.filter_by(usuario_id=user.id).first()
            citas = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.fecha.desc(), Appointment.hora.desc()).all()
        else:
            citas = []
    else:
        # Admin ve todas las citas
        citas = Appointment.query.order_by(Appointment.fecha.desc(), Appointment.hora.desc()).all()
    
    return render_template('citas/list.html', citas=citas)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            # Convertir fecha a objeto date
            fecha_obj = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
            
            # Validación básica de horario (sin ScheduleManager)
            conflicto = Appointment.query.filter_by(
                doctor_id=int(request.form['doctor_id']),
                fecha=fecha_obj,
                hora=request.form['hora'],
                estado='confirmada'
            ).first()
            
            if conflicto:
                flash('El doctor ya tiene una cita confirmada en ese horario.', 'error')
                return render_template('citas/add.html', 
                                    pacientes=Patient.query.all(),
                                    doctores=Doctor.query.all(),
                                    consultorios=Consultorio.query.all())
            
            # Crear la cita
            cita = Appointment(
                paciente_id=int(request.form['paciente_id']),
                doctor_id=int(request.form['doctor_id']),
                consultorio_id=int(request.form['consultorio_id']) if request.form.get('consultorio_id') else None,
                fecha=fecha_obj,
                hora=request.form['hora'],
                tipo_consulta=request.form['tipo_consulta'],
                motivo=request.form['motivo'],
                notas=request.form.get('notas', ''),
                estado='pendiente'
            )
            
            db.session.add(cita)
            db.session.commit()
            flash('Cita agendada correctamente.', 'success')
            return redirect(url_for('citas_controller.index'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Error en el formato de la fecha. Use el formato YYYY-MM-DD.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agendar cita: {str(e)}', 'error')
    
    return render_template('citas/add.html', 
                         pacientes=Patient.query.all(),
                         doctores=Doctor.query.all(),
                         consultorios=Consultorio.query.all())

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    cita = Appointment.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Convertir fecha a objeto date
            fecha_obj = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
            
            # Verificar conflicto de horario
            conflicto = Appointment.query.filter(
                Appointment.doctor_id == int(request.form['doctor_id']),
                Appointment.fecha == fecha_obj,
                Appointment.hora == request.form['hora'],
                Appointment.estado == 'confirmada',
                Appointment.id != id
            ).first()
            
            if conflicto:
                flash('El doctor ya tiene una cita confirmada en ese horario.', 'error')
                return render_template('citas/edit.html', 
                                    cita=cita,
                                    pacientes=Patient.query.all(),
                                    doctores=Doctor.query.all(),
                                    consultorios=Consultorio.query.all())
            
            cita.paciente_id = int(request.form['paciente_id'])
            cita.doctor_id = int(request.form['doctor_id'])
            cita.consultorio_id = int(request.form['consultorio_id']) if request.form.get('consultorio_id') else None
            cita.fecha = fecha_obj
            cita.hora = request.form['hora']
            cita.tipo_consulta = request.form['tipo_consulta']
            cita.motivo = request.form['motivo']
            cita.notas = request.form.get('notas', '')
            
            db.session.commit()
            flash('Cita actualizada correctamente.', 'success')
            return redirect(url_for('citas_controller.index'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Error en el formato de la fecha. Use el formato YYYY-MM-DD.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cita: {str(e)}', 'error')
    
    return render_template('citas/edit.html', 
                         cita=cita,
                         pacientes=Patient.query.all(),
                         doctores=Doctor.query.all(),
                         consultorios=Consultorio.query.all())

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        cita = Appointment.query.get_or_404(id)
        db.session.delete(cita)
        db.session.commit()
        flash('Cita eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cita: {str(e)}', 'error')
    
    return redirect(url_for('citas_controller.index'))

@bp.route('/cambiar_estado/<int:id>/<estado>')
@login_required
def cambiar_estado(id, estado):
    try:
        cita = Appointment.query.get_or_404(id)
        estados_validos = ['pendiente', 'confirmada', 'cancelada', 'completada']
        
        if estado in estados_validos:
            cita.estado = estado
            db.session.commit()
            flash(f'Cita {estado} correctamente.', 'success')
        else:
            flash('Estado inválido.', 'error')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'error')
    
    return redirect(url_for('citas_controller.index'))

@bp.route('/api/horarios_disponibles/<int:doctor_id>/<fecha>')
@login_required
def horarios_disponibles(doctor_id, fecha):
    """API para obtener horarios disponibles de un doctor en una fecha específica"""
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        # Horarios de trabajo típicos
        horarios_trabajo = [
            '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
            '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
            '16:00', '16:30', '17:00'
        ]
        
        # Obtener citas existentes del doctor en esa fecha
        citas_existentes = Appointment.query.filter_by(
            doctor_id=doctor_id,
            fecha=fecha_obj,
            estado='confirmada'
        ).all()
        
        horarios_ocupados = [cita.hora for cita in citas_existentes]
        horarios_disponibles = [h for h in horarios_trabajo if h not in horarios_ocupados]
        
        return jsonify({
            'disponibles': horarios_disponibles,
            'ocupados': horarios_ocupados
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500