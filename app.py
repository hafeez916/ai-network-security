import streamlit as st
import pandas as pd
import joblib
from utils.feature_extraction import extract_features

st.title("🛡️ URL - BASED INTRUTION DETECTION SYSTEM ")

model = joblib.load("model/rf_model.pkl")

option = st.radio("Choose Mode:", ("Upload URLs", "Enter Single URL"))

if option == "Upload URLs":
    uploaded_file = st.file_uploader("Upload CSV with column 'url'", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["features"] = df["url"].apply(extract_features)
        df["prediction"] = df["features"].apply(lambda x: model.predict([x])[0])
        df["result"] = df["prediction"].map({1: "🚫 UNSAFE URL FOUND", 0: "✅ YOUR LINK IS SECURE"})
        st.dataframe(df[["url", "result"]])
else:
    url = st.text_input("Enter a URL:")
    if url:
        features = extract_features(url)
        pred = model.predict([features])[0]

        if pred:
            # Malicious case
            st.markdown(
                f"""
                <div style='background-color:#ffcccc; padding:20px; border-radius:10px; border:2px solid red;'>
                    <h3 style='color:red;'>⚠ Warning: Malicious Link Detected</h3>
                    <p><strong>Prediction:</strong> 🔴 UNSAFE URL FOUND</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Safe case
            st.markdown(
                f"""
                <div style='background-color:#ccffcc; padding:20px; border-radius:10px; border:2px solid green;'>
                    <h3 style='color:green;'>✅ Safe Link</h3>
                    <p><strong>Prediction:</strong> YOUR LINK IS SECURE</p>
                </div>
                """,
                unsafe_allow_html=True
            )
