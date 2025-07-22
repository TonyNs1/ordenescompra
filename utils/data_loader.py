import pandas as pd
import unicodedata
import traceback

def load_data(uploaded_file):
    """
    Carga un archivo Excel, limpia encabezados y normaliza nombres de columnas.
    Devuelve un DataFrame listo para procesar.
    """
    try:
        if uploaded_file is None:
            raise ValueError("❌ No se cargó ningún archivo.")

        df = pd.read_excel(uploaded_file, header=1, dtype=str, engine="openpyxl")
        df.columns = [str(col).strip() if col else "" for col in df.columns]

        def normalize(text):
            return (
                unicodedata.normalize("NFKD", str(text))
                .encode("ascii", errors="ignore")
                .decode("ascii")
                .strip()
                .lower()
            )

        normalized_cols = [normalize(c) for c in df.columns]

        col_map = {
            "codigo": "Código",
            "nombre": "Nombre",
            "promedio mensual vendido": "Promedio mensual",
            "promedio mensual": "Promedio mensual",
            "existencias": "Existencias",
            "costo ultima compra": "Último costo",
            "ultimo costo unitario con descuento": "Último costo",
            "ultimo proveedor": "Último proveedor",
            "proveedor": "Último proveedor",
            "categoria": "Categoría",
            "categoría": "Categoría",
            "ultima compra": "Fecha última compra",
        }

        renamed_cols = {
            original: col_map[norm]
            for original, norm in zip(df.columns, normalized_cols)
            if norm in col_map
        }

        df = df.rename(columns=renamed_cols)

        if "Código" not in df.columns:
            raise ValueError("❌ No se encontró la columna 'Código' en el archivo Excel.")

        df["Código"] = df["Código"].astype(str).str.strip()

        return df.reset_index(drop=True).copy()

    except Exception:
        raise RuntimeError(f"❌ Error al cargar el archivo Excel:\n{traceback.format_exc()}")

