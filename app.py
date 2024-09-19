from flask import Flask, render_template
from model.db import db
import mysql.connector

app = Flask(__name__)

# Configure the SQLAlchemy part of the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:163625@localhost/customer_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
# db = SQLAlchemy(app)
db.init_app(app)

# Call init_app to bind the Flask app to SQLAlchemy
# db.init_app(app)

# Import blueprints after the app and db are initialized to avoid circular imports
from routes.customer_routes import customer_blueprint
from routes.visualizations import viz_blueprint
from fetchdata import fetchdata_blueprint


# Register blueprints
app.register_blueprint(customer_blueprint, url_prefix='/customer')
app.register_blueprint(viz_blueprint, url_prefix='/visualizations')
app.register_blueprint(fetchdata_blueprint, url_prefix='/fetchdata')


mydb=mysql.connector.connect(
    host='localhost',
    user= 'root',
    password='163625',
    database='customer_db'
)
my_cursor= mydb.cursor(dictionary=True)


# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    my_cursor.execute("SELECT * FROM customers")
    customer= my_cursor.fetchall()
    return render_template('table.html', customer=customer)

# Create tables when running the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This creates the tables automatically in MySQL
    app.run(debug=True)
