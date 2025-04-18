from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    cloud_provider = db.Column(db.String(64))
    instance_type = db.Column(db.String(128))
    region = db.Column(db.String(64))
    cpu_util = db.Column(db.Float)
    gpu_util = db.Column(db.Float)
    emissions = db.Column(db.Float)
    recommendations = db.relationship('Recommendation', backref='assessment', lazy='dynamic')

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    text = db.Column(db.String(256))
    impact = db.Column(db.Float)
    effort = db.Column(db.String(64))
    implemented = db.Column(db.Boolean, default=False)