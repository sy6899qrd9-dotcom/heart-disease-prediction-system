# import pickle

# model = pickle.load(open("model.pkl", "rb"))
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import os
import pickle


model = pickle.load(open("model.pkl", "rb"))

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="🫀",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.main {
    background-color: #F8FAFC;
}
h1, h2, h3 {
    color: #0A2647;
}
.stButton>button {
    background-color: #2EC4B6;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("🫀 HeartCare AI")
st.sidebar.markdown('by HARPREET SINGH')
page = st.sidebar.radio("Navigation", ["Home", "Prediction", "Reports", "About"])

# -------------------- HOME PAGE --------------------
if page == "Home":
    st.title("🫀 Heart Disease Prediction 🫀")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Fast. Reliable. Accurate.

        Predict cardiovascular risk using advanced machine learning.

        #### Features:
        - 🧠 Real Prediction  
        - 📊 Real-time Analysis  
        - 🔐 Secure Data  
        - 📄 Export Reports  
        """)

        if st.button("🚀 Start Prediction"):
            st.session_state.page = "Prediction"

    with col2:
        st.image("/Users/apple/Downloads/d6ea22d0cae6bdd40e806347b0f2b1bc-2.jpg", width=300)

        
       
    st.markdown("---")

    st.subheader("🩺 How It Works")
    col1, col2, col3, col4 = st.columns(4)

    col1.info("1. Enter patient data")
    col2.info("2. Run prediction")
    col3.info("3. View results")
    col4.info("4. Download report")

# -------------------- PREDICTION PAGE --------------------
elif page == "Prediction":
    st.title("🧪 Heart Disease Prediction")

    st.markdown("### Enter Patient Details")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name")
        age = st.slider("Age", 20, 100, 50)
        sex = st.selectbox("Gender", ["Male", "Female"])
        cp = st.selectbox("Chest Pain Type", ["Typical", "Atypical", "Non-anginal", "Asymptomatic"])
        trestbps = st.slider("Resting Blood Pressure", 80, 200, 120)
        chol = st.slider("Cholesterol", 100, 400, 200)

    with col2:
        fbs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"])
        restecg = st.selectbox("Resting ECG", ["Normal", "ST-T abnormality", "Left ventricular hypertrophy"])
        thalach = st.slider("Max Heart Rate", 60, 220, 150)
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
        oldpeak = st.slider("ST Depression", 0.0, 6.0, 1.0)

    st.markdown("---")

    if st.button("🔍 Predict Risk"):
        if not patient_name:
            st.warning("Please enter patient name.")
            st.stop()

        gender = 1 if sex == "Male" else 0

        cp_map = {
            "Typical": 0,
            "Atypical": 1,
            "Non-anginal": 2,
            "Asymptomatic": 3
        }

        fbs_map = {
            "No": 0,
            "Yes": 1
        }

        ecg_map = {
            "Normal": 0,
            "ST-T abnormality": 1,
            "Left ventricular hypertrophy": 2
        }

        angina_map = {
            "No": 0,
            "Yes": 1
        }

        input_data = [[
            age,
            gender,
            cp_map[cp],
            trestbps,
            chol,
            fbs_map[fbs],
            ecg_map[restecg],
            thalach,
            angina_map[exang],
            oldpeak
       ]]

        prediction = model.predict(input_data)[0]

        risk_score = model.predict_proba(input_data)[0][1]

        st.session_state['risk'] = risk_score

        st.success("Prediction completed!")

        if risk_score < 0.3:
            st.session_state['result'] = ("Low Risk", "green")
        elif risk_score < 0.7:
            st.session_state['result'] = ("Moderate Risk", "orange")
        else:
            st.session_state['result'] = ("High Risk", "red")
            # SAVE RECORD
        record = {
            "Date & Time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Patient Name": patient_name,
            "Age": age,
            "Gender": sex,
            "Risk": st.session_state['result'][0]
        }
        
        df_record = pd.DataFrame([record])

        if os.path.exists("patient_record.csv"):
            df_record.to_csv(
                "patient_record.csv",
                mode="a",
                header=False,
                index=False
            )
        else:
            df_record.to_csv(
                "patient_record.csv",
                index=False
            )
        st.success("Record saved successfully ! ")

# -------------------- RESULTS DISPLAY --------------------
    if 'result' in st.session_state:
        result, color = st.session_state['result']
        risk = st.session_state['risk']

        st.markdown("## 📊 Results")

        st.markdown(f"""
        <div class="card">
            <h3>Patient: {patient_name}</h3>
            <h3 style="color:{color};">{result}</h3>
            <p>Risk Score: {risk:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(risk * 100))

        st.markdown("### 🧠 Insights")
        if risk > 0.7:
            st.error("High cholesterol and heart rate may increase risk.")
        elif risk > 0.3:
            st.warning("Moderate risk detected. Monitor lifestyle.")
        else:
            st.success("Healthy condition. Keep maintaining your lifestyle.")

# -------------------- REPORTS PAGE --------------------
elif page == "Reports":
    st.title("📁 Patient Reports")


   

    st.info("Reports are being saved here")
    
    
        
    try:
        reports = pd.read_csv("patient_record.csv")
        
        reports.index = reports.index + 1

        st.dataframe(
        reports,
        use_container_width=True
    )
        

    except:
        st.info("No records available yet.")

    if os.path.exists("patiennt_record.csv"):
        with open("patient_record.csv", "rb") as file:
            st.download_button(
            label="📥 Download Records",
            data=file,
            file_name="patient_record.csv",
            mime="text/csv"
            )



# -------------------- ABOUT PAGE --------------------
elif page == "About":
    st.title("ℹ️ About This System")

    st.markdown("""
    This Heart Disease Prediction System uses machine learning 
    to assess cardiovascular risk based on clinical inputs.

    ### 👨‍⚕️ Features:
    - Assist doctors  
    - Early detection  
    - Preventive healthcare  

    ### ⚙️ Tech Used:
    - Streamlit  
    - Python  
    - Machine Learning  
                











                
















                                                                                                                    Managed By: HARPREET SINGH
    """)
        