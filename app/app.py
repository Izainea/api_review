import streamlit as st
import requests

# Función para realizar la solicitud POST a la API
def realizar_solicitud_post(url, data):
    try:
        response = requests.post(url, json=data)
        # Considera añadir headers si necesitas pasar un token de autorización
        # Ejemplo: response = requests.post(url, json=data, headers={"Authorization": "Bearer tu_token_aqui"})
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


st.title("Consulta de API para Modelo de Adultos")

# Formulario para introducir los datos requeridos por la API
with st.form("api_form"):
    age = st.number_input("Edad", min_value=1, value=21)
    workclass = st.selectbox("Clase de trabajo", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
    fnlwgt = st.number_input("fnlwgt", value=346478)
    education = st.selectbox("Educación", ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"])
    education_num = st.number_input("Número de educación", min_value=1, max_value=16, value=10)
    marital_status = st.selectbox("Estado civil", ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
    occupation = st.selectbox("Ocupación", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
    relationship = st.selectbox("Relación", ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"])
    race = st.selectbox("Raza", ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"])
    sex = st.selectbox("Sexo", ["Male", "Female"])
    capital_gain = st.number_input("Ganancia de capital", value=4000)
    capital_loss = st.number_input("Pérdida de capital", value=0)
    hours_per_week = st.number_input("Horas por semana", min_value=1, max_value=168, value=45)
    native_country = st.text_input("País de origen", value="United-States")

    submitted = st.form_submit_button("Enviar")

    if submitted:
        datos_json = {
            'age': age,
            'workclass': workclass,
            'fnlwgt': fnlwgt,
            'education': education,
            'education-num': education_num,
            'marital-status': marital_status,
            'occupation': occupation,
            'relationship': relationship,
            'race': race,
            'sex': sex,
            'capital-gain': capital_gain,
            'capital-loss': capital_loss,
            'hours-per-week': hours_per_week,
            'native-country': native_country
        }

        url = 'http://127.0.0.1:8000/adults_model/'

        exito, respuesta = realizar_solicitud_post(url, datos_json)

        if exito:
            st.success(f'Solicitud exitosa. Respuesta: {respuesta}')
        else:
            st.error(f'Error en la solicitud: {respuesta}')
