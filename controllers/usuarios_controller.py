from flask import Blueprint, render_template
from utils.helpers import login_required, admin_required

bp = Blueprint('usuarios_controller', __name__)

@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('usuarios/list.html')