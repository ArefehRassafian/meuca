Django E-Commerce

A full-featured e-commerce web application developed using Python and Django.
The project provides the main features required for an online store, including user authentication, product management, shopping cart, order management, payment flow, and content management.

✨ Features

👤 User & Account Management

- User registration and login
- User authentication using Django
- Email and phone number support
- Phone number verification
- Password change
- Password recovery
- User profile management
- Profile picture support
- Address management
- Contact us functionality

🛍️ Product Management

- Product listing
- Product details
- Product categories
- Multiple images for each product
- Product search
- Category filtering
- Price sorting
- Discounted products
- Automatic final price calculation
- Product pagination
- Product publishing system

🛒 Shopping Cart

- Add products to cart
- Increase/decrease product quantity
- Remove products from cart
- Session-based shopping cart
- Automatic price calculation
- Discount calculation
- Tax calculation
- Shipping cost calculation

📦 Order Management

- Create orders
- Order items management
- Select delivery address
- Receiver information
- Order status management
- Order tracking code
- Order history
- Order details
- Paid/unpaid order management

💳 Payment

- Payment page
- Payment confirmation flow
- Payment status management
- Payment timestamp
- Unique order tracking code
- Cart clearing after successful payment
- Order confirmation email

📝 Content Management

- About Us section
- Website rules
- Frequently Asked Questions (FAQ)
- Website banners
- Blog posts
- Blog details
- Multiple images for blog posts
- Persian/Jalali date support

⚙️ Admin Panel

The project uses the built-in Django Admin Panel to manage:

- Users
- Addresses
- Products
- Categories
- Product images
- Orders
- Order items
- Website settings
- Rules
- FAQs
- Banners
- Blog posts
- Blog images

---

🛠️ Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Django ORM
- Django Authentication
- Django Admin
- Session
- SQLite / Configured Database
- jdatetime

The project was developed using PyCharm as the primary IDE.

---

🏗️ Project Structure

project/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── orders_cart/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── main/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

📁 Applications

"accounts"

Handles all user-related functionality, including:

- Registration
- Login and logout
- User profiles
- Password management
- Password recovery
- Addresses
- Contact messages

"products"

Responsible for the product catalog:

- Products
- Categories
- Product images
- Discounts
- Search
- Filtering
- Sorting
- Pagination

"orders_cart"

Handles the shopping and ordering process:

- Shopping cart
- Cart operations
- Checkout
- Orders
- Order items
- Taxes
- Shipping costs
- Payment flow
- Order tracking

"main"

Manages the general content of the website:

- About Us
- Rules
- FAQs
- Website settings
- Banners
- Blog

---

🚀 Installation

1. Clone the Repository

git clone <repository-url>
cd <project-directory>

2. Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

Linux / macOS

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Apply Database Migrations

python manage.py makemigrations
python manage.py migrate

5. Create a Superuser

python manage.py createsuperuser

Follow the instructions in the terminal to create the administrator account.

6. Run the Development Server

python manage.py runserver

Open the following address in your browser:

http://127.0.0.1:8000/

The Django Admin Panel is available at:

http://127.0.0.1:8000/admin/


🛒 Shopping Flow

The main shopping process works as follows:

Browse Products
      ↓
View Product Details
      ↓
Add Product to Cart
      ↓
Review Shopping Cart
      ↓
Login / Authentication
      ↓
Select Delivery Address
      ↓
Create Order
      ↓
Calculate Discount + Tax + Shipping
      ↓
Payment
      ↓
Confirm Order
      ↓
Receive Tracking Code

---

🔗 Main Routes

Feature| URL
Product List| "/product_list/"
Product Details| "/product_details/<id>"
Discounted Products| "/discounted_products_list/"
Categories| "/categories_list/<id>"
Login| "/account/login/"
Sign Up| "/account/signup/"
Profile| "/account/profile/"
Shopping Cart| "/oc/cart/"
Checkout| "/oc/checkout/"
Orders| "/oc/order_list/"
Blog| "/main/blog_list/"
Admin Panel| "/admin/"

---

💰 Order Price Calculation

The final order price is calculated based on:

Discounted Products Subtotal
            +
Tax
            +
Shipping Cost
            =
Final Order Price

Products can have individual discounts, while the order also includes the configured tax percentage and shipping cost.

---

🔐 Security

The project uses several Django features for authentication and access control, including:

- Django Authentication
- Login-required views
- Session management
- Form validation
- Model validation
- Database constraints
- User-specific addresses
- User-specific order history

Sensitive configuration values should not be stored directly in the Git repository.

For production environments, sensitive information such as secret keys, database credentials, email credentials, and payment gateway credentials should be stored using environment variables.

---

📄 Requirements

All Python dependencies are listed in:

requirements.txt

Install them with:

pip install -r requirements.txt

---

📌 Project Status

This project is a Django-based e-commerce application that implements the core functionality of an online store, including user management, product catalog, shopping cart, order processing, payment flow, and content management.

It can be further extended with additional features and prepared for production deployment.

---

👨‍💻 Developer

Developed with ❤️ using Python, Django, HTML, CSS, JavaScript, and Bootstrap.