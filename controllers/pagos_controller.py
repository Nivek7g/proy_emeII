from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.pago import Pago
from models.appointment import Appointment
from models.patient import Patient
from utils.helpers import login_required
from datetime import datetime

bp = Blueprint('pagos_controller', __name__)

@bp.route('/')
@login_required
def index():
    pagos = Pago.query.order_by(Pago.created_at.desc()).all()
    return render_template('pagos/list.html', pagos=pagos)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            pago = Pago(
                cita_id=request.form['cita_id'],
                paciente_id=request.form['paciente_id'],
                monto=float(request.form['monto']),
                metodo_pago=request.form['metodo_pago'],
                estado=request.form['estado'],
                referencia=request.form['referencia'],
                fecha_pago=datetime.strptime(request.form['fecha_pago'], '%Y-%m-%d') if request.form['fecha_pago'] else None
            )
            db.session.add(pago)
            db.session.commit()
            flash('Pago registrado correctamente.', 'success')
            return redirect(url_for('pagos_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar pago: {str(e)}', 'error')
    
    citas = Appointment.query.filter_by(estado='completada').all()
    pacientes = Patient.query.all()
    return render_template('pagos/add.html', citas=citas, pacientes=pacientes)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    pago = Pago.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            pago.monto = float(request.form['monto'])
            pago.metodo_pago = request.form['metodo_pago']
            pago.estado = request.form['estado']
            pago.referencia = request.form['referencia']
            pago.fecha_pago = datetime.strptime(request.form['fecha_pago'], '%Y-%m-%d') if request.form['fecha_pago'] else None
            
            db.session.commit()
            flash('Pago actualizado correctamente.', 'success')
            return redirect(url_for('pagos_controller.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar pago.', 'error')
    
    citas = Appointment.query.filter_by(estado='completada').all()
    pacientes = Patient.query.all()
    return render_template('pagos/edit.html', pago=pago, citas=citas, pacientes=pacientes)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    try:
        pago = Pago.query.get_or_404(id)
        db.session.delete(pago)
        db.session.commit()
        flash('Pago eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar pago.', 'error')
    
    return redirect(url_for('pagos_controller.index'))