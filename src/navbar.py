import streamlit as st

def mostrar_navbar():
    """
    Función para renderizar la barra lateral personalizada en todas las páginas.
    Oculta la navegación por defecto de Streamlit y muestra enlaces con nombres propios.
    """
    # 1. Ocultar la navegación automática de Streamlit (la que pone los nombres de archivo)
    st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

    # 2. Definir nuestros propios enlaces
    with st.sidebar:
        st.header("Navegación")
        st.page_link("app.py", label="Inicio", icon="🏠")
        st.page_link("pages/01_Interfaz_1.py", label="Gestión de Flota", icon="🚚")
        st.page_link("pages/02_Interfaz_2.py", label="Cajas", icon="📦")
        st.page_link("pages/03_Interfaz_3.py", label="control de comustible", icon="⛽")