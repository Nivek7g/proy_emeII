from flask_login import UserMixin
from models import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default='usuario')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    doctor = db.relationship('Doctor', backref='usuario', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.contraseña = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.contraseña, password)
    
    def __repr__(self):
        return f'<User {self.usuario}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))