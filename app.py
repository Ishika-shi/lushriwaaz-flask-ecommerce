# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db_config import mysql, init_app
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
app.secret_key = 'lushriwaaz'
bcrypt = Bcrypt(app)
init_app(app)

@app.context_processor
def inject_cart_count():
    count = 0
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) as c FROM cart WHERE user_id=%s", (session['user_id'],))
        count = cur.fetchone()['c']
        cur.close()
    return dict(cart_count=count)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

# API: add product to cart (POST)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        # for now, create a guest user session or ask to login
        return jsonify({'status':'error','message':'login required'}), 401

    data = request.json
    product_id = data.get('product_id')
    qty = int(data.get('quantity', 1))
    user_id = session['user_id']

    cur = mysql.connection.cursor()
    # Check if exists -> update quantity
    cur.execute("SELECT id, quantity FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    row = cur.fetchone()
    if row:
        new_q = row['quantity'] + qty
        cur.execute("UPDATE cart SET quantity=%s WHERE id=%s", (new_q, row['id']))
    else:
        cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, qty))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status':'ok'})

# View cart
@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("""
      SELECT c.id as cart_id, p.id as product_id, p.name, p.price, c.quantity, p.image_path
      FROM cart c JOIN products p ON c.product_id = p.id
      WHERE c.user_id = %s
    """, (session['user_id'],))
    items = cur.fetchall()
    cur.close()
    return render_template('cart.html', cart_items=items)

# Place order (POST)
@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('order_success'))
    data = request.form
    shipping = data.get('address')
    user_id = session['user_id']

    # get cart
    cur = mysql.connection.cursor()
    cur.execute("""
      SELECT p.id, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.id
      WHERE c.user_id = %s
    """, (user_id,))
    items = cur.fetchall()
    if not items:
        cur.close()
        return "Cart empty", 400

    total = sum(item['price'] * item['quantity'] for item in items)
    product_list = json.dumps([{'product_id': item['id'], 'qty': item['quantity'], 'price': float(item['price'])} for item in items])

    cur.execute("INSERT INTO orders (user_id, product_list, total_amount, shipping_address) VALUES (%s, %s, %s, %s)",
                (user_id, product_list, total, shipping))
    mysql.connection.commit()
    # clear cart
    cur.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('order_success'))

@app.route('/order_success')
def order_success():
    return render_template('order_success.html')

# Simple signup/login 
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing = cur.fetchone()
        if existing:
            cur.close()
            return "Email already exists! Try logging in."

        cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name,email,pw_hash))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']; password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Search products
@app.route('/search')
def search():
    q = request.args.get('query', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE name LIKE %s OR category LIKE %s OR short_desc LIKE %s", 
                (f'%{q}%', f'%{q}%', f'%{q}%'))
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

# Category filter
@app.route('/category/<cat>')
def category(cat):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE category=%s", (cat,))
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Fetch user info
    cur.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()

    # Fetch orders for that user
    cur.execute("""
        SELECT id, total_amount, shipping_address, created_at 
        FROM orders 
        WHERE user_id=%s 
        ORDER BY created_at DESC
    """, (user_id,))
    orders = cur.fetchall()
    cur.close()

    return render_template('profile.html', user=user, orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
