from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db
from models.horario_doctor import HorarioDoctor
from models.doctor import Doctor
from utils.helpers import login_required

bp = Blueprint('horarios_controller', __name__)

@bp.route('/')
@login_required
def index():
    horarios = HorarioDoctor.query.order_by(HorarioDoctor.doctor_id, HorarioDoctor.dia_semana).all()
    return render_template('horarios/list.html', horarios=horarios)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            horario = HorarioDoctor(
                doctor_id=request.form['doctor_id'],
                dia_semana=int(request.form['dia_semana']),
                hora_inicio=request.form['hora_inicio'],
                hora_fin=request.form['hora_fin']
            )
            db.session.add(horario)
            db.session.commit()
            flash('Horario agregado correctamente.', 'success')
            return redirect(url_for('horarios_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar horario.', 'error')
    
    doctores = Doctor.query.filter_by(activo=True).all()
    return render_template('horarios/add.html', doctores=doctores)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    horario = HorarioDoctor.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            horario.doctor_id = request.form['doctor_id']
            horario.dia_semana = int(request.form['dia_semana'])
            horario.hora_inicio = request.form['hora_inicio']
            horario.hora_fin = request.form['hora_fin']
            horario.activo = 'activo' in request.form
            
            db.session.commit()
            flash('Horario actualizado correctamente.', 'success')
            return redirect(url_for('horarios_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar horario.', 'error')
    
    doctores = Doctor.query.filter_by(activo=True).all()
    return render_template('horarios/edit.html', horario=horario, doctores=doctores)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        horario = HorarioDoctor.query.get_or_404(id)
        db.session.delete(horario)
        db.session.commit()
        flash('Horario eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar horario.', 'error')
    
    return redirect(url_for('horarios_controller.index'))

@bp.route('/api/doctor/<int:doctor_id>')
@login_required
def horarios_doctor(doctor_id):
    """API para obtener horarios de un doctor específico"""
    horarios = HorarioDoctor.query.filter_by(doctor_id=doctor_id, activo=True).all()
    result = []
    
    for horario in horarios:
        result.append({
            'id': horario.id,
            'dia_semana': horario.dia_semana,
            'dia_nombre': horario.dia_nombre,
            'hora_inicio': horario.hora_inicio.strftime('%H:%M'),
            'hora_fin': horario.hora_fin.strftime('%H:%M')
        })
    
    return jsonify(result)