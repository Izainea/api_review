import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Financiero",
    page_icon="💰",
    layout="wide",
)

# Encabezado elegante
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💼 Dashboard Financiero Personal</h1>", unsafe_allow_html=True)
st.markdown("##### Un vistazo rápido a tus ingresos, gastos y ahorros", unsafe_allow_html=True)
st.markdown("---")

# Datos simulados
df = pd.DataFrame({
    "Mes": ["Enero", "Febrero", "Marzo"],
    "Ingresos": [100, 200, 300],
    "Gastos": [50, 80, 120],
    "Ahorros": [50, 120, 180]
})

# Métricas destacadas
ingresos_totales = df["Ingresos"].sum()
gastos_totales = df["Gastos"].sum()
ahorros_totales = df["Ahorros"].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💵 Ingresos Totales", value=f"${ingresos_totales:,.0f}")
with col2:
    st.metric(label="💸 Gastos Totales", value=f"${gastos_totales:,.0f}")
with col3:
    st.metric(label="🏦 Ahorros Totales", value=f"${ahorros_totales:,.0f}")

style_metric_cards(background_color="#F9F9F9", border_left_color="#4CAF50", border_color="#D3D3D3")

st.markdown("---")

# Visualizaciones
colored_header(label="Tendencia Mensual", description="Visualiza cómo cambian tus finanzas mes a mes", color_name="green-70")

fig = px.line(df, x="Mes", y=["Ingresos", "Gastos", "Ahorros"],
              markers=True, template="plotly_white",
              labels={"value": "Monto ($)", "variable": "Categoría"},
              title="Comparación de Ingresos, Gastos y Ahorros")

fig.update_layout(legend_title_text="Categoría", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# Tabla
with st.expander("📊 Ver datos en tabla"):
    st.dataframe(df, use_container_width=True)
