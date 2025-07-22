import pandas as pd

def apply_filters(df: pd.DataFrame, extra: list) -> pd.DataFrame:
    """
    Reordena las columnas para mostrar primero las importantes.
    Agrega columnas extra seleccionadas por el usuario (si existen en el DataFrame).

    Args:
        df (pd.DataFrame): DataFrame original.
        extra (list): Lista de columnas adicionales seleccionadas.

    Returns:
        pd.DataFrame: DataFrame con columnas reorganizadas.
    """
    df_filtered = df.copy()
    extra = extra or []

    columnas_base = [
        'Alerta', 'Código', 'Nombre', 'Promedio mensual',
        'Existencias', 'Cantidad a comprar', 'Último costo',
        'Fecha última compra', 'Último proveedor'
    ]

    columnas_orden = [c for c in columnas_base if c in df_filtered.columns]
    columnas_extra = [c for c in extra if c in df_filtered.columns and c not in columnas_orden]
    columnas_finales = columnas_orden + columnas_extra

    return df_filtered[columnas_finales]
