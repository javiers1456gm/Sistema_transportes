import streamlit as st
import pandas as pd
from src.navbar import mostrar_navbar

# Configuración de la página
st.set_page_config(
    page_title="Control de Combustible",
    page_icon="⛽",
    layout="wide"
)

# Renderizar navegación lateral
mostrar_navbar()

# Título Principal
st.title("⛽ Control de Combustible")
st.markdown("Registro de cargas de combustible, kilometraje y rendimiento por viaje.")
st.markdown("---")

# --- SECCIÓN 1: FORMULARIO DE REGISTRO ---
with st.expander("➕ Registrar Carga / Actualizar Datos", expanded=True):
    st.info("Ingrese los datos del viaje y la carga de combustible.")
    # NOTA TÉCNICA: Implementar lógica de selección en la tabla inferior.
    # Al seleccionar una fila, los datos deben cargarse en los widgets de este formulario
    # usando st.session_state para permitir la edición y posterior actualización (UPDATE).
    st.warning("📝 Nota: El sistema permitirá actualizar registros seleccionándolos en la tabla inferior. La información se reflejará aquí para su edición.")

    # Fila 1: FECHA, UNIDAD, NOMBRE CONDUCTOR
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("FECHA")
    with col2:
        unidad = st.text_input("UNIDAD", placeholder="Ej. T-101")
    with col3:
        conductor = st.text_input("NOMBRE CONDUCTOR", placeholder="Nombre Completo")

    # Fila 2: INICIAL, FINAL, LITROS
    col4, col5, col6 = st.columns(3)
    with col4:
        inicial = st.number_input("INICIAL (Km)", min_value=0, step=100)
    with col5:
        final = st.number_input("FINAL (Km)", min_value=0, step=100)
    with col6:
        litros = st.number_input("LITROS", min_value=0.0, step=10.0)

    # Fila 3: COSTO X LITRO, FECHA COMISIÓN
    col7, col8 = st.columns(2)
    with col7:
        costo_litro = st.number_input("COSTO X LITRO", min_value=0.0, step=0.5)
    with col8:
        fecha_comision = st.date_input("FECHA O PERIODO DE COMISIÓN")

    # Fila 4: DE, A (Ruta)
    col9, col10 = st.columns(2)
    with col9:
        origen = st.text_input("DE (Origen)", placeholder="Ej. Saltillo - Monterrey")
    with col10:
        destino = st.text_input("A (Destino)", placeholder="Ej. Toluca")

    # Botón de Guardar
    if st.button("Guardar Registro", type="primary"):
        st.success(f"Carga para la unidad {unidad} registrada exitosamente.")

st.markdown("---")

# --- SECCIÓN 2: VISUALIZACIÓN DE DATOS (MOCK) ---
st.subheader("📋 Registro de Combustible")

# Datos ficticios para maquetación (Incluyendo columnas calculadas)
data_mock = {
    "FECHA": ["2024-01-10", "2024-01-12", "2024-01-15", "2024-01-18"],
    "UNIDAD": ["T-101", "T-102", "T-101", "T-103"],
    "NOMBRE CONDUCTOR": ["Juan Pérez", "Carlos López", "Juan Pérez", "Miguel Ángel"],
    "INICIAL": [150000, 280000, 152000, 95000],
    "FINAL": [152000, 282500, 154500, 97000],
    "KILÓMETROS RECORRIDOS": [2000, 2500, 2500, 2000],
    "LITROS": [800, 1000, 950, 750],
    "COSTO X LITRO": [22.50, 22.80, 22.50, 23.00],
    "IMPORTE": [18000.0, 22800.0, 21375.0, 17250.0],
    "RENDIMIENTO KM/LTS": [2.5, 2.5, 2.63, 2.66],
    "FECHA O PERIODO DE COMISIÓN": ["Semana 2", "Semana 2", "Semana 3", "Semana 3"],
    "DE": ["Saltillo - Monterrey", "Laredo", "Toluca", "Laredo"],
    "A": ["Toluca", "México", "Saltillo", "Guadalajara"],
    "Eliminar": [False, False, False, False]
}

df_combustible = pd.DataFrame(data_mock)

# Tabla editable
st.data_editor(
    df_combustible,
    column_config={
        "Eliminar": st.column_config.CheckboxColumn(
            "Eliminar",
            help="Seleccione para borrar",
            default=False,
        ),
        "IMPORTE": st.column_config.NumberColumn(format="$%.2f"),
        "COSTO X LITRO": st.column_config.NumberColumn(format="$%.2f"),
        "RENDIMIENTO KM/LTS": st.column_config.NumberColumn(format="%.2f km/l"),
    },
    disabled=["FECHA", "UNIDAD", "NOMBRE CONDUCTOR", "INICIAL", "FINAL", "KILÓMETROS RECORRIDOS", "LITROS", "COSTO X LITRO", "IMPORTE", "RENDIMIENTO KM/LTS", "FECHA O PERIODO DE COMISIÓN", "DE", "A"],
    use_container_width=True,
    hide_index=True
)

# Botón de borrado
col_del1, col_del2 = st.columns([6, 1])
with col_del2:
    st.button("🗑️ Borrar Seleccionados", type="primary", key="btn_borrar_combustible")