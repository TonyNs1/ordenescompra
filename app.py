import streamlit as st
import os
from config import TEMP_FILE
from views.vista_principal import vista_principal

# Configuración inicial
st.set_page_config(page_title="📦 Depósito Jiménez", layout="wide")
RUTA_ORDENES = os.path.expanduser("~/Desktop/Ordenes de Compra")

# Ejecutar directamente la vista principal
try:
    vista_principal(ruta_ordenes=RUTA_ORDENES, temp_file=TEMP_FILE)
except Exception as e:
    st.error("❌ Ocurrió un error inesperado al ejecutar la aplicación.")
    st.exception(e)
