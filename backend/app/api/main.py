from flask import Flask
from flask_cors import CORS
from app.db.engine import engine
from app.db.base import Base
import app.db.models  # keep this so Base has metadata
from app.api.health import bp as health_bp
from app.api.customers import bp as customers_bp

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(bind=engine)

app.register_blueprint(health_bp)
app.register_blueprint(customers_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
