from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.especialidad import Especialidad
from utils.helpers import login_required, admin_required

bp = Blueprint('especialidades_controller', __name__)

@bp.route('/')
@login_required
def index():
    especialidades = Especialidad.query.order_by(Especialidad.nombre).all()
    return render_template('especialidades/list.html', especialidades=especialidades)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        try:
            especialidad = Especialidad(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion']
            )
            db.session.add(especialidad)
            db.session.commit()
            flash('Especialidad agregada correctamente.', 'success')
            return redirect(url_for('especialidades_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar especialidad.', 'error')
    
    return render_template('especialidades/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    especialidad = Especialidad.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            especialidad.nombre = request.form['nombre']
            especialidad.descripcion = request.form['descripcion']
            especialidad.activa = 'activa' in request.form
            
            db.session.commit()
            flash('Especialidad actualizada correctamente.', 'success')
            return redirect(url_for('especialidades_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar especialidad.', 'error')
    
    return render_template('especialidades/edit.html', especialidad=especialidad)

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    try:
        especialidad = Especialidad.query.get_or_404(id)
        db.session.delete(especialidad)
        db.session.commit()
        flash('Especialidad eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar especialidad.', 'error')
    
    return redirect(url_for('especialidades_controller.index'))