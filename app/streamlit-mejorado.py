import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Ingresos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS personalizado
st.markdown("""
<style>
    .main {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .card {
        border-radius: 1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        padding: 1.5rem;
        margin-bottom: 1rem;
        background-color: white;
    }
    .header-card {
        background-color: #1E88E5;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-card {
        background-color: #4CAF50;
        color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
    }
    .warning-card {
        background-color: #FFA726;
        color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-container {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .income-badge-high {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: bold;
        display: inline-block;
    }
    .income-badge-low {
        background-color: #FFA726;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: bold;
        display: inline-block;
    }
    .avatar-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    .avatar {
        border-radius: 50%;
        width: 120px;
        height: 120px;
        object-fit: cover;
        border: 4px solid white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .profile-detail {
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

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

# Función para generar avatar basado en características
def generar_avatar(sex, age):
    gender = "male" if sex == "Male" else "female"
    age_group = "young" if age < 30 else "middle" if age < 50 else "old"
    
    # Usamos avatares predefinidos según género y grupo de edad
    avatar_map = {
        "male_young": "👨‍💼",
        "male_middle": "👨‍💼",
        "male_old": "👴",
        "female_young": "👩‍💼",
        "female_middle": "👩‍💼",
        "female_old": "👵"
    }
    
    return avatar_map.get(f"{gender}_{age_group}", "👤")

# Función para crear un gráfico de gauge (medidor)
def crear_medidor_probabilidad(probabilidad):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probabilidad * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Probabilidad de Ingreso >$50K", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'lightyellow'},
                {'range': [50, 80], 'color': 'lightgreen'},
                {'range': [80, 100], 'color': 'green'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50}}))
    
    fig.update_layout(
        paper_bgcolor="white",
        height=300,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig

# Función para crear gráfico de comparación
def crear_grafico_comparacion(probabilidad):
    # Datos de referencia (hipotéticos, podrías usar datos reales si están disponibles)
    categorias = ["<$15K", "$15K-$25K", "$25K-$50K", ">$50K"]
    valores = [15, 30, 35, 20]  # Porcentajes hipotéticos de la población
    
    # Determinamos en qué categoría cae el usuario
    if probabilidad > 0.5:
        color_usuario = ["lightgrey", "lightgrey", "lightgrey", "#4CAF50"]
        categoria_usuario = ">$50K"
    else:
        color_usuario = ["lightgrey", "lightgrey", "#FFA726", "lightgrey"]
        categoria_usuario = "$25K-$50K"
    
    fig = px.bar(
        x=categorias,
        y=valores,
        color_discrete_sequence=color_usuario,
        labels={"x": "Categoría de Ingreso", "y": "Porcentaje de Población (%)"}
    )
    
    fig.update_layout(
        title="Su predicción le sitúa en la categoría: " + categoria_usuario,
        showlegend=False,
        height=300,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Añadir anotación para la posición del usuario
    fig.add_annotation(
        x=categoria_usuario,
        y=valores[categorias.index(categoria_usuario)],
        text="SU POSICIÓN",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    return fig

# Función para generar una tarjeta de perfil
def mostrar_tarjeta_perfil(datos, prediccion):
    probabilidad = prediccion.get("probability", prediccion.get("prediction", 0))
    ingreso_alto = probabilidad > 0.5
    
    # Contenedor principal para el perfil
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # Dividir en dos columnas (avatar y datos básicos)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
        emoji_avatar = generar_avatar(datos["sex"], datos["age"])
        st.markdown(f"<div style='font-size: 100px; text-align: center;'>{emoji_avatar}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<h2>{datos['education']} en {datos['occupation']}</h2>", unsafe_allow_html=True)
        
        # Etiqueta de ingreso
        if ingreso_alto:
            st.markdown("<div class='income-badge-high'>Ingreso >$50K</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='income-badge-low'>Ingreso <$50K</div>", unsafe_allow_html=True)
        
        # Detalles del perfil
        st.markdown("<div class='profile-detail'>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Edad:</strong> {datos['age']} años</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Género:</strong> {datos['sex']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Estado civil:</strong> {datos['marital-status']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Horas de trabajo:</strong> {datos['hours-per-week']} h/semana</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Medidor de probabilidad
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Probabilidad de Ingreso Superior a $50,000</h3>", unsafe_allow_html=True)
    
    # Mostrar el gauge
    st.plotly_chart(crear_medidor_probabilidad(probabilidad), use_container_width=True)
    
    # Explicación del resultado
    if ingreso_alto:
        st.markdown(f"""
        <div class='success-card'>
            <h3>¡Felicidades!</h3>
            <p>Según nuestro modelo, tiene un <strong>{probabilidad*100:.1f}%</strong> de probabilidad de ganar más de $50,000 al año.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='warning-card'>
            <h3>Resultado</h3>
            <p>Según nuestro modelo, tiene un <strong>{probabilidad*100:.1f}%</strong> de probabilidad de ganar más de $50,000 al año.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Gráfico comparativo
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Comparación con la Población General</h3>", unsafe_allow_html=True)
    st.plotly_chart(crear_grafico_comparacion(probabilidad), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Factores influyentes (simplificado)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Factores que Influyen en el Pronóstico</h3>", unsafe_allow_html=True)
    
    # Factores hipotéticos - en una aplicación real, esto podría venir del modelo
    factores = {
        "Educación": 0.8 if datos["education"] in ["Doctorate", "Prof-school", "Masters"] else 0.3,
        "Horas de trabajo": 0.6 if datos["hours-per-week"] > 40 else 0.2,
        "Ocupación": 0.7 if datos["occupation"] in ["Exec-managerial", "Prof-specialty"] else 0.4,
        "Estado civil": 0.5 if "Married" in datos["marital-status"] else 0.3
    }
    
    # Visualizar los factores como barras horizontales
    factor_df = pd.DataFrame({
        "Factor": list(factores.keys()),
        "Impacto": list(factores.values())
    })
    
    fig_factores = px.bar(
        factor_df,
        y="Factor",
        x="Impacto",
        orientation="h",
        color="Impacto",
        color_continuous_scale=["#FFA726", "#4CAF50"],
        range_color=[0, 1]
    )
    
    fig_factores.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Impacto en la Predicción",
        yaxis_title="",
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig_factores, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Header de la aplicación
st.markdown("<div class='header-card'>", unsafe_allow_html=True)
st.title("🧠 Predictor de Ingresos")
st.markdown("Complete los datos para predecir si sus ingresos superan los $50,000 anuales")
st.markdown("</div>", unsafe_allow_html=True)

# Crear interfaz de dos columnas
col1, col2 = st.columns([1, 2])

# Columna para el formulario
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 Datos Personales y Laborales")
    
    # Formulario para introducir los datos requeridos por la API
    with st.form("api_form"):
        age = st.number_input("Edad", min_value=18, max_value=90, value=30)
        sex = st.selectbox("Sexo", ["Male", "Female"])
        race = st.selectbox("Raza", ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"])
        
        st.markdown("#### Educación y Trabajo")
        education = st.selectbox("Educación", ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"])
        education_num = st.number_input("Años de educación", min_value=1, max_value=16, value=10)
        workclass = st.selectbox("Clase de trabajo", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
        occupation = st.selectbox("Ocupación", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
        hours_per_week = st.number_input("Horas por semana", min_value=1, max_value=99, value=40)
        
        st.markdown("#### Información personal y financiera")
        marital_status = st.selectbox("Estado civil", ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
        relationship = st.selectbox("Relación", ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"])
        capital_gain = st.number_input("Ganancia de capital ($)", min_value=0, value=0)
        capital_loss = st.number_input("Pérdida de capital ($)", min_value=0, value=0)
        
        # Campos menos importantes en un expander
        with st.expander("Campos adicionales"):
            fnlwgt = st.number_input("fnlwgt", value=200000)
            native_country = st.selectbox("País de origen", ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany", "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"])

        submitted = st.form_submit_button("Predecir Ingresos", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Columna para los resultados
with col2:
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
        
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
        
    if 'last_data' not in st.session_state:
        st.session_state.last_data = None
    
    # Si se envió el formulario o ya hay una predicción guardada
    if 'submitted' in locals() and submitted:
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

        with st.spinner('Analizando datos...'):
            exito, respuesta = realizar_solicitud_post(url, datos_json)

        if exito:
            st.session_state.prediction_made = True
            st.session_state.last_prediction = respuesta
            st.session_state.last_data = datos_json
            
            # Mostrar la tarjeta de perfil con la predicción
            mostrar_tarjeta_perfil(datos_json, respuesta)
        else:
            st.error(f'Error en la solicitud: {respuesta}')
            st.markdown("""
            <div class="card">
                <h3>🛑 No se pudo realizar la predicción</h3>
                <p>Compruebe que el servicio de la API esté funcionando correctamente en http://127.0.0.1:8000/adults_model/</p>
                <p>Detalles del error:</p>
                <code>{}</code>
            </div>
            """.format(respuesta), unsafe_allow_html=True)
    
    # Si ya hay una predicción guardada, mostrarla
    elif st.session_state.prediction_made:
        mostrar_tarjeta_perfil(st.session_state.last_data, st.session_state.last_prediction)
    
    # Si no hay predicción, mostrar placeholder
    else:
        st.markdown("""
        <div class="card" style="height: 300px; display: flex; align-items: center; justify-content: center; text-align: center;">
            <div>
                <h2>👈 Complete el formulario</h2>
                <p>Ingrese sus datos personales y laborales para obtener una predicción sobre su nivel de ingresos.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar un ejemplo de visualización
        st.markdown("""
        <div class="card">
            <h3>Ejemplo de Visualización</h3>
            <p>Una vez que envíe sus datos, verá aquí una visualización detallada similar a esta:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Imagen de ejemplo
        st.image("https://via.placeholder.com/800x400.png?text=Visualización+de+Ejemplo", use_column_width=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f0f0f0; border-radius: 0.5rem;">
    <p>📊 Modelo predictivo de ingresos basado en características demográficas y laborales</p>
    <p style="font-size: 0.8rem;">Este es un modelo de demostración y no debe usarse para tomar decisiones financieras reales.</p>
</div>
""", unsafe_allow_html=True)
