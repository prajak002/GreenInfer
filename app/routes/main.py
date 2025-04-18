from flask import Blueprint, render_template
from app.models.models import Assessment

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    assessments = Assessment.query.order_by(Assessment.timestamp.desc()).limit(5).all()
    return render_template('dashboard.html', assessments=assessments)