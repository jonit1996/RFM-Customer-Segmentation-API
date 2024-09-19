from flask import Blueprint, jsonify, send_file, render_template
import pandas as pd
from model.customer import Customer
import json


fetchdata_blueprint = Blueprint('fetchdata', __name__)

@fetchdata_blueprint.route('/customer_data', methods=['GET'])
def get_customers():
    # Query customer data
    customers = Customer.query.all()
    df = pd.DataFrame([{
        "customer_id": c.customer_id,
        "recency": c.recency,
        "frequency": c.frequency,
        "monetary": c.monetary,
        "rfm_score": c.rfm_score,
        "customer_group": c.customer_group,
        "clv": c.clv
    } for c in customers])

    # Convert dataframe to dictionary
    df.to_csv('table.csv', index=False)
    data = df.to_dict(orient='records')
    file_path = "data/out.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    # return jsonify(data), 200
    return send_file(file_path, mimetype='application/json')

