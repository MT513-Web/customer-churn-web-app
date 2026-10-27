import streamlit as st
import pandas as pd
import joblib

# Page setup
st.markdown("""
<style>
div[data-testid="stMetric"] {background:#F6EBDD; padding:16px; border-radius:16px;}
.stButton > button {border-radius:12px;}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Customer Churn Prediction Engine",
    page_icon="📊",
    layout="wide"
)

# Load saved ML model
@st.cache_resource
def load_model():
    return joblib.load("churn_pipeline.joblib")

model = load_model()

# Simple and honest header
st.title("📊 Customer Churn Prediction Engine")
st.markdown("A simple tool to explore customer churn risk based on customer behavior and history.")
st.markdown("---")

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Single Prediction", 
    "📂 Batch Upload (CSV)", 
    "📊 Model Insights", 
    "📖 How to Use"
])

# --- TAB 1: SINGLE PREDICTION ---
with tab1:
    st.subheader("Evaluate Individual Customer Risk")
    
    # Session state initialization to prevent input reset bug
    default_values = {"tenure": 5, "charges": 5000.0, "calls": 2}
    for k, v in default_values.items():
        st.session_state.setdefault(k, v)

    def load_example():
        st.session_state.tenure = 4
        st.session_state.charges = 6500.0
        st.session_state.calls = 5

    st.button("Try an Example Customer", on_click=load_example)

    col1, col2 = st.columns(2)
    
    with col1:
        tenure_months = st.number_input("Tenure (Months)", min_value=0, max_value=120, key="tenure")
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=5000.0, key="charges")

    with col2:
        support_calls = st.number_input("Support Calls", min_value=0, max_value=50, key="calls")

    st.markdown("")
    if st.button("Run Prediction", type="primary", use_container_width=True):
        input_data = pd.DataFrame({
            'tenure_months': [tenure_months],
            'monthly_charges': [monthly_charges],
            'support_calls': [support_calls]
        })
        
        # Prediction & Probability
        prediction = model.predict(input_data)[0]
        if hasattr(model, "predict_proba"):
            churn_proba = model.predict_proba(input_data)[0][1] * 100
        else:
            churn_proba = 100.0 if prediction == 1 else 0.0

        st.markdown("---")
        st.subheader("Analysis Results")
        
        res_col1, res_col2 = st.columns([2, 1])
        
        with res_col1:
            if churn_proba >= 70:
                st.error("🔴 **High Churn Risk**")
                st.markdown("*Recommendation: Immediate outreach required. Offer special loyalty discounts.*")
            elif churn_proba >= 40:
                st.warning("🟡 **Medium Churn Risk**")
                st.markdown("*Recommendation: Monitor closely and send check-in emails.*")
            else:
                st.success("🟢 **Low Churn Risk**")
                st.markdown("*Recommendation: Customer is stable. Continue standard engagement.*")
                
            # Honest note reflecting rule-of-thumb nature
            st.caption("Risk levels (40% and 70%) are simple rules of thumb, not calibrated thresholds.")
                
        with res_col2:
            st.metric(label="Churn Probability", value=f"{churn_proba:.2f}%")
            st.progress(int(churn_proba))

# --- TAB 2: BATCH UPLOAD ---
with tab2:
    st.subheader("Batch Customer Churn Analysis")
    st.markdown("Upload a CSV file containing multiple customer records to evaluate risk in bulk.")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    # Initialize session state for batch results
    if "batch_result_df" not in st.session_state:
        st.session_state.batch_result_df = None

    # Clear previous results if file is removed
    if uploaded_file is None:
        st.session_state.batch_result_df = None

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write("Preview of Uploaded Data:", batch_df.head())
            
            required_cols = ['tenure_months', 'monthly_charges', 'support_calls']
            if all(col in batch_df.columns for col in required_cols):
                if st.button("Process Batch Predictions"):
                    before = len(batch_df)
                    batch_df.dropna(subset=required_cols, inplace=True)
                    if len(batch_df) < before:
                        st.warning(f"{before - len(batch_df)} rows with missing values were skipped.")
                    
                    batch_preds = model.predict(batch_df[required_cols])
                    if hasattr(model, "predict_proba"):
                        batch_probas = model.predict_proba(batch_df[required_cols])[:, 1] * 100
                    else:
                        batch_probas = [100.0 if p == 1 else 0.0 for p in batch_preds]
                    
                    batch_df['Churn_Probability_%'] = batch_probas
                    batch_df['Risk_Level'] = ['High' if p >= 70 else ('Medium' if p >= 40 else 'Low') for p in batch_probas]
                    st.session_state.batch_result_df = batch_df.sort_values(by='Churn_Probability_%', ascending=False)
            else:
                st.error(f"CSV file must contain exact columns: {required_cols}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # Display results and download button safely
    if st.session_state.batch_result_df is not None:
        st.success("Batch processing complete!")
        st.dataframe(st.session_state.batch_result_df)
        
        csv_data = st.session_state.batch_result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="churn_predictions_output.csv",
            mime="text/csv"
        )

# --- TAB 3: MODEL INSIGHTS ---
with tab3:
    st.subheader("Machine Learning Model Insights")
    st.markdown("Overview of the trained model architecture and feature importance.")
    
    col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    with st.container(border=True):
        st.markdown("**Model Type:** Scikit-Learn Pipeline")
    with st.container(border=True):
        st.markdown("**Persistence:** Saved via `joblib`")

with col_inf2:
    with st.container(border=True):
        st.markdown("**Input Features:** Tenure, Monthly Charges, Support Calls")
    with st.container(border=True):
        st.markdown("**Output:** Churn Status & Probability")
        
    try:
        classifier = model.named_steps.get('model') or model[-1]
        if hasattr(classifier, 'feature_importances_'):
            st.markdown("### Feature Importance Chart")
            importances = classifier.feature_importances_
            features = list(getattr(model, "feature_names_in_", ['tenure_months', 'monthly_charges', 'support_calls']))
            
            # Define fi_df here before passing to bar_chart
            fi_df = pd.DataFrame({'Feature': features, 'Importance': importances}).set_index('Feature')
            
            st.bar_chart(fi_df, color="#9A6F1E", horizontal=True)
    except Exception:
        pass

# --- TAB 4: HOW TO USE ---
with tab4:
    st.subheader("Guide for Users")
    st.markdown("""
    1. **Single Prediction Tab:** Check individual customer risk with a visual score.
    2. **Batch Upload Tab:** Upload a CSV file for bulk predictions and download results securely.
    3. **Model Insights Tab:** View model details and feature importance.
    """)