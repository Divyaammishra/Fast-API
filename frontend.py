import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/predict'

st.title('Insurance Premium category Predictor')

st.markdown('Enter your details below')

age = st.number_input('Age', min_value=1, max_value=119, value=24),
weight = st.number_input('Weight (KGs)', min_value=1.0, value=66.0)
height = st.number_input('Height (M)', min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input('Annual Income (LPA)', min_value=0.1, value=2.0)
smoker = st.selectbox('Are you smoker', options=[True, False])
city = st.text_input('City', value='Varanasi')
occupation = st.selectbox(
    'Occupation',
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

if st.button('Predict Premium Category'):
    input_data = {
        'age': age,
        'weight': weight,
        'height': height,
        'income_lpa': income_lpa,
        'smoker': smoker,
        'city': city,
        'occupation': occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f'Predicted Insurance Premium Category: **{result['predicted_category']}**')
        else:
            st.error(f'API Error: {response.status_code} - {response.text}')
    except requests.exceptions.ConnectionError:
        st.error('Could not connect to FastAPI server. Make sure it is running on port 800')             
