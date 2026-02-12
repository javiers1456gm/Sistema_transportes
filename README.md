# 🚚 Sistema de Gestión de Transportes

## Estructura del Proyecto

Este proyecto utiliza una arquitectura modular para separar la interfaz de la lógica.

```text
Sistema_transportes/
│
├── .streamlit/          # Configuración visual de Streamlit.
├── assets/              # Imágenes y estilos CSS.
├── data/                # Archivos de datos (CSV, Excel).
├── pages/               # INTERFACES: Cada archivo aquí es una página en el menú lateral.
├── src/                 # BACKEND: Lógica de negocio, cálculos y bases de datos.
├── app.py               # PORTADA: Página de inicio de la aplicación.
├── requirements.txt     # Dependencias del proyecto.
└── README.md            # Documentación.
