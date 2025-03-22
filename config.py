import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    # ✅ Correct database name
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1290@localhost/laundry_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

