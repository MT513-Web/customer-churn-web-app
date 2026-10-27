# 📊 Customer Churn Prediction Engine

A simple Streamlit app to explore customer churn risk. Enter one customer's details, or upload a CSV to check many customers at once.

**Live demo:** [Open the app](https://customer-churn-web-app-debn7cekcrda8mwprjtova.streamlit.app)


## What it does
- **Single Prediction:** enter tenure, monthly charges and support calls to get a churn probability and a risk level (Low, Medium or High).
- **Batch Upload (CSV):** upload many customers, rows with missing values are skipped, and download the results sorted by risk.
- **Model Insights:** see the model type, its inputs and a feature importance chart.
- **How to Use:** a short guide inside the app.

## CSV format
Your file needs these exact columns:
`tenure_months`, `monthly_charges`, `support_calls`

## Tech stack
Python, Streamlit, Scikit-Learn, Joblib, Pandas

## About the model
- The model is trained on a sample dataset for demonstration.
- Risk levels (40% for medium, 70% for high) are simple rules of thumb, not calibrated thresholds.
- This is a portfolio demo and has not been validated for real business decisions.

## Run locally
```bash
git clone https://github.com/MT513-Web/customer-churn-web-app.git
cd customer-churn-web-app
pip install -r requirements.txt
streamlit run app.py
```

Built by Ayesha Afzal 🤍 If you find it useful, feel free to give it a star.