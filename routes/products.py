from flask import Blueprint, request, jsonify
from src.models.product import Product, Category, db

products_bp = Blueprint('products', __name__)

# Get all products
@products_bp.route('/', methods=['GET'])
def get_products():
    # Get query parameters for filtering
    category = request.args.get('category')
    featured = request.args.get('featured')
    new = request.args.get('new')
    sale = request.args.get('sale')
    search = request.args.get('search')
    
    # Start with base query
    query = Product.query
    
    # Apply filters
    if category:
        category_obj = Category.query.filter_by(name=category).first()
        if category_obj:
            query = query.filter_by(category_id=category_obj.id)
    
    if featured and featured.lower() == 'true':
        query = query.filter_by(is_featured=True)
    
    if new and new.lower() == 'true':
        query = query.filter_by(is_new=True)
    
    if sale and sale.lower() == 'true':
        query = query.filter_by(is_sale=True)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    # Execute query
    products = query.all()
    
    # Convert to dict
    products_list = [product.to_dict() for product in products]
    
    return jsonify(products_list), 200

# Get single product
@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

# Get all categories
@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [category.to_dict() for category in categories]
    return jsonify(categories_list), 200

# ... (rest of product routes)
