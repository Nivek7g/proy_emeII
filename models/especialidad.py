from models import db

class Especialidad(db.Model):
    __tablename__ = 'especialidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    doctores = db.relationship('Doctor', backref='especialidad_rel', lazy=True)
    
    def __repr__(self):
        return f'<Especialidad {self.nombre}>'