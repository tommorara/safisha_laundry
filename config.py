import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://laundry_user:1290@localhost/laundry_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

