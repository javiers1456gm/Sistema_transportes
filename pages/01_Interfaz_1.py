import streamlit as st
import pandas as pd
from src.navbar import mostrar_navbar

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Flota",
    page_icon="🚚",
    layout="wide"
)

# Renderizar navegación lateral
mostrar_navbar()

# Título Principal
st.title("🛠️ Gestión de Flota")
st.markdown("Registro y control de unidades: **Físico-Mecánico** y **Humos**.")
st.markdown("---")

# Crear pestañas para organizar la información
tab1, tab2 = st.tabs(["🚛 Inventario General", "🔧 Control de Servicios"])

# --- PESTAÑA 1: INVENTARIO (Lo que ya tenías) ---
with tab1:
    # --- SECCIÓN 1: FORMULARIO DE REGISTRO ---
    with st.expander("➕ Registrar Nueva Unidad / Actualizar Datos", expanded=True):
        st.info("Ingrese los datos de la unidad. Seleccione el tipo de registro correspondiente.")
        # NOTA TÉCNICA: Implementar lógica de selección en la tabla inferior.
        # Al seleccionar una fila, los datos deben cargarse en los widgets de este formulario
        # usando st.session_state para permitir la edición y posterior actualización (UPDATE).
        st.warning("📝 Nota: El sistema permitirá actualizar registros seleccionándolos en la tabla inferior. La información se reflejará aquí para su edición.")
        
        # Fila 1: UNIDAD, MARCA, TIPO
        col1, col2, col3 = st.columns(3)
        with col1:
            unidad = st.text_input("UNIDAD", placeholder="Ej. T-001")
        with col2:
            marca = st.text_input("MARCA", placeholder="Ej. Kenworth")
        with col3:
            tipo = st.selectbox("TIPO", ["Tracto Físico-Mecánico", "Tracto Humos"])

        # Fila 2: MOD., SERIE, Tarjeta de Circulacion
        col4, col5, col6 = st.columns(3)
        with col4:
            modelo = st.text_input("MOD.", placeholder="Ej. T680")
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
            fecha_realizar = st.date_input("REALIZAR")
        
        # Botón de Guardar (Simulado)
        if st.button("Guardar Registro", type="primary"):
            st.success(f"Unidad {unidad} registrada exitosamente.")

    st.markdown("---")

    # --- SECCIÓN 2: VISUALIZACIÓN DE DATOS (MOCK) ---
    st.subheader("📋 Inventario de Unidades")

    # Datos ficticios para maquetación
    data_mock = {
        "UNIDAD": ["T-101", "T-102", "T-103", "T-104", "T-105"],
        "MARCA": ["Kenworth", "Volvo", "Freightliner", "International", "Kenworth"],
        "TIPO": ["Tracto Físico-Mecánico", "Tracto Humos", "Tracto Físico-Mecánico", "Tracto Humos", "Tracto Físico-Mecánico"],
        "MOD.": ["T680", "VNL 760", "Cascadia", "LT Series", "T880"],
        "SERIE": ["1M1...589", "4V4...123", "3A3...789", "1H1...456", "2K2...001"],
        "Tarjeta de Circulacion": ["TC-998877", "TC-112233", "TC-445566", "TC-778899", "TC-001122"],
        "PLACA": ["58-AK-9C", "12-UE-4F", "89-PL-1A", "45-TR-2B", "90-MN-5X"],
        "STATUS": ["Vigente", "Vigente", "Por Vencer", "Vencido", "Vigente"],
        "REALIZAR": ["2024-12-15", "2024-11-20", "2023-10-30", "2023-09-15", "2025-01-10"],
        "Eliminar": [False, False, False, False, False]
    }

    df_flota = pd.DataFrame(data_mock)

    # Filtro rápido por tipo
    filtro_tipo = st.multiselect("Filtrar por TIPO", df_flota["TIPO"].unique(), default=df_flota["TIPO"].unique())

    if filtro_tipo:
        df_display = df_flota[df_flota["TIPO"].isin(filtro_tipo)]
    else:
        df_display = df_flota

    # Tabla editable para simular selección de borrado
    st.data_editor(
        df_display,
        column_config={
            "Eliminar": st.column_config.CheckboxColumn(
                "Eliminar",
                help="Seleccione para borrar",
                default=False,
            )
        },
        disabled=["UNIDAD", "MARCA", "TIPO", "MOD.", "SERIE", "Tarjeta de Circulacion", "PLACA", "STATUS", "REALIZAR"],
        use_container_width=True,
        hide_index=True
    )
    
    # Botón de borrado múltiple
    col_del1, col_del2 = st.columns([6, 1])
    with col_del2:
        st.button("🗑️ Borrar Seleccionados", type="primary")

# --- PESTAÑA 2: SERVICIOS (Nueva funcionalidad) ---
with tab2:
    st.header("Historial y Programación de Servicios")
    
    with st.expander("🛠️ Registrar Mantenimiento / Actualizar Kilometraje"):
        # Formulario simplificado para servicios
        # NOTA TÉCNICA: El campo de selección de unidad debe ser un st.selectbox.
        # Debe poblarse concatenando "Unidad - Marca - Año" desde la base de datos.
        # Dado que la flota es pequeña, no hay problemas de rendimiento al cargar todos los registros.
        st.info("📝 Nota: El sistema traerá un menú desplegable con la Unidad, Marca y Año de los vehículos.")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            s_unidad = st.text_input("UNIDAD a actualizar", placeholder="Ej. T-101")
        with s_col2:
            s_km_actual = st.number_input("KILOMETRAJE ACTUAL", min_value=0, step=100)
        with s_col3:
            s_fecha = st.date_input("FECHA SERVICIO")
            
        s_col4, s_col5 = st.columns(2)
        with s_col4:
            s_ultimo = st.text_input("ULTIMO SERVICIO", placeholder="Ej. Cambio de Aceite")
        with s_col5:
            s_proximo = st.number_input("PROXIMO SERVICIO", min_value=0, step=5000)
            
        if st.button("Registrar Servicio", type="primary"):
            st.success(f"Servicio registrado para la unidad {s_unidad}")

    st.markdown("---")
    st.subheader("📊 Tabla de Control de Servicios")
    
    # Datos ficticios para servicios (Coincidiendo con las columnas solicitadas)
    data_servicios = {
        "UNIDAD": ["T-101", "T-102", "T-103", "T-104", "T-105"],
        "MARCA": ["Kenworth", "Volvo", "Freightliner", "International", "Kenworth"],
        "TIPO": ["Tracto Físico-Mecánico", "Tracto Humos", "Tracto Físico-Mecánico", "Tracto Humos", "Tracto Físico-Mecánico"],
        "MOD.": ["T680", "VNL 760", "Cascadia", "LT Series", "T880"],
        "SERIE": ["1M1...589", "4V4...123", "3A3...789", "1H1...456", "2K2...001"],
        "Tarjeta de Circulacion": ["TC-998877", "TC-112233", "TC-445566", "TC-778899", "TC-001122"],
        "PLACA": ["58-AK-9C", "12-UE-4F", "89-PL-1A", "45-TR-2B", "90-MN-5X"],
        "ULTIMO SERVICIO": ["Cambio Aceite", "Frenos", "Afinación", "Llantas", "General"],
        "FECHA SERVICIO": ["2023-12-01", "2023-11-15", "2023-10-20", "2023-09-10", "2024-01-05"],
        "PROXIMO": [150000, 280000, 95000, 310000, 55000],
        "PROXIMO SERVICIO": [150000, 280000, 95000, 310000, 55000],
        "KILOMETRAJE ACTUAL": [145000, 278000, 92000, 305000, 50000],
        "KM PARA RECC. 25000KM": [5000, 2000, 3000, 5000, 5000]
    }
    
    df_servicios = pd.DataFrame(data_servicios)
    st.dataframe(df_servicios, use_container_width=True, hide_index=True)
