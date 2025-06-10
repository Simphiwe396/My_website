from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory, jsonify
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# ✅ Use SQLite (no PostgreSQL needed)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Import and initialize shared db instance
from src.models.db import db
db.init_app(app)

# Import models to create tables
from src.models.product import Product, Category
from src.models.user import User
from src.models.order import Order, OrderItem

# Register blueprints
from src.routes.auth import auth_bp
from src.routes.products import products_bp
from src.routes.orders import orders_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory