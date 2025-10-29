import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEFAULT_TOKEN_EXPIRATION_MINUTES = 30
    FLAG = os.environ.get('FLAG', 'CYBN{prends contact avec un admin ya du y avoir un problème oopsi}')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'vL8HllzgYxlIICxlpCMbq7IK9WQpIo1N')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'VVBOsm4qipLEYWpWYEuk8VN-jaJGF9-lpgql248GlSuTnwi7MYVWE0lDmerS-GP4XgzCiOALKoa2JbjWOgcDCw')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False