from flask import Flask, render_template
from routes.shop_routes import shop_bp

app = Flask(_name_)

# Register the blueprint
app.register_blueprint(shop_bp)

# Main routes
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

# Run the app (when running locally, not on Render)
if _name_ == '_main_':
    app.run(debug=True)