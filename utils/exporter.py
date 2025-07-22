import os
import pandas as pd
import xlsxwriter

def exportar_usando_machote(df: pd.DataFrame, nombre_archivo: str, carpeta_destino: str, *_args, **_kwargs) -> str:
    """Exporta la orden directamente en formato Excel compatible con ERP, usando xlsxwriter."""
    try:
        requeridas = ["Código", "Cantidad comprada", "Costo unitario de la compra", "Descuento"]
        for col in requeridas:
            if col not in df.columns:
                raise ValueError(f"❌ Faltan columnas requeridas en el DataFrame: {col}")

        os.makedirs(carpeta_destino, exist_ok=True)
        ruta_salida = os.path.join(carpeta_destino, nombre_archivo)

        with pd.ExcelWriter(ruta_salida, engine="xlsxwriter") as writer:
            df = df[requeridas].copy()
            df.to_excel(writer, index=False, sheet_name="Orden")

            workbook  = writer.book
            worksheet = writer.sheets["Orden"]

            formato_centro = workbook.add_format({"align": "center", "valign": "vcenter"})
            formato_texto = workbook.add_format({"num_format": "@", "align": "center"})
            formato_num = workbook.add_format({"num_format": "#,##0.00", "align": "center"})

            for idx, col in enumerate(requeridas):
                ancho = max(df[col].astype(str).map(len).max(), len(col)) + 2
                if col == "Código":
                    worksheet.set_column(idx, idx, ancho, formato_texto)
                elif col == "Cantidad comprada":
                    worksheet.set_column(idx, idx, ancho, formato_centro)
                else:
                    worksheet.set_column(idx, idx, ancho, formato_num)

        return ruta_salida

    except Exception as e:
        raise RuntimeError(f"❌ Error al exportar con xlsxwriter: {e}")

