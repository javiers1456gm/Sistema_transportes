import streamlit as st
import pandas as pd
import numpy as np
from src.navbar import mostrar_navbar  # Importamos nuestra nueva función

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Transportes",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Llamamos a la función que dibuja el menú lateral
mostrar_navbar()

# Contenido Principal
st.title("🚚 Dashboard General")
st.markdown("---")  # Línea separadora minimalista

# --- SIMULACIÓN DE DATOS ---
# Generamos datos ficticios para las gráficas
np.random.seed(42)

# Datos para línea de tiempo (Viajes por día)
fechas = pd.date_range(start="2023-10-01", periods=30)
datos_viajes = pd.DataFrame(
    np.random.randint(5, 20, size=(30, 3)),
    index=fechas,
    columns=['Ruta Norte', 'Ruta Sur', 'Ruta Centro']
)

# Datos para barras (Gastos por vehículo)
datos_gastos = pd.DataFrame({
    'Combustible': [1200, 1500, 900, 1100, 1300],
    'Mantenimiento': [200, 500, 100, 300, 250],
    'Peajes': [150, 200, 100, 180, 120]
}, index=['Camión 01', 'Camión 02', 'Furgoneta 01', 'Camión 03', 'Furgoneta 02'])

# --- METRICAS (KPIs) ---
st.subheader("Resumen Operativo")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Flota Activa", "15 Vehículos", "2 en taller", delta_color="inverse")
col2.metric("Viajes del Mes", "342", "+12%")
col3.metric("Gasto Combustible", "$12,450", "-5%")
col4.metric("Eficiencia Promedio", "92%", "+1.5%")

st.markdown("---")

# --- GRÁFICAS ---
st.subheader("📊 Análisis Visual")

# Gráfica 1: Línea de tiempo (Ancho completo)
st.markdown("**Viajes diarios por Ruta (Últimos 30 días)**")
st.line_chart(datos_viajes)

# Columnas para gráficas inferiores
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("**Costos Operativos por Unidad**")
    # Gráfico de barras apiladas (Streamlit lo hace auto con dataframes)
    st.bar_chart(datos_gastos)

with col_graf2:
    st.markdown("**Distribución de Carga (Simulada)**")
    # Gráfico de área
    datos_area = pd.DataFrame(
        np.random.randn(20, 3) + [10, 10, 10],
        columns=['Refrigerado', 'Seco', 'Peligroso']
    )
    st.area_chart(datos_area)

st.info("💡 Nota: Estos datos son simulados para demostrar la capacidad gráfica de Streamlit.")