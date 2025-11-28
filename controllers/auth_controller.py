from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from utils.helpers import login_required

bp = Blueprint('auth_controller', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        user = User.query.filter_by(usuario=usuario).first()
        
        if user and user.check_password(contraseña):
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            session['user_rol'] = user.rol
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard_controller.index'))
        else:
            flash('Credenciales incorrectas.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        celular = request.form['celular']
        contraseña = request.form['contraseña']
        confirmar = request.form['confirmar']
        
        if contraseña != confirmar:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html')
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(usuario=usuario).first():
            flash('El usuario ya existe.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado.', 'error')
            return render_template('auth/register.html')
        
        try:
            user = User(
                usuario=usuario,
                correo=correo,
                celular=celular,
                rol='usuario'  # Rol por defecto
            )
            user.set_password(contraseña)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth_controller.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario.', 'error')
    
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth_controller.login'))