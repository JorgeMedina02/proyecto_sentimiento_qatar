# Análisis de Sentimiento y Opinión Pública: Mundial Qatar 2022

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Dash](https://img.shields.io/badge/Dash-Plotly-informational?style=flat&logo=plotly)
![NetworkX](https://img.shields.io/badge/NetworkX-ARS-success?style=flat)
![Gephi](https://img.shields.io/badge/Gephi-0.10.1-orange?style=flat)

## Descripción del Proyecto

Este repositorio contiene un proyecto integral de Ciencia de Datos enfocado en el análisis de la opinión pública digital durante el primer día de la Copa Mundial de la FIFA Qatar 2022. 

A través de la extracción y procesamiento de aproximadamente 22.500 tuits (dataset obtenido de Kaggle), este estudio combina técnicas de Procesamiento de Lenguaje Natural (NLP) y Análisis de Redes Sociales (ARS) para:
1. Comprender la polaridad emocional (positiva, neutra, negativa) en torno a temas deportivos y sociopolíticos.
2. Identificar a los principales líderes de opinión mediante métricas topológicas (PageRank, Betweenness Centrality).
3. Detectar la polarización del discurso y la formación de "cámaras de eco" (Comunidades / Modularidad de Louvain).

El entregable final es un Dashboard Interactivo construido con Plotly Dash que integra visualizaciones de datos, el sociograma de la red y el Data Storytelling académico.

---

## Estructura del Repositorio

El proyecto sigue una arquitectura estándar para flujos de trabajo analíticos:

    proyecto_sentimiento_qatar/
    │
    ├── app/
    │   ├── dashboard.py                      # Código fuente principal de la aplicación web
    │   └── assets/                           # Recursos estáticos exportados desde Gephi
    │       ├── Red_interacciones.png
    │       ├── Betweenness_Centrality_Distribution.png
    │       ├── Closeness_Centrality_Distribution.png
    │       ├── degree-distribution.png
    │       └── communities-size-distribution.png
    │
    ├── data/
    │   ├── raw/                              # Dataset original (ignorado por Git por tamaño)
    │   │   └── fifa_world_cup_2022_tweets.csv
    │   └── processed/                        # Tablas procesadas y archivos estructurales
    │       ├── datos_limpios.csv
    │       ├── evolucion_temporal.csv
    │       ├── red_interacciones.gexf        # Archivo base para visualizar la red en Gephi
    │       ├── sentimiento_actores.csv
    │       └── top_influencers.csv
    │
    ├── notebooks/
    │   └── 1_EDA_y_Preprocesamiento.ipynb    # Pipeline de NLP, agregación de datos y ARS (NetworkX)
    │
    ├── requirements.txt                      # Dependencias de Python
    └── README.md                             # Documentación del proyecto

---

## Tecnologías Utilizadas

* Lenguaje: Python 3.x
* Manipulación de Datos: pandas, numpy
* Procesamiento de Lenguaje Natural: Expresiones regulares (re)
* Análisis de Redes Sociales (ARS): networkx (Cálculo de métricas estructurales)
* Visualización de Grafos: Gephi 0.10.1 (Distribución espacial ForceAtlas2, Algoritmo de Louvain)
* Desarrollo Web / Dashboarding: dash, plotly

---

## Instalación y Configuración

Para replicar este entorno y ejecutar el dashboard en tu máquina local, sigue estos pasos:

1. Clonar el repositorio:
    ```bash
    git clone [https://github.com/TU_USUARIO/proyecto_sentimiento_qatar.git](https://github.com/TU_USUARIO/proyecto_sentimiento_qatar.git)
    cd proyecto_sentimiento_qatar
    ```

2. Crear y activar un entorno virtual (Recomendado):
* En Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
* En macOS / Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

---

## Flujo de Ejecución

El proyecto está diseñado para ejecutarse en dos fases secuenciales:

### Fase 1: Preprocesamiento y Modelado Matemático (Jupyter)
1. Inicia Jupyter Notebook o abre Visual Studio Code.
2. Navega a notebooks/1_EDA_y_Preprocesamiento.ipynb.
3. Ejecuta todas las celdas. Este proceso limpia el texto, calcula las agregaciones, genera las métricas de centralidad matemática de la red de usuarios y exporta los datos a la carpeta data/processed/.

Nota sobre Gephi: El archivo red_interacciones.gexf generado debe abrirse en el software Gephi para generar la visualización final del grafo (ForceAtlas 2) y exportar las gráficas estadísticas de distribución (Grado, Modularidad, Intermediación). Las imágenes resultantes deben alojarse en app/assets/.

### Fase 2: Lanzamiento del Dashboard
Una vez procesados los datos y alojadas las imágenes, despliega la interfaz web:

1. Navega a la carpeta de la aplicación:
    ```bash
    cd app
    ```
2. Ejecuta el servidor:
    ```bash
    python dashboard.py
    ```
3. Accede a http://127.0.0.1:8055/ en tu navegador web.

---

## Conclusiones Principales

1. Topología de Broadcast: El análisis topológico revela que el discurso operó bajo un esquema de "difusión masiva" (Diámetro 1, Grado Medio 0.257). Los usuarios actuaron como emisores pasivos apuntando a cuentas oficiales, sin generar debates horizontales.
2. Cámaras de Eco: Una Modularidad extrema (0.932) demuestra la existencia de un discurso altamente fracturado en micro-comunidades aisladas.
3. Polarización Temática: Los actores estrictamente deportivos (Messi, Ronaldo) capitalizaron el sentimiento positivo, mientras que las instituciones (FIFA, VAR) concentraron la negatividad sociopolítica del evento.

---
Autor: Jorge Medina
Modelos Predictivos III: Opinión Pública y Sentimiento