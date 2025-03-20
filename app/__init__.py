from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Update with your MySQL username, password, host, and database name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_username:your_password@localhost/laundrydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app

