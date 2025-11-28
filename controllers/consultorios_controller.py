from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.consultorio import Consultorio
from utils.helpers import login_required, admin_required

bp = Blueprint('consultorios_controller', __name__)

@bp.route('/')
@login_required
def index():
    consultorios = Consultorio.query.order_by(Consultorio.numero).all()
    return render_template('consultorios/list.html', consultorios=consultorios)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        try:
            consultorio = Consultorio(
                numero=request.form['numero'],
                piso=int(request.form['piso']),
                descripcion=request.form['descripcion'],
                equipamiento=request.form['equipamiento']
            )
            db.session.add(consultorio)
            db.session.commit()
            flash('Consultorio agregado correctamente.', 'success')
            return redirect(url_for('consultorios_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar consultorio.', 'error')
    
    return render_template('consultorios/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    consultorio = Consultorio.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            consultorio.numero = request.form['numero']
            consultorio.piso = int(request.form['piso'])
            consultorio.descripcion = request.form['descripcion']
            consultorio.equipamiento = request.form['equipamiento']
            consultorio.activo = 'activo' in request.form
            
            db.session.commit()
            flash('Consultorio actualizado correctamente.', 'success')
            return redirect(url_for('consultorios_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar consultorio.', 'error')
    
    return render_template('consultorios/edit.html', consultorio=consultorio)

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    try:
        consultorio = Consultorio.query.get_or_404(id)
        db.session.delete(consultorio)
        db.session.commit()
        flash('Consultorio eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar consultorio.', 'error')
    
    return redirect(url_for('consultorios_controller.index'))