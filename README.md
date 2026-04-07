# Análisis de Sentimiento y Opinión Pública: Mundial Qatar 2022 ⚽📊

## Descripción del Proyecto
Este repositorio contiene un proyecto integral de Ciencia de Datos enfocado en el análisis de la opinión pública digital durante el inicio de la Copa Mundial de la FIFA Qatar 2022. 

A través de la extracción y procesamiento de más de 22.000 mensajes de la red social Twitter (X), este estudio combina técnicas de Procesamiento de Lenguaje Natural (NLP) y Análisis de Redes Sociales (ARS) para comprender las emociones de los usuarios, identificar líderes de opinión y detectar la polarización temática en torno al evento.

El resultado final es un panel de control (Dashboard) interactivo que permite explorar las métricas topológicas de la red, la evolución temporal del sentimiento y el impacto de los principales actores del debate.

## Estructura del Repositorio

El proyecto sigue una arquitectura estándar para flujos de trabajo de Machine Learning y análisis de datos:

* `app/`: Contiene el código fuente del dashboard interactivo.
  * `assets/`: Carpeta para recursos estáticos, incluyendo el `sociograma.png` generado en Gephi.
  * `dashboard.py`: Script principal de la aplicación web construida con Dash.
* `data/`: Almacenamiento de los conjuntos de datos.
  * `raw/`: Datos originales crudos (excluidos del repositorio por su tamaño).
  * `processed/`: Archivos limpios y tablas de resultados agregados listos para visualización (`datos_limpios.csv`, `top_influencers.csv`, etc.).
* `notebooks/`: Cuadernos de experimentación.
  * `1_EDA_y_Preprocesamiento.ipynb`: Pipeline completo de limpieza, NLP, agregación de datos y cálculo de métricas de red mediante NetworkX.
* `requirements.txt`: Lista de dependencias y librerías de Python necesarias.
* `.gitignore`: Configuración de archivos ignorados por Git.

## Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Manipulación de Datos:** Pandas, NumPy
* **Procesamiento de Lenguaje Natural (NLP):** Expresiones regulares (`re`)
* **Análisis de Redes Sociales (ARS):** NetworkX (PageRank, Betweenness, Closeness), Gephi 0.10.1 (Algoritmo Louvain, ForceAtlas2)
* **Visualización y Dashboard:** Plotly Express, Dash