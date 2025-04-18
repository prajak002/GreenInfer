import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///greeninfer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUD_CREDENTIALS = {
        'aws': {
            'access_key': os.environ.get('AWS_ACCESS_KEY'),
            'secret_key': os.environ.get('AWS_SECRET_KEY')
        }
    }