import os
import json
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# 1. Inicializador simple y seguro
# ----------------------------------------------------------------------
def init_orden() -> None:
    """Inicializa las estructuras necesarias en session_state para manejar la orden."""
    estado_inicial = {
        "orden_en_curso": [],
        "selected_codigos": set(),
        "nombre_orden": "",
        "ruta_ultima_orden": None,
        "mostrar_descarga_final": False,
    }
    for clave, valor in estado_inicial.items():
        st.session_state.setdefault(clave, valor)

# ----------------------------------------------------------------------
# 2. Agregar productos únicos
# ----------------------------------------------------------------------
def add_items(df_nuevos: pd.DataFrame) -> None:
    """
    Agrega productos a la orden, evitando duplicados por 'Código'.

    df_nuevos debe tener al menos: Código, Nombre, Cantidad a comprar, Último costo, Descuento
    """
    if df_nuevos.empty:
        st.warning("⚠️ No hay filas válidas para agregar.")
        return

    columnas_requeridas = ["Código", "Nombre", "Cantidad a comprar", "Último costo", "Descuento"]
    for col in columnas_requeridas:
        if col not in df_nuevos.columns:
            df_nuevos[col] = 0

    df_nuevos = df_nuevos[columnas_requeridas].copy()
    df_nuevos["Código"] = df_nuevos["Código"].astype(str).str.strip()

    df_nuevos = df_nuevos[df_nuevos["Código"] != ""]
    df_nuevos = df_nuevos[df_nuevos["Código"].notnull()]

    if df_nuevos.empty:
        st.warning("⚠️ No se encontraron códigos válidos.")
        return

    codigos_existentes = st.session_state.get("selected_codigos", set())
    df_filtrado = df_nuevos[~df_nuevos["Código"].isin(codigos_existentes)]

    if df_filtrado.empty:
        st.info("ℹ️ Todos los productos seleccionados ya están en la orden.")
        return

    df_filtrado["Descuento"] = pd.to_numeric(df_filtrado["Descuento"], errors="coerce").fillna(0).round(2)

    st.session_state["orden_en_curso"].extend(df_filtrado.to_dict(orient="records"))
    st.session_state["selected_codigos"].update(df_filtrado["Código"].tolist())

# ----------------------------------------------------------------------
# 3. Remover productos por índices
# ----------------------------------------------------------------------
def remove_items(idx_list) -> None:
    """Quita productos de la orden según sus índices, actualizando los códigos seleccionados."""
    for idx in sorted(idx_list, reverse=True):
        try:
            item = st.session_state["orden_en_curso"].pop(idx)
            codigo = str(item.get("Código", "")).strip()
            st.session_state["selected_codigos"].discard(codigo)
        except IndexError:
            st.warning(f"⚠️ Índice inválido al intentar eliminar: {idx}")

# ----------------------------------------------------------------------
# 4. Cerrar la orden
# ----------------------------------------------------------------------
def close_order(export_fn, nombre_orden="General") -> str | None:
    """
    Exporta la orden actual usando export_fn(df, proveedor=nombre_orden).
    Reinicia el estado de la orden y devuelve la ruta generada.
    """
    orden = st.session_state.get("orden_en_curso", [])
    if not orden:
        st.warning("⚠️ La orden está vacía.")
        return None

    df_export = pd.DataFrame(orden)
    if df_export.empty:
        st.warning("⚠️ No hay datos válidos para exportar.")
        return None

    try:
        ruta_exportada = export_fn(df_export, proveedor=nombre_orden)
    except TypeError:
        ruta_exportada = export_fn(df_export)

    init_orden()
    st.session_state["ruta_ultima_orden"] = ruta_exportada
    st.session_state["mostrar_descarga_final"] = True

    return ruta_exportada

