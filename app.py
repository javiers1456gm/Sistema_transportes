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
# Generamos datos ficticios alineados con los módulos (Flota, Cajas, Combustible)
np.random.seed(42)

# 1. Datos de Rendimiento de Combustible (Relacionado con Módulo 3)
# Simulamos Km/L para ver tendencias diarias
fechas = pd.date_range(start="2024-01-01", periods=30)
datos_rendimiento = pd.DataFrame({
    'Rendimiento Real (Km/L)': np.random.uniform(2.2, 2.9, size=30),
    'Meta de la Empresa (2.7 Km/L)': [2.7] * 30
}, index=fechas)

# 2. Datos de Gastos por Unidad (Relacionado con Módulo 1 y 3)
# Usamos IDs de unidades como en el inventario (T-101, etc.)
unidades_ids = ['T-101 (Kenworth)', 'T-102 (Volvo)', 'T-103 (Freightliner)', 'T-104 (International)', 'T-105 (Kenworth)']
datos_gastos = pd.DataFrame({
    'Combustible ($)': np.random.randint(15000, 25000, size=5),
    'Mantenimiento ($)': np.random.randint(2000, 8000, size=5),
    'Gestoría/Multas ($)': np.random.randint(500, 2000, size=5)
}, index=unidades_ids)

# 3. Datos Simulados para Alertas de Mantenimiento (Basado en tus reglas)
# Simulamos cuánto falta para el próximo servicio crítico
datos_mantenimiento_alertas = pd.DataFrame({
    'Unidad': ['T-101', 'T-103', 'T-105', 'T-102', 'T-104'],
    'Servicio Requerido': ['Lubricación (10k)', 'Aceite y Filtros (30k)', 'Frenos Balatas (40k)', 'Enfriamiento (25k)', 'Masa/Rodamientos (100k)'],
    'Km Restantes': [500, 1200, 4500, 8000, 15000],  # Cuánto falta para llegar al límite
    'Estado': ['CRÍTICO', 'ALERTA', 'ATENCIÓN', 'OK', 'OK']
})

# Filtramos solo lo urgente para el dashboard principal
alertas_urgentes = datos_mantenimiento_alertas[datos_mantenimiento_alertas['Km Restantes'] < 5000].sort_values('Km Restantes')

# Configuración de colores para la tabla de alertas
def color_alertas(val):
    if val == 'CRÍTICO':
        return 'background-color: #ff4b4b; color: white'
    elif val == 'ALERTA':
        return 'background-color: #ffbd45; color: black'
    return ''

# --- METRICAS (KPIs) ---
st.subheader("📌 Resumen Rápido")
st.markdown("Vista general del estado de la empresa hoy.")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Flota Total", "9 Unidades", "5 Tractos + 4 Cajas", help="Suma total de vehículos y remolques registrados.")
col2.metric("Rendimiento Promedio", "2.55 Km/L", "-0.15 vs Meta", delta_color="inverse", help="Promedio general de consumo de diesel. Si está en rojo, estamos gastando más de lo planeado.")
col3.metric("Gasto Combustible Mes", "$98,450", "+5% vs Mes Anterior", delta_color="inverse", help="Dinero gastado en diesel en lo que va del mes.")
col4.metric("Docs. Por Vencer", "3 Alertas", "Atención Requerida", delta_color="inverse", help="Documentos que vencen en los próximos 30 días.")

st.markdown("---")

# --- GRÁFICAS ---
st.subheader("📊 Análisis Detallado")

# Nueva Sección: Alertas de Mantenimiento (Lo más importante primero)
st.markdown("### 🚨 Próximos Mantenimientos (Preventivo)")
col_maint1, col_maint2 = st.columns([2, 1])

with col_maint1:
    st.info("Unidades que requieren atención inmediata según kilometraje acumulado.")
    # Mostramos tabla estilizada
    st.dataframe(alertas_urgentes.style.applymap(color_alertas, subset=['Estado']), use_container_width=True, hide_index=True)

with col_maint2:
    # Gráfica de barras horizontal para ver visualmente "cuánto hilo le queda" a los servicios urgentes
    st.bar_chart(alertas_urgentes.set_index('Unidad')['Km Restantes'], color="#ff4b4b")

# Gráfica 1: Línea de tiempo (Rendimiento)
st.markdown("### 📉 Rendimiento de Diesel: ¿Estamos cumpliendo la meta?")
st.info("Esta gráfica compara el rendimiento diario de la flota (Línea Azul) contra la meta establecida por la empresa (Línea Roja). **Objetivo: Mantenerse por encima de la línea roja.**")
st.line_chart(datos_rendimiento, color=["#29b5e8", "#ff4b4b"]) # Azul para real, Rojo para meta

# Columnas para gráficas inferiores
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown("### 💰 ¿En qué gasta cada camión?")
    st.caption("Desglose de gastos acumulados este mes. Permite identificar qué unidad está consumiendo más recursos en Mantenimiento o Combustible.")
    st.bar_chart(datos_gastos)

with col_graf2:
    st.markdown("### 🚦 Semáforo de Documentación")
    st.caption("Estado legal de la flota. **Rojo** = Vencido (No circular), **Amarillo** = Por vencer (Renovar pronto), **Verde** = OK.")
    # Datos de estado (Vigente, Vencido, etc.)
    datos_estatus = pd.DataFrame({
        '✅ Todo en Orden': [3, 2],
        '⚠️ Por Vencer (30 días)': [1, 1],
        '❌ VENCIDO (Detener)': [1, 1]
    }, index=['Tractocamiones', 'Cajas/Remolques'])
    
    # Usamos colores semáforo: Verde, Amarillo, Rojo
    st.bar_chart(datos_estatus, color=["#09ab3b", "#ffbd45", "#ff2b2b"])

st.success("💡 **Tip:** Pase el mouse sobre las gráficas para ver los valores exactos de cada unidad o día.")