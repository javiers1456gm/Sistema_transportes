import streamlit as st
import pandas as pd
import numpy as np
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
    st.header("🔧 Monitor de Mantenimiento Preventivo")
    st.markdown("El sistema calcula automáticamente el desgaste basado en el kilometraje actual vs. el último servicio.")
    
    # Definición de Reglas de Negocio (Tus requerimientos exactos)
    REGLAS_MANTENIMIENTO = {
        "Lubricación (Crucetas, 5ta rueda)": 10000,
        "Sistema Enfriamiento": 25000,
        "Aceite y Filtros (Motor/Trans)": 30000,
        "Frenos (Balatas)": 40000,
        "Filtro de Aire": 40000,
        "Frenos (Líquido)": 100000,
        "Masa Ruedas (Rodamientos/Retenes)": 100000
    }

    with st.expander("🛠️ Registrar Servicio Realizado (Resetear Contador)"):
        st.info("Utilice este formulario cuando el mecánico haya completado una tarea para reiniciar el contador de kilometraje de ese servicio.")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            s_unidad = st.selectbox("UNIDAD", ["T-101", "T-102", "T-103", "T-104", "T-105"])
        with s_col2:
            # Seleccionar cuál de los servicios específicos se realizó
            s_servicio = st.selectbox("TIPO DE SERVICIO REALIZADO", list(REGLAS_MANTENIMIENTO.keys()))
        with s_col3:
            s_fecha = st.date_input("FECHA SERVICIO")
            
        s_notas = st.text_area("Notas del Mecánico", placeholder="Ej. Se cambiaron balatas delanteras marca X...")
            
        if st.button("✅ Confirmar Servicio Realizado", type="primary"):
            st.success(f"Contador de '{s_servicio}' reiniciado para la unidad {s_unidad}.")

    st.markdown("---")
    st.subheader("🚦 Semáforo de Salud de la Flota")
    
    # --- LÓGICA DE SIMULACIÓN DE ESTADO ---
    # En una app real, esto vendría de comparar (Km Actual - Km Ultimo Servicio) vs Regla
    
    # Creamos un DataFrame donde las filas son las Unidades y las columnas son los Servicios
    unidades = ["T-101", "T-102", "T-103", "T-104", "T-105"]
    
    # Generamos datos aleatorios de "Km recorridos desde último servicio"
    # Algunos estarán cerca del límite (Rojo), otros lejos (Verde)
    data_matrix = {}
    for servicio, limite in REGLAS_MANTENIMIENTO.items():
        # Generamos valores aleatorios entre 0 y el límite + un poco más (para simular vencidos)
        valores = np.random.randint(0, int(limite * 1.2), size=5)
        data_matrix[f"{servicio} (Cada {limite//1000}k)"] = valores

    df_semaforo = pd.DataFrame(data_matrix, index=unidades)
    
    # Función para colorear la celda según el porcentaje de uso
    def estilo_semaforo(val):
        # Extraemos el límite del nombre de la columna (ej. "Aceite (Cada 30k)")
        # Esto es un hack visual para la demo, en prod se hace con diccionarios
        import re
        match = re.search(r'(\d+)k', val.name)
        if match:
            limite = int(match.group(1)) * 1000
            
            styles = []
            for v in val:
                porcentaje = v / limite
                if porcentaje >= 1.0:
                    styles.append('background-color: #ff4b4b; color: white') # Rojo Vencido
                elif porcentaje >= 0.8:
                    styles.append('background-color: #ffbd45; color: black') # Amarillo Alerta
                else:
                    styles.append('background-color: #90ee90; color: black') # Verde OK
            return styles
        return [''] * len(val)

    # Mostramos la tabla con el estilo aplicado
    st.dataframe(df_semaforo.style.apply(estilo_semaforo, axis=0), use_container_width=True)
    
    st.caption("🟢 Verde: OK | 🟡 Amarillo: Próximo a vencer (>80%) | 🔴 Rojo: Vencido (Atención Inmediata)")
