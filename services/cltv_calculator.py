def calculate_clv(data):
    # A basic CLV formula based on frequency and monetary value
    # CLV = frequency * monetary * average lifespan of customer (assumed as 12 months here)
    average_lifespan = 12
    data['clv'] = data['Frequency'] * data['Monetary'] * average_lifespan
    return data['clv']
