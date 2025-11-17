# app.py
import streamlit as st
from posture_model import analyze_video, train_dummy_model
import os
import pandas as pd

st.set_page_config(page_title="PostureSense+: Smart Exercise Detection", layout="centered")

# Ensure model exists
if not os.path.exists("python_app/data/posture_model.pkl"):
    train_dummy_model()

st.title("🏋️ PostureSense+: Smart Exercise Posture Detection")
st.write("Upload your exercise video for real-time posture evaluation.")

uploaded_file = st.file_uploader("Upload exercise video", type=["mp4", "mov", "avi", "mpeg4"])

if uploaded_file is not None:
    save_path = f"python_app/data/{uploaded_file.name}"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(save_path)

    with st.spinner("Analyzing posture..."):
        accuracy, feedback = analyze_video(save_path)

    st.success(f"**Posture Accuracy:** {accuracy}%")
    st.info(feedback)

    # Save progress to CSV for R dashboard
    df = pd.DataFrame([[uploaded_file.name, accuracy]], columns=["Video", "Accuracy"])
    progress_file = "python_app/data/progress.csv"
    if os.path.exists(progress_file):
        old = pd.read_csv(progress_file)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(progress_file, index=False)

st.markdown("---")
st.subheader("📊 View Progress Analytics (R Dashboard)")
st.write("Click below to open your R-powered progress dashboard.")

st.link_button("Open R Dashboard", "http://127.0.0.1:8080")  # R Shiny app link
