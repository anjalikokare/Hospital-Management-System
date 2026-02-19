from flask import Flask, render_template, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.models import db
import os
from cache import init_cache

from auth_api import auth_bp
from admin_api import admin_bp
from doctor_api import doctor_bp
from patient_api import patient_bp

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    frontend_dist = os.path.join(base_dir, "../frontend/dist")
    backend_static = os.path.join(base_dir, "static")

    app = Flask(
        __name__,
        static_folder=backend_static,        
        static_url_path="/static",
        template_folder=frontend_dist          
    )
    
    @app.route("/", defaults={'path': ''})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path.startswith("api/") or path.startswith("static/"):
            return {"message": "Not Found"}, 404
        return render_template("index.html")

    @app.route("/assets/<path:filename>")
    def frontend_assets(filename):
        return send_from_directory(os.path.join(frontend_dist, "assets"), filename)

    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///hms_v2.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="super-secret-key",

        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",

        CACHE_TYPE="RedisCache",
        CACHE_REDIS_HOST="127.0.0.1",
        CACHE_REDIS_PORT=6379,
        CACHE_REDIS_DB=1,            
        CACHE_DEFAULT_TIMEOUT=300
    )

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    init_cache(app)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
