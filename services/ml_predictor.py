import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

def replace_numeric_labels(array):
    labels = {
        0: "Potential",
        1: "Hibernating",
        2: "At-Risk"
    }
    return np.vectorize(labels.get)(array)

def predict_customer_group(rfm_data):
    model = pickle.load(open('model/rf_model.pkl', 'rb'))
    scaler = pickle.load(open('model/scaler.pkl', 'rb'))
    scaled_rfm_data= scaler.transform(rfm_data)
    predictions = model.predict(scaled_rfm_data)
    predicted_labels = replace_numeric_labels(predictions)
    return predicted_labels
