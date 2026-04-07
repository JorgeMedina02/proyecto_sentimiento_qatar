# =================================================================
# FASE 4: DASHBOARD INTERACTIVO FINAL - MUNDIAL QATAR 2022
# =================================================================

import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import pandas as pd

print("Iniciando montaje del Dashboard final...")

# 1. CARGA DE DATOS PROCESADOS (Desde la Fase 1-4)
# -----------------------------------------------------------------
try:
    df_limpios = pd.read_csv('../data/processed/datos_limpios.csv')
    df_temporal = pd.read_csv('../data/processed/evolucion_temporal.csv')
    df_actores = pd.read_csv('../data/processed/sentimiento_actores.csv')
    df_top_table = pd.read_csv('../data/processed/top_influencers.csv')
except FileNotFoundError as e:
    print(f"Error al cargar los datos: {e}. Asegúrate de ejecutar el cuaderno de Jupyter primero.")
    exit()

# 2. CONFIGURACIÓN DE GRÁFICAS ESTATICAS
# -----------------------------------------------------------------
# Paleta de colores consistente
color_map = {'positive': '#27AE60', 'neutral': '#95A5A6', 'negative': '#C0392B'}

fig_global = px.pie(
    df_limpios['Sentiment'].value_counts().reset_index(), 
    names='Sentiment', values='count', 
    title='Distribución Global del Sentimiento',
    color='Sentiment', color_discrete_map=color_map
)

fig_time = px.line(
    df_temporal, x='Fecha', y='counts', color='Sentiment',
    title='Evolución Diaria del Sentimiento', 
    color_discrete_map=color_map, markers=True
)

fig_cross = px.bar(
    df_actores, x='Actor_Tema', y='Porcentaje', color='Sentimiento', 
    barmode='group', title='Sentimiento por Tema/Actor Clave', 
    color_discrete_map=color_map
)

# 3. TEXTOS DEL RESUMEN EJECUTIVO Y ANÁLISIS DE RED
# -----------------------------------------------------------------
resumen_texto = """
### 1. Introducción y objetivo
Este proyecto analiza la estructura del debate y la percepción ciudadana durante el inicio del Mundial de la FIFA Qatar 2022. Para presentar los resultados, se utiliza un dashboard interactivo que integra Procesamiento de Lenguaje Natural (NLP) y Análisis de Redes Sociales (ARS), permitiendo identificar tendencias clave en la opinión pública frente a un evento de alcance global.

### 2. Descripción de los datos
Se empleó un dataset estructurado proveniente de Twitter, recolectado durante los primeros días de la competición. Contiene más de 22.000 registros procesados con variables esenciales como fecha de publicación, número de likes y el texto original limpio.

### 3. Fases del trabajo
1. **Preprocesamiento:** Limpieza de texto mediante expresiones regulares para eliminar URLs y menciones, normalización a minúsculas y eliminación de ruido.
2. **NLP y Sentimiento:** Análisis de las polaridades para evaluar la proporción de mensajes positivos, negativos y neutros en el contexto deportivo y sociopolítico del evento, cruzando los datos con temas específicos (FIFA, Qatar, VAR, etc.).
3. **Análisis de Redes Sociales (ARS):** Construcción de un grafo dirigido a partir de las menciones entre usuarios. El modelo permitió calcular métricas de centralidad (PageRank, Betweenness) para identificar a los líderes de opinión.
"""

# 4. DISEÑO DEL DASHBOARD (LAYOUT)
# -----------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#F4F7F6', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1('Análisis de Opinión Pública: Mundial Qatar 2022', style={'textAlign': 'center', 'color': '#2C3E50'}),
    
    # Bloque 1: Resumen Ejecutivo
    html.Div(style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)', 'marginBottom': '30px'}, children=[
        html.H2('Resumen Ejecutivo', style={'color': '#2C3E50', 'borderBottom': '2px solid #34495E', 'paddingBottom': '10px'}),
        dcc.Markdown(resumen_texto, style={'fontSize': '15px', 'lineHeight': '1.6'})
    ]),
    
    # Bloque 2: Gráficas de Sentimiento (Global y Temporal)
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'}, children=[
        html.Div([dcc.Graph(figure=fig_global)], style={'width': '45%', 'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '10px'}),
        html.Div([dcc.Graph(figure=fig_time)], style={'width': '45%', 'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '10px'}),
    ]),
    
    # Bloque 3: Sociograma Gephi con Zoom Interactivo
    html.Div(style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)', 'marginTop': '30px'}, children=[
        html.H2('Mapa de la Red de Interacciones (Zoom Interactivo)', style={'color': '#2C3E50', 'borderBottom': '2px solid #34495E', 'paddingBottom': '10px'}),
        html.P('Utiliza la rueda del ratón para explorar el núcleo de la red exportada desde Gephi.', style={'color': '#7F8C8D'}),
        dcc.Graph(
            id='gephi-zoom',
            figure={
                'data': [],
                'layout': {
                    'xaxis': {'visible': False, 'range': [0, 1000]},
                    'yaxis': {'visible': False, 'range': [0, 1000], 'scaleanchor': 'x'},
                    'images': [{
                        'source': '/assets/sociograma.png',
                        'xref': 'x', 'yref': 'y', 'x': 0, 'y': 1000, 'sizex': 1000, 'sizey': 1000,
                        'sizing': 'stretch', 'layer': 'below'
                    }],
                    'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}, 'height': 700, 'plot_bgcolor': 'white'
                }
            },
            config={'scrollZoom': True}
        )
    ]),

    # Bloque 4: Cruce de Temas y Tabla de Top Influencers
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px', 'justifyContent': 'center', 'marginTop': '30px'}, children=[
        html.Div([dcc.Graph(figure=fig_cross)], style={'width': '45%', 'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '10px'}),
        html.Div(style={'width': '45%', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px'}, children=[
            html.H3('Top 10 Influencers (Métricas Estructurales)', style={'textAlign': 'center', 'color': '#2C3E50'}),
            dash_table.DataTable(
                data=df_top_table.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df_top_table.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px', 'fontFamily': 'Arial', 'fontSize': '13px'},
                style_header={'backgroundColor': '#34495E', 'color': 'white', 'fontWeight': 'bold'}
            )
        ]),
    ]),
    
    # Bloque 5: Interpretación de Red
    html.Div(style={'backgroundColor': '#ECF0F1', 'padding': '30px', 'borderRadius': '10px', 'marginTop': '30px'}, children=[
        html.H2('Interpretación del Análisis de Grafos', style={'color': '#2C3E50', 'borderBottom': '3px solid #34495E', 'paddingBottom': '10px'}),
        html.H4('1. Perfiles de Actores', style={'color': '#2980B9'}),
        html.P('La tabla superior revela quiénes dominan la conversación según el algoritmo PageRank. Observamos una mezcla entre cuentas oficiales e influenciadores orgánicos.'),
        html.H4('2. Polarización Temática', style={'color': '#2980B9'}),
        html.P('El gráfico de barras demuestra cómo entidades deportivas generan opiniones mayoritariamente positivas, mientras que tópicos sociopolíticos o arbitrales concentran la carga negativa.'),
        html.H4('3. Nodos Puente', style={'color': '#2980B9'}),
        html.P('Aquellos usuarios con alta métrica de Intermediación (Betweenness) actúan como conectores vitales de información entre distintas burbujas de aficionados aisladas.')
    ]),

    # Bloque 6: Explorador de Tuits
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginTop': '30px'}, children=[
        html.H3('Explorador de Mensajes Originales', style={'textAlign': 'center', 'color': '#2C3E50'}),
        html.Div(style={'width': '300px', 'margin': '0 auto', 'paddingBottom': '20px'}, children=[
            dcc.Dropdown(
                id='sentiment-filter', 
                options=[
                    {'label': 'Todos', 'value': 'all'}, 
                    {'label': 'Positivo', 'value': 'positive'}, 
                    {'label': 'Neutral', 'value': 'neutral'}, 
                    {'label': 'Negativo', 'value': 'negative'}
                ], 
                value='all', clearable=False
            )
        ]),
        dash_table.DataTable(
            id='tweets-table',
            columns=[{"name": i, "id": i} for i in ['Fecha_Completa', 'Tweet_Limpio', 'Sentiment', 'Number of Likes']],
            style_cell={'textAlign': 'left', 'padding': '10px', 'whiteSpace': 'normal', 'height': 'auto', 'fontFamily': 'Arial', 'fontSize': '14px'},
            style_header={'backgroundColor': '#34495E', 'color': 'white', 'fontWeight': 'bold'},
            page_size=10
        )
    ]),
    
    html.Footer("Proyecto Universitario - Análisis de Sentimiento y Opinión Pública", style={'textAlign': 'center', 'marginTop': '30px', 'color': '#7F8C8D'})
])

# 5. LÓGICA DE INTERACTIVIDAD
# -----------------------------------------------------------------
@app.callback(Output('tweets-table', 'data'), Input('sentiment-filter', 'value'))
def update_table(selected_sentiment):
    # Mostrar primero los tuits con más 'Likes' para entender la opinión mayoritaria
    df_tweets = df_limpios[['Fecha_Completa', 'Tweet_Limpio', 'Sentiment', 'Number of Likes']].sort_values(by='Number of Likes', ascending=False)
    
    if selected_sentiment != 'all':
        df_tweets = df_tweets[df_tweets['Sentiment'] == selected_sentiment]
        
    return df_tweets.head(50).to_dict('records')

if __name__ == '__main__':
    print("\nServidor Dashboard cargando en http://127.0.0.1:8055/")
    app.run_server(debug=True, port=8055)
