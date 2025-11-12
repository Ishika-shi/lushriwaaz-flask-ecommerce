# lushRiwaaz — Full-Stack E-commerce Website

A dynamic **Flask + MySQL** e-commerce web application developed for *lushRiwaaz*, a home aesthetics brand offering bedsheets, cushions, carpets, and AC covers.  
Users can browse products, add items to cart, and place orders through a clean, responsive interface.

## Features

- **Product Browsing:** View products by category (Bedsheets, Cushions, Carpets, AC Covers)
- **User Authentication:** Signup/Login with password hashing (Flask-Bcrypt)
- **Shopping Cart:** Add, update, and remove products dynamically
- **Order Placement:** Place orders and clear cart on confirmation
- **Search & Filter:** Search products and filter by category
- **Responsive Design:** Clean, modern UI using HTML, CSS, and JS
- **Database Integration:** MySQL for products, users, cart, and order management

## Tech Stack

Technology stack used:
-> **Frontend**: HTML, CSS, JavaScript, Jinja2 
-> **Backend** : Python (Flask Framework) 
-> **Database**: MySQL 
-> **Authentication**: Flask-Bcrypt, Flask Sessions 
-> **Tools** : MySQL Workbench, VS Code 

##  Project Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ishika/lushriwaaz.git
   cd lushriwaaz
````

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate      # on Windows
   ```

3. **Install dependencies**

   ```bash
   pip install flask flask-mysqldb flask-bcrypt
   ```

4. **Set up MySQL database**

   * Open MySQL Workbench
   * Create a new database (e.g., `lushriwaaz_db`)
   * Run the provided `products.sql` file to insert sample data

5. **Run the Flask app**

   ```bash
   python app.py
   ```

6. **Open the website**

   * Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)



⭐ *If you like this project, don’t forget to give it a star on GitHub!*