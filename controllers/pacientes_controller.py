from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.patient import Patient
from utils.helpers import login_required

bp = Blueprint('pacientes_controller', __name__)

@bp.route('/')
@login_required
def index():
    pacientes = Patient.query.order_by(Patient.id.desc()).all()
    return render_template('pacientes/list.html', pacientes=pacientes)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            paciente = Patient(
                nombre=request.form['nombre'],
                apellidos=request.form['apellidos'],
                fecha_nacimiento=request.form['fecha_nacimiento'],
                telefono=request.form['telefono'],
                direccion=request.form['direccion'],
                alergias=request.form['alergias']
            )
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente agregado correctamente.', 'success')
            return redirect(url_for('pacientes_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar paciente.', 'error')
    
    return render_template('pacientes/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    paciente = Patient.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            paciente.nombre = request.form['nombre']
            paciente.apellidos = request.form['apellidos']
            paciente.fecha_nacimiento = request.form['fecha_nacimiento']
            paciente.telefono = request.form['telefono']
            paciente.direccion = request.form['direccion']
            paciente.alergias = request.form['alergias']
            
            db.session.commit()
            flash('Paciente actualizado correctamente.', 'success')
            return redirect(url_for('pacientes_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar paciente.', 'error')
    
    return render_template('pacientes/edit.html', paciente=paciente)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        paciente = Patient.query.get_or_404(id)
        db.session.delete(paciente)
        db.session.commit()
        flash('Paciente eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar paciente.', 'error')
    
    return redirect(url_for('pacientes_controller.index'))