# 📊 Customer Churn Prediction Engine

Hey everyone! Welcome to my machine learning portfolio project. This is an interactive web app built using **Streamlit** that helps explore customer churn risk, handle batch data uploads, and inspect model insights seamlessly.

 **Live Demo:** [Check out the live app here!](https://customer-churn-web-app-debn7cekcrda8mwprjtova.streamlit.app)

---

## Features Inside the App
- **Single Prediction Tab:** Instantly check an individual customer's churn risk using key behavioral metrics with clear visual indicators.
- **Batch Upload (CSV) Tab:** Upload bulk customer data in CSV format, handle missing rows automatically, and download results instantly.
- **Model Insights Tab:** Look under the hood at the model architecture and explore an interactive feature importance chart.
- **How to Use Tab:** Built-in guidance for a smooth user experience.

---

## Tech Stack & Tools
- **Python**
- **Streamlit** (Interactive Web UI)
- **Scikit-Learn** (ML Pipeline)
- **Joblib** (Model Persistence)
- **Pandas & NumPy** (Data Processing)

---

## A Quick Note on the Model & Risk Thresholds
- The underlying model is trained on a sample dataset for demonstration and portfolio purposes.
- Risk levels (such as 40% for medium risk and 70% for high risk) are implemented as simple business rules of thumb / working assumptions rather than strict statistical cutoffs.

---

## Local Setup & Installation
If you want to run this project locally on your machine, follow these simple steps:

## 1. **Clone the repository:**
   ```bash
git clone https://github.com/MT513-Web/customer-churn-web-app.git
```
## 2. Install the required dependencies:
```
pip install -r requirements.txt
```

## 3. Run the Streamlit app:
```
streamlit run app.py
```

---
⭐ *If you found this project helpful or interesting, feel free to give it a star! Built with passion by Ayesha Afzal* 🤍