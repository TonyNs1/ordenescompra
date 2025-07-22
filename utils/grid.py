import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def mostrar_aggrid(
    df,
    editable=False,
    seleccionar_filas=True,
    columnas_bloqueadas=None,
    height=450,
    key="aggrid"
) -> dict:
    df = df.copy().reset_index(drop=True)

    # 🔒 Protección: eliminar funciones u objetos no serializables
    for col in df.columns:
        if df[col].apply(lambda x: callable(x)).any():
            df[col] = df[col].astype(str)

    gb = GridOptionsBuilder.from_dataframe(df)

    # Filtros y comportamiento básico
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True, filter=True)

    for col in df.columns:
        editable_col = editable and (columnas_bloqueadas is None or col not in columnas_bloqueadas)
        flex_val = 2 if col.lower().startswith(("nombre", "último")) else 1

        gb.configure_column(
            col,
            editable=editable_col,
            flex=flex_val,
            minWidth=100
        )

    if seleccionar_filas:
        gb.configure_selection(
            selection_mode="multiple",
            use_checkbox=True,
            header_checkbox=True,
            header_checkbox_filtered_only=False,
        )

    gb.configure_grid_options(
        domLayout="normal",
        suppressRowClickSelection=True,
        enableCellTextSelection=True,
        headerHeight=30,
        rowHeight=34,
    )

    update_mode = GridUpdateMode.MODEL_CHANGED if editable else GridUpdateMode.SELECTION_CHANGED

    return AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=update_mode,
        data_return_mode="AS_INPUT",
        allow_unsafe_jscode=False,
        use_container_width=True,
        height=height,
        theme="streamlit",
        key=key,
    )
