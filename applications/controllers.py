from flask import render_template, request, redirect, url_for, flash, current_app as app 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from applications.models import User, Category, Product, CartItems
from applications.database import db
from werkzeug.utils import secure_filename
import os

login_manager=LoginManager(app)
login_manager.login_view='user_login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid user','error')
    return render_template('user_login.html')

@app.route('/manager_login', methods=['GET','POST'])
def manager_login():
    if request.method=='POST':
        managername=request.form.get('managername')
        password=request.form.get('password')
        if managername=="sanjana" and password=="sanjana":
            return redirect(url_for('manager_dashboard'))
    return render_template('manager_login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username and password:
            user=User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Register Successfully!','success')
            return redirect(url_for('user_login'))
        else:
            flash('Enter correctly username and password','error')
    return render_template('register.html')

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    categories=Category.query.all()
    products=Product.query.all()
    return render_template('user_dashboard.html',username=current_user.username,categories=categories, products=products)

@app.route('/manager_dashboard')
def manager_dashboard():
    categories=Category.query.all()
    products=[]
    for category in categories:
        products.extend(category.products)
    return render_template('manager_dashboard.html', categories=categories, products=products)

@app.route('/add_category',methods=['GET','POST'])
def add_category():
    if request.method=='POST':
        category_name=request.form.get('category_name')
        if category_name:
            new_category=Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added successfully','success')
            return redirect(url_for('manager_dashboard'))
    return render_template('add_category.html')

@app.route('/edit_category/<int:category_id>',methods=['GET','POST'])
def edit_category(category_id):
    category=Category.query.get_or_404(category_id)
    if request.method=='POST':
        new_category_name=request.form.get('category_name')
        if new_category_name:
            category.name=new_category_name
            db.session.commit()
            flash('Category added successfully','success')
            return redirect(url_for('manager_dashboard'))
    return render_template('edit_category.html',category=category)

@app.route('/delete_category/<int:category_id>',methods=['GET','POST'])
def delete_category(category_id):
    category=Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully','success')
    return redirect(url_for('manager_dashboard'))

@app.route('/add_product_to_category/<int:category_id>',methods=['GET','POST'])
def add_product_to_category(category_id):
    category=Category.query.get_or_404(category_id)
    if request.method=='POST':
        product_name=request.form.get('product_name')
        quantity=request.form.get('quantity')
        price=request.form.get('price')
        description=request.form.get('description')
        image_filename=request.files.get('image')

        if not product_name or not quantity or not price or not description:
            flash('add fields','error')
            return redirect(url_for('add_product_to_category',category=category,category_id=category_id))

        try:
            quantity=int(quantity)
            price=float(price)
        except ValueError:
            flash('Quantity and price must be a valid numbers','error')
            return redirect(url_for('add_product_to_catgory',category=category,category_id=category_id))

        if image_filename:
            filename=secure_filename(image_filename.filename)
            image_filename.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        else:
            filename='default_product_image.jpg'
        new_product=Product(image_filename=filename,name=product_name,quantity=quantity,price=price,description=description,category_id=category_id)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully','success')
        return redirect(url_for('manager_dashboard'))
    return render_template('add_product_to_category.html',category=category,category_id=category_id)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/edit_product/<int:category_id>/<int:product_id>',methods=['GET','POST'])
def edit_product(category_id,product_id):
    category=Category.query.get_or_404(category_id)
    product=Product.query.get_or_404(product_id)
    if request.method=='POST':
        product.name=request.form.get('product_name')
        product.quantity=request.form.get('quantity')
        product.price=request.form.get('price')
        product.description=request.form.get('description')
        image_filename=request.files.get('image')

        if not product.name or not product.quantity or not product.price or not product.description:
            flash('add fields','error')
            return redirect(url_for('edit_product',category=category,category_id=category_id,product=product,product_id=product_id))

        try:
            product.quantity=int(product.quantity)
            product.price=float(product.price)
        except ValueError:
            flash('Quantity and price must be a valid numbers','error')
            return redirect(url_for('edit_product',category=category,category_id=category_id,product=product,product_id=product_id))

        if image_filename:
            filename=secure_filename(image_filename.filename)
            image_filename.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image=filename
        
        db.session.commit()
        flash('Product added successfully','success')
        return redirect(url_for('manager_dashboard'))
    return render_template('edit_product.html',category=category,category_id=category_id,product=product)

@app.route('/delete_product/<int:category_id>/<int:product_id>',methods=['GET','POST'])
def delete_product(category_id,product_id):
    product=Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully','success')
    return redirect(url_for('manager_dashboard'))

@app.route('/add_to_cart',methods=['GET','POST'])
def add_to_cart():
    if request.method=='POST':
        product_id=request.form.get('product_id')
        quantity=int(request.form.get('quantity',0))
        product=Product.query.get(product_id)
        if product and 1<=quantity<=product.quantity:
            cart_item=CartItems.query.filter_by(user_id=current_user.id,product_id=product_id).first()
            if cart_item:
                cart_item.quantity+=quantity
            else:
                cart_item=CartItems(user_id=current_user.id,product_id=product.id,quantity=quantity)
                db.session.add(cart_item)
            db.session.commit()
            flash(f'{product.name} added to cart','success')
        else:
            flash('Invalid quantity','error')
    return redirect(url_for('cart'))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        query=request.form.get('query','').strip()
        if not query:
            flash('please enter a query','warning')
            return redirect(url_for('search'))
        product_results=Product.query.filter(Product.name.ilike(f'%{query}%')).all()
        category_results=Category.query.filter(Category.name.ilike(f'%{query}%')).all()
        if not product_results and not category_results:
            flash('no result','info')
        return render_template('search.html',query=query,product_results=product_results,category_results=category_results)
    return render_template('search.html')

@app.route('/cart',methods=['GET','POST'])
def cart():
    if request.method=='POST':
        for item in current_user.cart_items:
            new_quantity=int(request.form.get('quantity_'+str(item.id),0))
            item.quantity=new_quantity
        db.session.commit()
        flash('Cart updated','success')
    cart_items=current_user.cart_items
    return render_template('cart.html',cart_items=cart_items)

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['GET','POST'])
def remove_from_cart(cart_item_id):
    cart_item=CartItems.query.get_or_404(cart_item_id)
    if cart_item.user_id==current_user.id:
        if cart_item.quantity>1:
            cart_item.quantity-=1
        else:
            db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed','success')
    else:
        flash('Item not found','error')
    return redirect(url_for('cart'))

@app.route('/buy_product', methods=['POST'])
def buy_product():
    if request.method=='POST':
        cart_items=CartItems.query.filter_by(user_id=current_user.id).all()
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
        flash('Puchase successful','success')
        
    cart_items=CartItems.query.filter_by(user_id=current_user.id).all()
    return render_template('buy_product.html',cart_items=cart_items)

@app.route('/logout')
def logout():
    logout_user
    return redirect(url_for('index'))