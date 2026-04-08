# Analisis de Sentimiento y Opinion Publica: Mundial Qatar 2022

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Dash](https://img.shields.io/badge/Dash-Plotly-informational?style=flat&logo=plotly)
![NetworkX](https://img.shields.io/badge/NetworkX-ARS-success?style=flat)
![Gephi](https://img.shields.io/badge/Gephi-0.10.1-orange?style=flat)

## Descripcion del Proyecto

Este repositorio contiene un proyecto integral de Ciencia de Datos enfocado en el analisis de la opinion publica digital durante el primer dia de la Copa Mundial de la FIFA Qatar 2022. 

A traves de la extraccion y procesamiento de aproximadamente 22.500 tuits (dataset obtenido de Kaggle), este estudio combina tecnicas de Procesamiento de Lenguaje Natural (NLP) y Analisis de Redes Sociales (ARS) para:
1. Comprender la polaridad emocional (positiva, neutra, negativa) en torno a temas deportivos y sociopoliticos.
2. Identificar a los principales lideres de opinion mediante metricas topologicas (PageRank, Betweenness Centrality).
3. Detectar la polarizacion del discurso, la formacion de "camaras de eco" y analizar la fragmentacion extrema de las audiencias.

El entregable final es un Dashboard Interactivo construido con Plotly Dash que integra visualizaciones de datos, sociogramas de la red segmentados por comunidades y un Data Storytelling de rigor academico.

---

## Estructura del Repositorio

El proyecto sigue una arquitectura estandar para flujos de trabajo analiticos:

    proyecto_sentimiento_qatar/
    │
    ├── app/
    │   ├── dashboard.py                      # Codigo fuente principal de la aplicacion web
    │   └── assets/                           # Recursos estaticos exportados desde Gephi
    │       ├── Red_interacciones.png
    │       ├── Betweenness_Centrality_Distribution.png
    │       ├── Closeness_Centrality_Distribution.png
    │       ├── degree-distribution.png
    │       ├── communities-size-distribution.png
    │       ├── comunidad_fifa.png
    │       ├── comunidad_bbc_y_comentarista.png
    │       ├── comunidad_inglaterra.png
    │       ├── comunidad_jiocinema.png
    │       └── comunidad_elon_musk.png
    │
    ├── data/
    │   ├── raw/                              # Dataset original
    │   │   └── fifa_world_cup_2022_tweets.csv
    │   └── processed/                        # Tablas procesadas y archivos estructurales
    │       ├── datos_limpios.csv
    │       ├── evolucion_temporal.csv
    │       ├── red_interacciones.gexf        # Archivo base para visualizar la red en Gephi
    │       ├── sentimiento_actores.csv
    │       └── top_influencers.csv
    │
    ├── notebooks/
    │   └── 1_EDA_y_Preprocesamiento.ipynb    # Pipeline de NLP, agregacion de datos y ARS (NetworkX)
    │
    ├── requirements.txt                      # Dependencias de Python
    └── README.md                             # Documentacion del proyecto

---

## Tecnologias Utilizadas

* Lenguaje: Python 3.x
* Manipulacion de Datos: pandas, numpy
* Procesamiento de Lenguaje Natural: Expresiones regulares (re)
* Analisis de Redes Sociales (ARS): networkx (Calculo de metricas estructurales)
* Visualizacion de Grafos: Gephi 0.10.1 (Distribucion espacial ForceAtlas2, Algoritmo de Louvain)
* Desarrollo Web / Dashboarding: dash, plotly

---

## Instalacion y Configuracion

Para replicar este entorno y ejecutar el dashboard en tu maquina local, sigue estos pasos:

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

## Flujo de Ejecucion

### Fase 1: Preprocesamiento y Modelado Matematico (Jupyter)
1. Inicia Jupyter Notebook o abre Visual Studio Code.
2. Navega a notebooks/1_EDA_y_Preprocesamiento.ipynb.
3. Ejecuta todas las celdas. Este proceso limpia el texto, calcula las agregaciones, genera las metricas de centralidad y exporta los datos a la carpeta data/processed/.

Nota sobre Gephi: El archivo red_interacciones.gexf generado se utilizo en el software Gephi para generar la visualizacion del grafo (ForceAtlas 2) y el aislamiento de sub-redes (Algoritmo de Louvain). Las imagenes resultantes se encuentran alojadas en app/assets/.

### Fase 2: Lanzamiento del Dashboard
1. Navega a la carpeta de la aplicacion:
    ```bash
    cd app
    ```
2. Ejecuta el servidor:
    ```bash
    python dashboard.py
    ```
3. Accede a http://127.0.0.1:8055/ en tu navegador web.

---

## Conclusiones Principales del Estudio

El analisis topologico y de interacciones arrojo los siguientes hallazgos empiricos:

1. Atomizacion del Discurso (Modularidad Extrema): Se registro una modularidad de 0.932. Las cinco comunidades principales apenas suman el 6% de la red total. Esto demuestra que no existio un debate global unificado, sino miles de micro-nichos hermeticos operando de forma simultanea.
2. Topologia de Broadcast: Las metricas de centralidad (Diametro 1, Grado Medio 0.257) confirman un modelo de comunicacion radial. Los usuarios actuan como emisores pasivos apuntando a cuentas oficiales, sin tejer redes de debate horizontal.
3. Los Cinco Pilares del Mega-Evento Digital: A traves del zoom analitico de comunidades, se identificaron las cinco sub-redes que definen el evento:
    * Pilar Institucional (@fifaworldcup - 2.02%): El nucleo organizativo, actuando como tablon de anuncios.
    * Pilar Mediatico (@bbcsport - 1.41%): El traslado de la contra-narrativa tradicional (derechos humanos) al entorno digital.
    * Pilar Tribal/Deportivo (England - 0.91%): La fanbase pasional aislada de la controversia.
    * Pilar Infraestructural (JioCinema - 0.79%): La respuesta en tiempo real a la crisis de servidores de retransmision en India.
    * Pilar Meta-Plataforma (@elonmusk - 0.79%): El meta-discurso generado por la propia adquisicion de la red social y sus metricas de trafico.

---
Autor: Jorge Medina López
Proyecto Universitario - Modelos Predictivos III: Analisis de Sentimiento y Opinion Publica