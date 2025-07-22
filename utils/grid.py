import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import json

def mostrar_aggrid(
    df,
    editable=False,
    seleccionar_filas=True,
    columnas_bloqueadas=None,
    height=450,
    key="aggrid"
) -> dict:
    df = df.copy().reset_index(drop=True)

    # Serializar todo a texto si es necesario
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, (int, float, str, bool, type(None))) else x)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True, filter=True)

    for col in df.columns:
        editable_col = editable and (columnas_bloqueadas is None or col not in columnas_bloqueadas)
        gb.configure_column(col, editable=editable_col)

    if seleccionar_filas:
        gb.configure_selection("multiple", use_checkbox=True)

    return AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED if editable else GridUpdateMode.SELECTION_CHANGED,
        data_return_mode="AS_INPUT",
        allow_unsafe_jscode=False,
        use_container_width=True,
        height=height,
        theme="streamlit",
        key=key,
    )
