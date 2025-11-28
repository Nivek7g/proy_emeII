from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.doctor import Doctor
from models.user import User
from models.especialidad import Especialidad
from utils.helpers import login_required, admin_required

bp = Blueprint('doctores_controller', __name__)

@bp.route('/')
@login_required
def index():
    doctores = Doctor.query.all()
    return render_template('doctores/list.html', doctores=doctores)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        try:
            # Primero crear el usuario
            usuario = request.form['usuario']
            correo = request.form['correo']
            celular = request.form['celular']
            contraseña = request.form['contraseña']
            
            # Verificar si el usuario ya existe
            if User.query.filter_by(usuario=usuario).first():
                flash('El usuario ya existe.', 'error')
                return render_template('doctores/add.html', especialidades=Especialidad.query.all())
            
            user = User(
                usuario=usuario,
                correo=correo,
                celular=celular,
                rol='doctor'
            )
            user.set_password(contraseña)
            db.session.add(user)
            db.session.flush()  # Para obtener el ID sin commit
            
            # Crear el doctor - CORREGIDO: usar especialidad_id en lugar de especialidad
            doctor = Doctor(
                usuario_id=user.id,
                especialidad_id=request.form['especialidad_id'],  # ← CAMBIADO
                licencia=request.form['licencia'],
                experiencia=request.form['experiencia'],
                biografia=request.form.get('biografia', ''),
                activo=True
            )
            db.session.add(doctor)
            db.session.commit()
            
            flash('Doctor agregado correctamente.', 'success')
            return redirect(url_for('doctores_controller.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar doctor: {str(e)}', 'error')
    
    return render_template('doctores/add.html', especialidades=Especialidad.query.all())

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    doctor = Doctor.query.get_or_404(id)
    user = User.query.get(doctor.usuario_id)
    
    if request.method == 'POST':
        try:
            # Actualizar usuario
            user.usuario = request.form['usuario']
            user.correo = request.form['correo']
            user.celular = request.form['celular']
            
            # Actualizar doctor - CORREGIDO
            doctor.especialidad_id = request.form['especialidad_id']  # ← CAMBIADO
            doctor.licencia = request.form['licencia']
            doctor.experiencia = request.form['experiencia']
            doctor.biografia = request.form.get('biografia', '')
            doctor.activo = 'activo' in request.form
            
            # Si se proporciona nueva contraseña
            if request.form['contraseña']:
                user.set_password(request.form['contraseña'])
            
            db.session.commit()
            flash('Doctor actualizado correctamente.', 'success')
            return redirect(url_for('doctores_controller.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar doctor: {str(e)}', 'error')
    
    especialidades = Especialidad.query.all()
    return render_template('doctores/edit.html', doctor=doctor, user=user, especialidades=especialidades)

@bp.route('/delete/<int:id>')
@login_required
@admin_required
def delete(id):
    try:
        doctor = Doctor.query.get_or_404(id)
        user = User.query.get(doctor.usuario_id)
        
        db.session.delete(doctor)
        db.session.delete(user)
        db.session.commit()
        
        flash('Doctor eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar doctor: {str(e)}', 'error')
    
    return redirect(url_for('doctores_controller.index'))