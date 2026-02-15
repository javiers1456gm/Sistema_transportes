import streamlit as st
import pandas as pd
from src.navbar import mostrar_navbar

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Cajas",
    page_icon="📦",
    layout="wide"
)

# Renderizar navegación lateral
mostrar_navbar()

# Título Principal
st.title("📦 Gestión de Cajas")
st.markdown("Control de inventario de cajas: **Secas**, **Refrigeradas**, etc.")
st.markdown("---")

# --- SECCIÓN 1: FORMULARIO DE REGISTRO ---
with st.expander("➕ Registrar Nueva Caja / Actualizar Datos", expanded=True):
    st.info("Ingrese los datos de la caja.")
    # NOTA TÉCNICA: Implementar lógica de selección en la tabla inferior.
    # Al seleccionar una fila, los datos deben cargarse en los widgets de este formulario
    # usando st.session_state para permitir la edición y posterior actualización (UPDATE).
    st.warning("📝 Nota: El sistema permitirá actualizar registros seleccionándolos en la tabla inferior. La información se reflejará aquí para su edición.")
    
    # Fila 1: UNIDAD, MARCA, TIPO
    col1, col2, col3 = st.columns(3)
    with col1:
        unidad = st.text_input("UNIDAD", placeholder="Ej. C-001")
    with col2:
        marca = st.text_input("MARCA", placeholder="Ej. Utility")
    with col3:
        # El cliente tiene casi todo en Caja Seca, pero lo dejamos como input de texto editable
        tipo = st.text_input("TIPO", value="Caja Seca")

    # Fila 2: MOD., SERIE, Tarjeta de Circulacion
    col4, col5, col6 = st.columns(3)
    with col4:
        modelo = st.text_input("MOD.", placeholder="Ej. 2018")
    with col5:
        serie = st.text_input("SERIE", placeholder="XXXXXXXXXXXXXXXXX")
    with col6:
        tarjeta = st.text_input("Tarjeta de Circulacion")

    # Fila 3: PLACA, STATUS, REALIZAR
    col7, col8, col9 = st.columns(3)
    with col7:
        placa = st.text_input("PLACA")
    with col8:
        status = st.selectbox("STATUS", ["Vigente", "Por Vencer", "Vencido", "En Mantenimiento", "Baja"])
    with col9:
        fecha_realizar = st.date_input("REALIZAR (Físico-Mecánico)")

    # Fila 4: UBICACIÓN y MULTAS (Campos específicos solicitados)
    col10, col11, col12 = st.columns(3)
    with col10:
        ubicacion = st.selectbox("UBICACIÓN / ORIGEN", ["Mexicana", "Nacional"])
    with col11:
        multa_sf = st.text_input("MULTA S/F", placeholder="Monto o Folio S/F")
    with col12:
        multa_cf = st.text_input("C/F", placeholder="Monto o Folio C/F")
    
    # Botón de Guardar (Simulado)
    if st.button("Guardar Caja", type="primary"):
        st.success(f"Caja {unidad} registrada exitosamente.")

st.markdown("---")

# --- SECCIÓN 2: VISUALIZACIÓN DE DATOS (MOCK) ---
st.subheader("📋 Inventario de Cajas")

# Datos ficticios para maquetación
data_mock = {
    "UNIDAD": ["C-501", "C-502", "C-503", "C-504"],
    "MARCA": ["Utility", "Great Dane", "Wabash", "Utility"],
    "TIPO": ["Caja Seca", "Caja Seca", "Caja Seca", "Caja Seca"],
    "MOD.": ["2019", "2020", "2018", "2021"],
    "SERIE": ["53U...123", "GD...456", "WB...789", "53U...000"],
    "Tarjeta de Circulacion": ["TC-C01", "TC-C02", "TC-C03", "TC-C04"],
    "PLACA": ["88-UA-9C", "11-VB-4F", "77-XC-1A", "44-YD-2B"],
    "STATUS": ["Vigente", "Vencido", "Vigente", "Por Vencer"],
    "REALIZAR": ["2024-05-10", "2023-12-01", "2024-08-15", "2024-02-20"],
    "UBICACIÓN": ["Mexicana", "Nacional", "Mexicana", "Nacional"],
    "MULTA S/F": ["-", "$1,500", "-", "-"],
    "C/F": ["-", "-", "-", "$500"],
    "Eliminar": [False, False, False, False]
}

df_cajas = pd.DataFrame(data_mock)

# Tabla editable para simular selección de borrado
st.data_editor(
    df_cajas,
    column_config={
        "Eliminar": st.column_config.CheckboxColumn(
            "Eliminar",
            help="Seleccione para borrar",
            default=False,
        )
    },
    disabled=["UNIDAD", "MARCA", "TIPO", "MOD.", "SERIE", "Tarjeta de Circulacion", "PLACA", "STATUS", "REALIZAR", "UBICACIÓN", "MULTA S/F", "C/F"],
    use_container_width=True,
    hide_index=True
)

# Botón de borrado múltiple
col_del1, col_del2 = st.columns([6, 1])
with col_del2:
    st.button("🗑️ Borrar Seleccionados", type="primary", key="btn_borrar_cajas")
