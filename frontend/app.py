import streamlit as st
import pandas as pd
import requests
import json

st.title("🏥 Medical Note Structurer")

uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    results = []

    with st.spinner("Extracting info from notes..."):
        for _, row in df.iterrows():
                response = requests.post(
                    "http://localhost:8000/extract/", data={"note": row["note"]}
                    )
                
                extracted = response.json()["structured"]
                try:
                    structured = json.loads(extracted)
                except:
                    structured = {"symptoms": "N/A", "diagnosis": "N/A", "medications": "N/A", "follow_up_instructions": "N/A"}
                
                results.append({
                    "patient_id": row["patient_id"],
                    **structured
                })

    result_df = pd.DataFrame(results)
    st.success("Extraction complete!")
    
st.download_button(
    "Download Structured Notes", result_df.to_csv(index=False), file_name="structured_notes.csv", mime="text/csv"
)      
