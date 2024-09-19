import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Blueprint, send_file
from model.customer import Customer
import os
import pandas as pd

viz_blueprint = Blueprint('visualizations', __name__)

@viz_blueprint.route('/customer_groups', methods=['GET'])
def plot_customer_groups():
    # Query customer data
    customer_data = Customer.query.all()
    df = pd.DataFrame([{
        "customer_group": c.customer_group
    } for c in customer_data])
    
    # Plot customer groups
    segment_counts = df['customer_group'].value_counts()
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')

    
    # Save plot to file
    plot_path = 'static/visualizations/customer_groups.png'
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path, transparent=True)
    plt.close(fig)
    
    return send_file(plot_path, mimetype='image/png')
