import streamlit as st
import train_and_predict

st.set_page_config(page_title="BDG WinGo Predictor", layout="centered")
st.title("🎯 BDG WinGo Predictor")

if st.button("🔮 Predict Now"):
    try:
        prediction = train_and_predict.match_pattern(
            train_and_predict.load_csv("10000_data.csv"),
            train_and_predict.load_csv("wingo_live_data.csv")[-20:]
        )
        if prediction:
            st.success(f"Prediction: {prediction}")
        else:
            st.warning("No strong match found in pattern.")
    except Exception as e:
        st.error(f"Error: {e}")
