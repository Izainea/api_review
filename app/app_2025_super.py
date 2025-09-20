import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Predicción de Ingresos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (Opcional, para las tarjetas) ---
st.markdown("""
<style>
.card {
    border-radius: 10px;
    padding: 20px;
    background-color: #f0f2f6;
    margin-bottom: 10px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
}
.card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
.suggestion-card {
    border-radius: 10px;
    padding: 15px;
    background-color: #e8f4ff;
    margin-bottom: 10px;
    border-left: 5px solid #007bff;
}
</style>
""", unsafe_allow_html=True)


# --- TÍTULO Y DESCRIPCIÓN ---
st.title('🔮 Predicción de Potencial de Ingresos')
st.write('Esta aplicación analiza diversos factores de un individuo para predecir si sus ingresos anuales superan los **$50,000 USD**. Completa el formulario para obtener un análisis detallado.')
st.divider()

# --- FORMULARIO DE ENTRADA DE DATOS ---
with st.form(key='prediction_form'):
    st.header('👤 Perfil del Individuo')
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Información Personal')
        age = st.number_input('Edad', min_value=17, max_value=100, value=35)
        sex = st.selectbox('Sexo', ['Male', 'Female'], index=0)
        race = st.selectbox('Raza', ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'])

    with col2:
        st.subheader('Educación y Trabajo')
        education_num = st.slider('Años de Educación', min_value=1, max_value=16, value=13)
        occupation = st.selectbox('Ocupación', ['Exec-managerial', 'Prof-specialty', 'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'])
        hours_per_week = st.number_input('Horas por Semana', min_value=1, max_value=100, value=40)

    with col3:
        st.subheader('Situación Financiera y Familiar')
        marital_status = st.selectbox('Estado Civil', ['Married-civ-spouse', 'Never-married', 'Divorced', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'])
        capital_gain = st.number_input('Ganancia de Capital ($)', min_value=0, max_value=100000, value=0)
        capital_loss = st.number_input('Pérdida de Capital ($)', min_value=0, max_value=100000, value=0)
    
    # --- DATOS ADICIONALES (Menos comunes, en un expander) ---
    with st.expander("Ver más opciones..."):
        workclass = st.selectbox('Clase de Trabajo', ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'])
        education = st.selectbox('Nivel Educativo (Referencia)', ['Bachelors', 'HS-grad', 'Some-college', 'Masters', 'Doctorate', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '11th', '12th', '10th', '9th', '7th-8th', '5th-6th', '1st-4th', 'Preschool'])
        relationship = st.selectbox('Relación Familiar', ['Husband', 'Wife', 'Not-in-family', 'Own-child', 'Unmarried', 'Other-relative'])
        native_country = st.selectbox('País de Origen', ['United-States', 'Mexico', 'Philippines', 'Germany', 'Canada', 'Puerto-Rico', 'El-Salvador', 'India', 'Cuba', 'England', 'Jamaica', 'South', 'China', 'Italy', 'Dominican-Republic', 'Vietnam', 'Guatemala', 'Japan', 'Poland', 'Columbia', 'Taiwan', 'Haiti', 'Iran', 'Portugal', 'Nicaragua', 'Peru', 'France', 'Greece', 'Ecuador', 'Ireland', 'Hong', 'Cambodia', 'Trinadad&Tobago', 'Laos', 'Thailand', 'Yugoslavia', 'Outlying-US(Guam-USVI-etc)', 'Honduras', 'Hungary', 'Scotland', 'Holand-Netherlands'])

    submit_button = st.form_submit_button(label='✨ Realizar Predicción')


# --- LÓGICA DE PREDICCIÓN Y VISUALIZACIÓN ---
if submit_button:
    # URL de tu API (Asegúrate que esté corriendo)
    url_api = 'http://127.0.0.1:8000/adults_model/'

    # Creación del payload para la API
    data = {
        'age': age, 'workclass': workclass, 'education': education, 
        'education-num': education_num, 'marital-status': marital_status,
        'occupation': occupation, 'relationship': relationship, 'race': race, 
        'sex': sex, 'capital-gain': capital_gain, 'capital-loss': capital_loss,
        'hours-per-week': hours_per_week, 'native-country': native_country
    }
    
    try:
        with st.spinner('🧠 Analizando el perfil...'):
            response = requests.post(url_api, data=json.dumps(data))
            response.raise_for_status()  # Lanza un error si la petición falla
            
            prediction_data = response.json()
            probability = prediction_data.get('prediction', 0)

        st.header(f"Resultados del Análisis 📈")

        tab1, tab2 = st.tabs(["📊 Resumen de Predicción", "💡 Factores Clave y Sugerencias"])

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            if probability > 0.5:
                st.success(f"**Resultado:** ¡Alta probabilidad de ganar más de $50K! 🎉")
                st.metric(
                    label="Probabilidad de Ingresos >$50K",
                    value=f"{probability:.2%}",
                    delta="Positivo"
                )
            else:
                st.warning(f"**Resultado:** Baja probabilidad de ganar más de $50K en este momento. 🤔")
                st.metric(
                    label="Probabilidad de Ingresos >$50K",
                    value=f"{probability:.2%}",
                    delta="A mejorar",
                    delta_color="inverse"
                )
            
            st.progress(probability)
            st.write("Esta barra representa la confianza del modelo en la predicción. Un valor más alto indica una mayor certeza.")
            st.markdown('</div>', unsafe_allow_html=True)


        with tab2:
            st.subheader("Análisis de Factores y Recomendaciones")
            if probability > 0.5:
                st.markdown("Basado en los datos, estos son algunos factores que contribuyen positivamente a tu perfil de ingresos:")
                
                if education_num >= 13: # Nivel universitario o superior
                    st.markdown('<div class="suggestion-card">🎓 **Educación Avanzada:** Tus años de estudio son un fuerte indicador de alto potencial de ingresos. ¡Excelente!</div>', unsafe_allow_html=True)
                if occupation in ['Exec-managerial', 'Prof-specialty', 'Tech-support']:
                     st.markdown(f'<div class="suggestion-card">💼 **Ocupación Estratégica:** Tu rol como **{occupation}** está en un sector con alta demanda y remuneración.</div>', unsafe_allow_html=True)
                if hours_per_week > 40:
                    st.markdown('<div class="suggestion-card">⏰ **Dedicación Extra:** Trabajar más de 40 horas semanales a menudo se correlaciona con mayores ingresos y responsabilidades.</div>', unsafe_allow_html=True)
                if capital_gain > 0:
                    st.markdown('<div class="suggestion-card">💹 **Inversiones Inteligentes:** Las ganancias de capital indican un manejo financiero que potencia los ingresos.</div>', unsafe_allow_html=True)
            
            else:
                st.markdown("Aquí tienes algunas áreas de oportunidad que podrían incrementar tu potencial de ingresos a futuro:")
                
                if education_num < 13:
                    st.markdown('<div class="suggestion-card">📚 **Capacitación Continua:** Considera obtener certificaciones, diplomados o un grado académico superior. La educación es uno de los factores más influyentes.</div>', unsafe_allow_html=True)
                if occupation in ['Other-service', 'Handlers-cleaners', 'Farming-fishing', 'Priv-house-serv']:
                    st.markdown(f'<div class="suggestion-card">🚀 **Desarrollo Profesional:** Explora oportunidades de crecimiento dentro de tu campo o la transición hacia roles con mayor demanda, como tecnología o gestión.</div>', unsafe_allow_html=True)
                if capital_gain == 0:
                     st.markdown('<div class="suggestion-card">💸 **Educación Financiera:** Aprender sobre inversiones puede abrir nuevas fuentes de ingresos pasivos a través de ganancias de capital.</div>', unsafe_allow_html=True)

    except requests.exceptions.RequestException as e:
        st.error(f"🔌 Error de Conexión: No se pudo conectar a la API en '{url_api}'.")
        st.error(f"Detalle del error: {e}")
        st.info("Asegúrate de que el servidor de la API (FastAPI) se esté ejecutando localmente.")
