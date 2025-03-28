import streamlit as st
import requests

# Configuración general
st.set_page_config(page_title="Predicción de Ingresos", page_icon="💰", layout="centered")

st.title("💼 Predicción de Ingreso Alto")
st.markdown("Ingresa los datos de una persona para estimar la probabilidad de que su ingreso sea mayor a 50K.")

# Función para realizar la solicitud POST a la API
def realizar_solicitud_post(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# Formulario
with st.form("api_form"):
    st.subheader("📝 Datos del individuo")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Edad", min_value=1, value=21)
        workclass = st.selectbox("Clase de trabajo", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
        education = st.selectbox("Educación", ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"])
        education_num = st.number_input("Años de educación", min_value=1, max_value=16, value=10)
        marital_status = st.selectbox("Estado civil", ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
        occupation = st.selectbox("Ocupación", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])

    with col2:
        relationship = st.selectbox("Relación", ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"])
        race = st.selectbox("Raza", ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"])
        sex = st.selectbox("Sexo", ["Male", "Female"])
        capital_gain = st.number_input("Ganancia de capital", value=4000)
        capital_loss = st.number_input("Pérdida de capital", value=0)
        hours_per_week = st.number_input("Horas por semana", min_value=1, max_value=168, value=45)
        native_country = st.text_input("País de origen", value="United-States")

    submitted = st.form_submit_button("🔍 Predecir ingreso")

    if submitted:
        datos_json = {
            'age': age,
            'workclass': workclass,
            'education': education,
            'education_num': education_num,
            'marital_status': marital_status,
            'occupation': occupation,
            'relationship': relationship,
            'race': race,
            'sex': sex,
            'capital_gain': capital_gain,
            'capital_loss': capital_loss,
            'hours_per_week': hours_per_week,
            'native_country': native_country
        }

        url = "http://127.0.0.1:8000/predict"
        exito, respuesta = realizar_solicitud_post(url, datos_json)

        st.divider()

        if exito:
            pred = respuesta["prediccion"]
            st.metric(label="🔢 Probabilidad de ingreso > 50K", value=f"{pred:.2%}")

            if pred >= 0.5:
                st.success("💸 Alta probabilidad de ingreso alto. ¡Buen perfil!")
            else:
                st.warning("⚠️ Baja probabilidad de ingreso alto. Puede mejorar algunos aspectos.")
        else:
            st.error(f'❌ Error en la solicitud: {respuesta}')
