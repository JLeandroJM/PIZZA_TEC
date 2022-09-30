from flask import Flask, render_template
from flask_login import LoginManager
from .config.config import Config
from .db.database import db, migrate
from .home import app as appViews, init_login
from .db.database import db
app = None
def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    app.secret_key = 'clave secretita'
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    # register blueprint apps
    app.register_blueprint(appViews)

    migrate.init_app(app, db)        # Flask DB Migration
    init_login(app)
    
    print(app.config['UPLOAD_FOLDER'])
    #handlers de errores
    register_error_handlers(app)
    return app

def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404