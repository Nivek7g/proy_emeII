from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.medicamento import Medicamento
from utils.helpers import login_required, admin_required

bp = Blueprint('medicamentos_controller', __name__)

@bp.route('/')
@login_required
def index():
    medicamentos = Medicamento.query.order_by(Medicamento.nombre).all()
    return render_template('medicamentos/list.html', medicamentos=medicamentos)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        try:
            medicamento = Medicamento(
                nombre=request.form['nombre'],
                principio_activo=request.form['principio_activo'],
                concentracion=request.form['concentracion'],
                forma_farmaceutica=request.form['forma_farmaceutica'],
                laboratorio=request.form['laboratorio'],
                stock=int(request.form['stock']),
                stock_minimo=int(request.form['stock_minimo']),
                precio=float(request.form['precio']),
                requiere_receta='requiere_receta' in request.form
            )
            db.session.add(medicamento)
            db.session.commit()
            flash('Medicamento agregado correctamente.', 'success')
            return redirect(url_for('medicamentos_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar medicamento: {str(e)}', 'error')
    
    return render_template('medicamentos/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    medicamento = Medicamento.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            medicamento.nombre = request.form['nombre']
            medicamento.principio_activo = request.form['principio_activo']
            medicamento.concentracion = request.form['concentracion']
            medicamento.forma_farmaceutica = request.form['forma_farmaceutica']
            medicamento.laboratorio = request.form['laboratorio']
            medicamento.stock = int(request.form['stock'])
            medicamento.stock_minimo = int(request.form['stock_minimo'])
            medicamento.precio = float(request.form['precio'])
            medicamento.requiere_receta = 'requiere_receta' in request.form
            medicamento.activo = 'activo' in request.form
            
            db.session.commit()
            flash('Medicamento actualizado correctamente.', 'success')
            return redirect(url_for('medicamentos_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar medicamento.', 'error')
    
    return render_template('medicamentos/edit.html', medicamento=medicamento)

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    try:
        medicamento = Medicamento.query.get_or_404(id)
        db.session.delete(medicamento)
        db.session.commit()
        flash('Medicamento eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar medicamento.', 'error')
    
    return redirect(url_for('medicamentos_controller.index'))