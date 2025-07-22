import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

def mostrar_aggrid(
    df,
    editable=False,
    seleccionar_filas=True,
    columnas_bloqueadas=None,
    height=450,
    key="aggrid"
) -> dict:
    df = df.copy().reset_index(drop=True)

    gb = GridOptionsBuilder.from_dataframe(df)

    # ✅ Filtros y propiedades básicas por columna
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True, filter=True)

    # ✅ Solo esta columna se formatea con dos decimales
    columna_dos_decimales = {"Último costo"}

    # 🎨 Zebra striping
    js_zebra = JsCode("""
        function(params) {
            return params.node.rowIndex % 2 === 0;
        }
    """)

    # ⌨️ Detener edición con Enter o Tab
    js_keyboard = JsCode("""
        function(params) {
            const ENTER = 13, TAB = 9;
            if (params.event.keyCode === ENTER || params.event.keyCode === TAB) {
                params.api.stopEditing();
            }
            return false;
        }
    """)

    for col in df.columns:
        editable_col = editable and (columnas_bloqueadas is None or col not in columnas_bloqueadas)
        flex_val = 2 if col.lower().startswith(("nombre", "último")) else 1

        if col in columna_dos_decimales:
            gb.configure_column(
                col,
                type=["numericColumn", "customNumericFormat"],
                valueFormatter=JsCode("""
                    function(params) {
                        let val = parseFloat(params.value);
                        return isNaN(val) ? '0.00' : val.toFixed(2);
                    }
                """),
                editable=editable_col,
                flex=flex_val,
                minWidth=120,
            )
        else:
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
        rowClassRules={"fila-alterna": js_zebra},
        suppressKeyboardEvent=js_keyboard,
    )

    update_mode = GridUpdateMode.MODEL_CHANGED if editable else GridUpdateMode.SELECTION_CHANGED

    return AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=update_mode,
        data_return_mode="AS_INPUT",
        allow_unsafe_jscode=True,
        use_container_width=True,
        height=height,
        theme="streamlit",
        key=key,
    )
