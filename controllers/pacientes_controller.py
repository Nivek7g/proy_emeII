from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.patient import Patient
from utils.helpers import login_required
from datetime import datetime  # ← AGREGAR ESTE IMPORT

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
            # Validar campos requeridos
            if not request.form['nombre'] or not request.form['apellidos'] or not request.form['fecha_nacimiento']:
                flash('Todos los campos marcados con * son obligatorios.', 'error')
                return render_template('pacientes/add.html')
            
            # CONVERTIR string a objeto date
            fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
            
            paciente = Patient(
                nombre=request.form['nombre'],
                apellidos=request.form['apellidos'],
                fecha_nacimiento=fecha_nacimiento,  # ← Usar el objeto date
                telefono=request.form.get('telefono', ''),
                direccion=request.form.get('direccion', ''),
                alergias=request.form.get('alergias', '')
            )
            
            db.session.add(paciente)
            db.session.commit()
            
            flash('Paciente agregado correctamente.', 'success')
            return redirect(url_for('pacientes_controller.index'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Error en el formato de la fecha. Use el formato YYYY-MM-DD.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar paciente: {str(e)}', 'error')
            print(f"ERROR: {e}")
    
    return render_template('pacientes/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    paciente = Patient.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # CONVERTIR string a objeto date para edición también
            fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
            
            paciente.nombre = request.form['nombre']
            paciente.apellidos = request.form['apellidos']
            paciente.fecha_nacimiento = fecha_nacimiento  # ← Usar el objeto date
            paciente.telefono = request.form.get('telefono', '')
            paciente.direccion = request.form.get('direccion', '')
            paciente.alergias = request.form.get('alergias', '')
            
            db.session.commit()
            flash('Paciente actualizado correctamente.', 'success')
            return redirect(url_for('pacientes_controller.index'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Error en el formato de la fecha. Use el formato YYYY-MM-DD.', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar paciente: {str(e)}', 'error')
    
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
        flash(f'Error al eliminar paciente: {str(e)}', 'error')
    
    return redirect(url_for('pacientes_controller.index'))