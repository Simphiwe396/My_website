from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, send_from_directory, jsonify
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(_file_)))

# Initialize Flask app
app = Flask(_name_, static_folder='static', template_folder='templates')

# ✅ SQLite (or use env DATABASE_URL for PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Import and initialize shared db instance
from src.models.db import db
db.init_app(app)

# ✅ Import all models BEFORE db.create_all
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

# ✅ Health check
@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"}), 200

# ✅ Page routes to render HTML
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

# ✅ Fallback for unmatched static files (optional, safe fallback)
@app.route('/<path:filename>')
def static_proxy(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, filename)
    return jsonify({'error': 'File not found'}), 404

# ✅ Create tables and sample data (only for local dev)
def create_tables():
    with app.app_context():
        db.create_all()
        if Category.query.count() == 0:
            categories = [
                Category(name='T-Shirts', description='Comfortable and stylish', image_url='', is_featured=True),
                Category(name='Jeans', description='Durable and fashionable', image_url='', is_featured=True),
            ]
            db.session.add_all(categories)
            db.session.commit()

            product = Product(name='Sample T-Shirt', description='Nice shirt', price=19.99, sale_price=14.99,
                              image_url='', category_id=1, stock=10, is_featured=True, is_new=True, is_sale=True)
            db.session.add(product)
            db.session.commit()

            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

if _name_ == '_main_':
    create_tables()
    app.run(debug=True, host='0.0.0.0')
