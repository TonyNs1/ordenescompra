import pandas as pd
import math

def compute_suggestions(df, dias):
    df = df.copy()

    # Asegurar numéricos
    df['Promedio mensual'] = pd.to_numeric(df.get('Promedio mensual', 0), errors='coerce').fillna(0)
    df['Existencias']      = pd.to_numeric(df.get('Existencias', 0), errors='coerce').fillna(0)

    # Cálculo único
    df['Sugerencia'] = (df['Promedio mensual'] / 30) * dias
    df['Cantidad a comprar'] = df['Sugerencia'] - df['Existencias']
    df['Cantidad a comprar'] = df['Cantidad a comprar'].apply(lambda x: max(0, math.floor(x)))

    # Clasificación de alerta
    def clasificar_alerta(row):
        if row['Cantidad a comprar'] > 0:
            return '🔴 Bajo stock'
        elif row['Existencias'] > row['Sugerencia']:
            return '🔵 Sobrestock'
        else:
            return '🟢 Óptimo'

    df['Alerta'] = df.apply(clasificar_alerta, axis=1)

    return df
