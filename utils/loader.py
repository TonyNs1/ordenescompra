import os
import hashlib
import streamlit as st
from utils.data_loader import load_data

def _file_hash(fileobj: bytes) -> str:
    """Devuelve el hash MD5 de un archivo cargado para comparar si cambió."""
    return hashlib.md5(fileobj).hexdigest()

def cargar_archivo_excel(temp_file: str) -> bool:
    """
    ▸ Carga un archivo Excel solo si es diferente al ya cargado.
    ▸ Si es el mismo, mantiene filtros, columnas y orden en curso.
    ▸ Si no se sube, intenta restaurar el último archivo cargado desde disco (solo si no hay sesión activa).
    """

    uploaded = st.file_uploader("📤 Cargar archivo Excel", type="xlsx", key="file_uploader")

    # 🟢 Si ya hay archivo cargado y no se subió uno nuevo
    if "df" in st.session_state and not uploaded:
        st.session_state.archivo_nuevo = False
        return True

    # 🔁 Usuario sube un nuevo archivo
    if uploaded:
        nuevo_hash = _file_hash(uploaded.getvalue())
        hash_anterior = st.session_state.get("hash_archivo")

        if nuevo_hash != hash_anterior:
            st.session_state.clear()

            with open(temp_file, "wb") as f:
                f.write(uploaded.getbuffer())

            st.session_state.hash_archivo = nuevo_hash
            st.session_state.archivo_nuevo = True

            df = load_data(temp_file)
            st.session_state.orig_df = df.copy()
            st.session_state.df = df.copy()

            st.success("✅ Archivo nuevo cargado correctamente.")
            return True
        else:
            # 📁 Archivo igual al anterior
            if "df" not in st.session_state:
                with open(temp_file, "wb") as f:
                    f.write(uploaded.getbuffer())
                df = load_data(temp_file)
                st.session_state.orig_df = df.copy()
                st.session_state.df = df.copy()

            st.session_state.archivo_nuevo = False
            st.info("ℹ️ Estás trabajando con el mismo archivo ya cargado.")
            return True

    # 🧠 Restaurar el último archivo cargado si existe y no hay archivo en memoria
    if "df" not in st.session_state and temp_file and os.path.exists(temp_file):
        df = load_data(temp_file)
        st.session_state.df = df
        st.session_state.orig_df = df.copy()
        st.session_state.archivo_nuevo = False
        st.info("ℹ️ Se restauró la sesión anterior desde disco.")
        return True

    st.warning("⚠️ Necesitas subir un archivo Excel para comenzar.")
    return False

