# 📦 Sistema de Órdenes de Compra – Depósito Jiménez

Aplicación desarrollada en Streamlit para facilitar la gestión de compras, análisis de inventario y generación de órdenes desde datos en Excel.

## 🚀 Funcionalidades

- Carga dinámica de archivos de inventario y compras
- Sugerencia de compras basada en promedio de ventas y stock actual
- Filtros por proveedor y categoría
- Exportación automática a formato Excel usando plantilla
- Interfaz moderna con AgGrid para visualización avanzada

## 🛠 Requisitos

- Python 3.10+
- Streamlit Cloud o ambiente local con dependencias instaladas desde `requirements.txt`

## ▶️ Cómo usar

1. Clonar o descargar este repositorio.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la app:

```bash
streamlit run app.py
```

## 🌐 Despliegue en la nube

Este proyecto es compatible con [Streamlit Cloud](https://streamlit.io/cloud). Solo conecte el repo a su cuenta y ¡listo!

## 📂 Estructura del proyecto

```
inventarios-app/
├── app.py
├── config.py
├── requirements.txt
├── views/
│   └── vista_principal.py
├── utils/
│   ├── loader.py
│   ├── filters.py
│   ├── calculations.py
│   └── exporter.py
```

## 👨‍💼 Autor

Desarrollado por Tony – Supervisor de ventas y programador en Depósito Jiménez.