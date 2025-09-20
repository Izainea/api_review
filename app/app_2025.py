### NOs conectamos a la API con requests
import requests
import json
import streamlit as st

url_api='http://127.0.0.1:8000/adults_model/'

# Ejemplo de datos
st.title('Predicción de ingresos con API')

st.write('Este es un app que calcula el peso de un modelo respecto a un individuo que podría ganar más de 50K USD al año')

st.write('Llene los siguientes campos:')

age = st.number_input('Edad', min_value=0, max_value=100, value=25)
workclass = st.selectbox('Clase de trabajo', ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'])
education = st.selectbox('Nivel educativo', ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'])
education_num = st.number_input('Número de años de educación', min_value=0, max_value=20, value=10)
marital_status = st.selectbox('Estado civil', ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'])
occupation = st.selectbox('Ocupación', ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'])
relationship = st.selectbox('Relación', ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'])
race = st.selectbox('Raza', ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'])
sex = st.selectbox('Sexo', ['Female', 'Male'])
capital_gain = st.number_input('Ganancia de capital', min_value=0, max_value=100000, value=0)
capital_loss = st.number_input('Pérdida de capital', min_value=0, max_value=100000, value=0)
hours_per_week = st.number_input('Horas por semana', min_value=1, max_value=100, value=40)
native_country = st.selectbox('País de origen', ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands'])

if st.button('Hacer predicción'):
    data=json.dumps({'age': age,
        'workclass': workclass,
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
        'native-country': native_country})
    response=requests.post(url_api, data=data)
    st.write('La probabilidad de que esta persona gane más de 50K USD al año es de:')
    st.write(response.json()['prediction'])