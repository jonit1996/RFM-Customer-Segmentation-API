def calculate_rfm_score(rfm_data):
    # Calculate quantiles for Recency, Frequency, and Monetary
    quantiles = rfm_data.quantile(q=[0.25, 0.5, 0.75])

    # Function to calculate the R, F, or M score
    def score_rfm(value, metric, quantiles, is_recency=True):
        if is_recency:
            # Lower recency is better (more recent)
            if value <= quantiles[metric][0.25]:
                return 1
            elif value <= quantiles[metric][0.5]:
                return 2
            elif value <= quantiles[metric][0.75]:
                return 3
            else:
                return 4
        else:
            # Higher frequency or monetary value is better
            if value <= quantiles[metric][0.25]:
                return 4
            elif value <= quantiles[metric][0.5]:
                return 3
            elif value <= quantiles[metric][0.75]:
                return 2
            else:
                return 1

    # Apply the score function to Recency, Frequency, and Monetary
    rfm_data['R_Quartile'] = rfm_data['Recency'].apply(score_rfm, args=('Recency', quantiles, True))
    rfm_data['F_Quartile'] = rfm_data['Frequency'].apply(score_rfm, args=('Frequency', quantiles, False))
    rfm_data['M_Quartile'] = rfm_data['Monetary'].apply(score_rfm, args=('Monetary', quantiles, False))

    # Create a combined RFM score by summing R, F, and M quartile scores
    rfm_data['RFM_Score'] = rfm_data['R_Quartile'] + rfm_data['F_Quartile'] + rfm_data['M_Quartile']
    
    return rfm_data['RFM_Score']

# Example of how to call the function
# rfm_segmentation = calculate_rfm_score(rfm_segmentation)
