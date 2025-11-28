from models import db

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    principio_activo = db.Column(db.String(200))
    concentracion = db.Column(db.String(100))
    forma_farmaceutica = db.Column(db.String(100))  # Tableta, jarabe, etc.
    laboratorio = db.Column(db.String(150))
    stock = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=10)
    precio = db.Column(db.Float, default=0.0)
    requiere_receta = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relaciones
    recetas = db.relationship('Prescription', backref='medicamento', lazy=True)
    
    def __repr__(self):
        return f'<Medicamento {self.nombre}>'