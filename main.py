import os
import sys
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS

# Ielādē .env failu
load_dotenv(dotenv_path=".env")
print("Current working directory:", os.getcwd())

# Nodrošina, ka Python zina, kur meklēt src/*
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Konfigurācija
    app.config['SECRET_KEY'] = 'n8n-ai-agent-secret-key-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Iespējo CORS
    CORS(app, origins="*")
    
    # Inicializē datubāzi (no extensions)
    from src.extensions import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Importē blueprintus PĒCĀK - kad db jau ir inicializēts
    from src.routes.user import user_bp
    from src.routes.workflow import workflow_bp
    from src.routes.n8n_integration import n8n_bp
    from src.routes.node_routes import node_bp
    
    # Reģistrē blueprintus
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(workflow_bp, url_prefix='/api/workflow')
    app.register_blueprint(n8n_bp, url_prefix='/api/n8n')
    app.register_blueprint(node_bp, url_prefix='/api')
    
    # Frontend apkalpošana
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404
        file_path = os.path.join(static_folder_path, path)
        if path != "" and os.path.exists(file_path):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    return app

# Izveido aplikācijas instanci
app = create_app()

# Servera palaišana
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')
