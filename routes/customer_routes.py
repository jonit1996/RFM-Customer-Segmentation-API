from werkzeug.utils import secure_filename
import os
import pandas as pd
from services.cltv_calculator import calculate_clv
from services.ml_predictor import predict_customer_group
from services.rfm_score import calculate_rfm_score
from flask import Blueprint, request, jsonify, redirect, url_for, render_template


customer_blueprint = Blueprint('customer', __name__)


# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@customer_blueprint.route('/upload', methods=['POST'])
def upload_data():
    from model.db import db
    from model.customer import Customer

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process CSV File (expected to have customer_id, recency, frequency, monetary)
        data = pd.read_csv(filepath)
        
        if not {'CustomerID', 'Recency', 'Frequency', 'Monetary'}.issubset(data.columns):
            return jsonify({"error": "CSV must contain columns: customer_id, recency, frequency, monetary"}), 400

        # Calculate Customer Lifetime Value (CLV)
        data['clv'] = calculate_clv(data)

        # Calculate RFM Score
        data['rfm_score'] = calculate_rfm_score(data)

        # Predict customer groups
        customer_groups = predict_customer_group(data[['Recency', 'Frequency', 'Monetary']])
        data['customer_group'] = customer_groups

        # Store the data in the database
        for _, row in data.iterrows():
            customer = Customer(
                customer_id=row['CustomerID'],
                recency=row['Recency'],
                frequency=row['Frequency'],
                monetary=row['Monetary'],
                rfm_score=row['rfm_score'],
                customer_group=row['customer_group'],
                clv=row['clv']
            )
            db.session.add(customer)
        db.session.commit()

        # Redirect to the results page
        return redirect(url_for('customer.display_results'))
    else:
        return jsonify({"error": "Invalid file format, please upload CSV."}), 400

    #     return jsonify({"message": "Data processed and customer segmentation done!"}), 200
    # else:
    #     return jsonify({"error": "Invalid file format, please upload CSV."}), 400


@customer_blueprint.route('/from_db', methods=['POST'])
def process_from_db():
    from model.db import db
    from model.customer import Customer
    # Fetch data from MySQL (assuming the relevant table is already created with the necessary columns)
    customers = Customer.query.all()
    
    if not customers:
        return jsonify({"error": "No customers found in the database"}), 404
    
    # Convert DB data to pandas DataFrame for further processing
    data = pd.DataFrame([{
        'customer_id': c.customer_id,
        'recency': c.recency,
        'frequency': c.frequency,
        'monetary': c.monetary
    } for c in customers])

    # Calculate Customer Lifetime Value (CLV)
    data['clv'] = calculate_clv(data)

    # Predict customer groups
    customer_groups = predict_customer_group(data[['Recency', 'Frequency', 'Monetary']])
    data['customer_group'] = customer_groups

    # Update customer groups in the DB
    for index, row in data.iterrows():
        customer = Customer.query.filter_by(customer_id=row['customer_id']).first()
        customer.customer_group = row['customer_group']
        customer.clv = row['clv']
    db.session.commit()

    return jsonify({"message": "Customer data processed and segmented!"}), 200

@customer_blueprint.route('/search/<customer_id>', methods=['GET'])
def search_customer(customer_id):
    from model.customer import Customer
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        return jsonify({
            "customer_id": customer.customer_id,
            "Recency": customer.recency,
            "Frequency": customer.frequency,
            "Monetary": customer.monetary,
            "rfm_score": customer.rfm_score,
            "customer_group": customer.customer_group,
            "clv": customer.clv
        }), 200
    else:
        return jsonify({"error": "Customer not found"}), 404

@customer_blueprint.route('/results', methods=['GET'])
def display_results():
    return render_template('results.html')


# @customer_blueprint.route('/customers', methods=['GET'])
# def get_customers():
#     from model.customer import Customer
#     customers = Customer.query.all()
#     df = pd.DataFrame([{
#         "customer_id": c.customer_id,
#         "recency": c.recency,
#         "frequency": c.frequency,
#         "monetary": c.monetary,
#         "rfm_score": c.rfm_score,
#         "customer_group": c.customer_group,
#         "clv": c.clv
#     } for c in customers])
    #df = pd.DataFrame([customer.to_dict() for customer in customers])
    
    # if not customers:
    #     return jsonify({"error": "No customers found"}), 404
    # table_html = df.to_html(classes='table table-striped', index=False)
    # data = df.to_dict(orient='records')
    # return jsonify(data), 200
    # customer_list = [customer.to_dict() for customer in customers]
    # return render_template('results.html', table_html=table_html)
    # return jsonify(customer_list), 200

