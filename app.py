import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ---------------------- Sample Data Generation ----------------------
def generate_sample_vitals():
    now = datetime.now()
    time_range = [now - timedelta(hours=i) for i in range(23, -1, -1)]
    heart_rate = np.random.normal(loc=75, scale=5, size=24).round(1)
    systolic = np.random.normal(loc=120, scale=10, size=24).round(1)
    diastolic = np.random.normal(loc=80, scale=5, size=24).round(1)
    spo2 = np.random.normal(loc=98, scale=1, size=24).round(1)
    temperature = np.random.normal(loc=98.6, scale=0.5, size=24).round(1)

    return pd.DataFrame({
        "Timestamp": time_range,
        "Heart Rate (BPM)": heart_rate,
        "Systolic BP (mmHg)": systolic,
        "Diastolic BP (mmHg)": diastolic,
        "SpO2 (%)": spo2,
        "Temperature (F)": temperature
    })

# ---------------------- Static Data ----------------------
medical_conditions = {
    "Diabetes": 1,
    "Hypertension": 1,
    "Arthritis": 0,
    "Asthma": 0,
    "Heart Disease": 1,
    "Others": 0
}

medication_schedule = [
    {"Medicine": "Aspirin", "Dosage": "75mg", "Time": "8:00 AM"},
    {"Medicine": "Metformin", "Dosage": "500mg", "Time": "12:00 PM"},
    {"Medicine": "Atorvastatin", "Dosage": "10mg", "Time": "8:00 PM"}
]

# Patient Profile
patient_profile = {
    "Name": "John Doe",
    "Age": 72,
    "Gender": "Male",
    "Blood Group": "B+",
    "Allergies": "None",
    "Emergency Contact": "Jane Doe (+1234567890)",
    "Address": "123 Elderly Lane, Healthville",
    "Assigned Doctor": "Dr. Smith, General Medicine"
}

# ---------------------- Streamlit App ----------------------
st.set_page_config(page_title="Elderly Health Monitor", layout="wide")
st.title("🩺 Elderly Patient Health Dashboard")

vitals_df = generate_sample_vitals()
latest_vital = vitals_df.iloc[-1]

# ---------------------- Patient Profile ----------------------
st.header("👤 Patient Profile")
for key, value in patient_profile.items():
    st.markdown(f"**{key}:** {value}")

# ---------------------- Display Real-time Metrics ----------------------
st.header("🔴 Real-time Vitals")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Heart Rate", f"{latest_vital['Heart Rate (BPM)']} BPM")
col2.metric("Blood Pressure", f"{latest_vital['Systolic BP (mmHg)']}/{latest_vital['Diastolic BP (mmHg)']} mmHg")
col3.metric("SpO2", f"{latest_vital['SpO2 (%)']} %")
col4.metric("Temperature", f"{latest_vital['Temperature (F)']} °F")

# ---------------------- Medical History ----------------------
st.header("📋 Medical History")
condition_df = pd.DataFrame.from_dict(medical_conditions, orient='index', columns=['Has Condition'])
condition_df = condition_df.reset_index().rename(columns={'index': 'Condition'})
pie_fig = px.pie(condition_df[condition_df['Has Condition'] == 1], names='Condition', title='Existing Medical Conditions')
st.plotly_chart(pie_fig, use_container_width=True)

# ---------------------- Medication Schedule ----------------------
st.header("💊 Medication Schedule")
med_df = pd.DataFrame(medication_schedule)
st.table(med_df)

# ---------------------- Graphs for Vitals ----------------------
st.header("📈 Vitals Trend (Last 24 Hours)")

fig1 = px.line(vitals_df, x='Timestamp', y='Heart Rate (BPM)', title='Heart Rate Over Time', markers=True)
fig2 = px.line(vitals_df, x='Timestamp', y=['Systolic BP (mmHg)', 'Diastolic BP (mmHg)'],
               title='Blood Pressure Over Time', markers=True)
fig3 = px.line(vitals_df, x='Timestamp', y='SpO2 (%)', title='SpO2 Over Time', markers=True)
fig4 = px.line(vitals_df, x='Timestamp', y='Temperature (F)', title='Body Temperature Over Time', markers=True)
fig5 = px.bar(vitals_df, x='Timestamp', y='Heart Rate (BPM)', title='Heart Rate Distribution')
fig6 = px.area(vitals_df, x='Timestamp', y='Temperature (F)', title='Temperature Area Chart')
fig7 = px.scatter(vitals_df, x='Systolic BP (mmHg)', y='Diastolic BP (mmHg)',
                  title='Blood Pressure Scatter Plot', size='Heart Rate (BPM)', color='SpO2 (%)')
fig8 = px.histogram(vitals_df, x='Heart Rate (BPM)', title='Heart Rate Histogram')
fig9 = px.box(vitals_df, y='Temperature (F)', title='Temperature Box Plot')
fig10 = px.scatter_matrix(vitals_df, dimensions=['Heart Rate (BPM)', 'Systolic BP (mmHg)', 'Diastolic BP (mmHg)', 'SpO2 (%)'],
                         title='Vitals Scatter Matrix')

r1c1, r1c2 = st.columns(2)
r1c1.plotly_chart(fig1, use_container_width=True)
r1c2.plotly_chart(fig2, use_container_width=True)

r2c1, r2c2 = st.columns(2)
r2c1.plotly_chart(fig3, use_container_width=True)
r2c2.plotly_chart(fig4, use_container_width=True)

r3c1, r3c2 = st.columns(2)
r3c1.plotly_chart(fig5, use_container_width=True)
r3c2.plotly_chart(fig6, use_container_width=True)

r4c1, r4c2 = st.columns(2)
r4c1.plotly_chart(fig7, use_container_width=True)
r4c2.plotly_chart(fig8, use_container_width=True)

r5c1, r5c2 = st.columns(2)
r5c1.plotly_chart(fig9, use_container_width=True)
r5c2.plotly_chart(fig10, use_container_width=True)

# ---------------------- Error Handling ----------------------
try:
    assert not vitals_df.empty, "Vitals data is missing."
    assert all(col in vitals_df.columns for col in ["Heart Rate (BPM)", "Systolic BP (mmHg)", "Diastolic BP (mmHg)", "SpO2 (%)"]), "Missing vital sign columns."
except AssertionError as e:
    st.error(f"Data Error: {e}")

# ---------------------- Footer ----------------------
st.markdown("---")
st.markdown("👨‍⚕️ *Developed for remote elderly patient health tracking.*")
