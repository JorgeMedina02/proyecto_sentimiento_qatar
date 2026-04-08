# =================================================================
# FASE 4: DASHBOARD INTERACTIVO FINAL - MUNDIAL QATAR 2022
# Version final con Analisis Exhaustivo de Comunidades Top 5
# =================================================================

import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

print("Iniciando montaje del Dashboard final...")

# =================================================================
# 1. CARGA DE DATOS PROCESADOS
# =================================================================
try:
    df_limpios = pd.read_csv('../data/processed/datos_limpios.csv')
    df_temporal = pd.read_csv('../data/processed/evolucion_temporal.csv')
    df_actores = pd.read_csv('../data/processed/sentimiento_actores.csv')
    df_top_table = pd.read_csv('../data/processed/top_influencers.csv')
except FileNotFoundError as e:
    print(f"ERROR: No se encontraron los datos procesados ({e}).")
    print("Por favor, asegurese de haber ejecutado todo el cuaderno de Jupyter primero.")
    exit()

# =================================================================
# 2. CONFIGURACION VISUAL (ESTILOS Y COLORES)
# =================================================================
COLORES = {
    'positive': '#27AE60',
    'neutral':  '#95A5A6',
    'negative': '#C0392B'
}
FONDO_CARD   = 'white'
FONDO_APP    = '#F0F3F4'
COLOR_SECCION = '#2C3E50'
ESTILO_CARD = {
    'backgroundColor': FONDO_CARD,
    'padding': '30px',
    'borderRadius': '12px',
    'boxShadow': '0 2px 12px rgba(0,0,0,0.08)',
    'marginBottom': '24px'
}

# =================================================================
# 3. CONSTRUCCION DE FIGURAS ESTATICAS (PLOTLY)
# =================================================================

fig_global = px.pie(
    df_limpios['Sentiment'].value_counts().reset_index(),
    names='Sentiment', values='count',
    title='Distribucion Global del Sentimiento',
    color='Sentiment', color_discrete_map=COLORES,
    hole=0.35
)
fig_global.update_traces(textinfo='percent+label', textfont_size=13)
fig_global.update_layout(legend_title='Sentimiento', title_font_size=16)

df_dia = df_temporal[df_temporal['granularidad'] == 'dia'] if 'granularidad' in df_temporal.columns else df_temporal
fig_time = px.line(
    df_dia, x='Fecha', y='counts', color='Sentiment',
    title='Evolucion Diaria del Sentimiento',
    color_discrete_map=COLORES, markers=True
)
fig_time.update_layout(xaxis_title='Fecha', yaxis_title='Numero de Tuits', legend_title='Sentimiento', title_font_size=16)

df_hora = df_temporal[df_temporal['granularidad'] == 'hora'] if 'granularidad' in df_temporal.columns else pd.DataFrame()
if not df_hora.empty:
    fig_hora = px.bar(
        df_hora, x='Fecha', y='counts', color='Sentiment',
        title='Actividad por Hora del Dia',
        color_discrete_map=COLORES, barmode='stack'
    )
    fig_hora.update_layout(xaxis_title='Hora (UTC)', yaxis_title='Tuits', title_font_size=16)
else:
    fig_hora = go.Figure()
    fig_hora.add_annotation(text="Datos horarios no disponibles", showarrow=False)

fig_cross = px.bar(
    df_actores, x='Actor_Tema', y='Porcentaje', color='Sentimiento',
    barmode='group',
    title='Distribucion del Sentimiento por Tema/Actor Clave',
    color_discrete_map=COLORES,
    text='Porcentaje'
)
fig_cross.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_cross.update_layout(xaxis_title='Actor / Tema', yaxis_title='Porcentaje (%)', legend_title='Sentimiento', title_font_size=16, yaxis_range=[0, 80])

fig_likes = px.box(
    df_limpios, x='Sentiment', y='Number of Likes',
    color='Sentiment', color_discrete_map=COLORES,
    title='Distribucion de Likes por Sentimiento',
    points='outliers'
)
fig_likes.update_layout(xaxis_title='Sentimiento', yaxis_title='Numero de Likes', showlegend=False, title_font_size=16)
fig_likes.update_yaxes(type='log')

# =================================================================
# 4. TEXTOS ACADEMICOS PARA EL STORYTELLING (MARKDOWN)
# =================================================================

TEXTO_INTRO = """
### 1. Pregunta de investigacion y justificacion

¿Como se distribuyo y evoluciono la opinion publica en Twitter durante el inicio del **Mundial de la FIFA Qatar 2022**? ¿Que actores concentraron mayor volumen de conversacion y que polaridad emocional generaron?

Qatar 2022 fue un evento de alcance global con una doble dimension analitica: la estrictamente **deportiva** (resultados, jugadores, controversias arbitrales) y la **sociopolitica** (derechos humanos, condiciones laborales, postura de la FIFA ante criticas internacionales). Esta dualidad genera un escenario especialmente rico para el analisis de sentimiento.

### 2. Descripcion de los datos

El dataset proviene de **Kaggle** y contiene aproximadamente **22.500 tuits recopilados durante el primer dia de competicion** (noviembre de 2022). Las variables principales son: texto original, fecha y hora de publicacion, numero de likes, fuente del dispositivo y etiqueta de sentimiento pre-asignada.
"""

TEXTO_NLP = """
### 3. Metodologia de Procesamiento de Lenguaje Natural (NLP)

El pipeline de limpieza aplico las siguientes transformaciones para garantizar la calidad analitica:
1. **Eliminacion de ruido:** Purga de URLs y menciones (@usuario) que carecen de valor semantico directo en el analisis de texto.
2. **Normalizacion:** Conversion a minusculas y eliminacion de caracteres no alfanumericos.
3. **Analisis de Polaridad:** Agregacion estadistica de los sentimientos (positivo, neutro, negativo) para cruzar las emociones predominantes con entidades o palabras clave extraidas del texto.
"""

TEXTO_ARS = """
### 4. Metodologia del Analisis de Redes Sociales (ARS)

Para comprender la propagacion de la informacion, se construyo un **grafo dirigido de menciones** usando la libreria matematica `NetworkX` en Python:
- **Nodos:** Tuits originales y usuarios explicitamente mencionados.
- **Aristas:** Direccion e intensidad de la interaccion (mencion).

El modelo estructural fue exportado a **Gephi 0.10.1** para su especializacion espacial (algoritmo *ForceAtlas2*) y la ejecucion de calculos estadisticos avanzados para la deteccion de comunidades hermeticas (algoritmo *Louvain*).
"""

TEXTO_CONCLUSIONES = """
### 5. Conclusiones y Hallazgos Principales

**1. Atomizacion del Discurso (El Hallazgo Estructural):** La conclusion mas reveladora del proyecto se extrae del analisis de modularidad. El hecho de que la comunidad mas grande de toda la red (FIFA) represente unicamente el 2,02% del grafo, demuestra que la autoridad oficial perdio el monopolio de la conversacion. No hubo "un" Mundial en Twitter, hubo miles de micro-debates desconectados.

**2. Sentimiento Global y Polarizacion Tematica:** Predomina el sentimiento neutro, reflejando el caracter puramente informativo de la red en eventos en vivo. Sin embargo, las entidades deportivas operan como catalizadores de positividad, mientras que las instituciones organizativas concentran la negatividad ciudadana.

**3. Topologia de Difusion (Broadcast):** Las metricas de centralidad confirman un modelo de comunicacion en estrella. Miles de usuarios enviaron mensajes al vacio o directamente a cuentas hiper-populares, sin generar hilos de debate bidireccional entre la base de usuarios (Diametro 1 y Grado medio bajo).
"""

# =================================================================
# 5. ESTRUCTURA HTML DE LA APLICACION (LAYOUT)
# =================================================================
app = dash.Dash(__name__)
app.title = "Dashboard - Mundial Qatar 2022"

def card(children, extra_style=None):
    return html.Div(style={**ESTILO_CARD, **(extra_style or {})}, children=children)

def seccion_titulo(texto, color=COLOR_SECCION):
    return html.H2(texto, style={'color': color, 'borderBottom': f'3px solid {color}', 'paddingBottom': '8px', 'marginTop': '0'})

app.layout = html.Div(
    style={'backgroundColor': FONDO_APP, 'padding': '20px 40px', 'fontFamily': '"Segoe UI", Arial, sans-serif'},
    children=[

        html.Div(style={
            'background': 'linear-gradient(135deg, #1A252F 0%, #2C3E50 100%)',
            'padding': '40px', 'borderRadius': '12px', 'marginBottom': '28px', 'textAlign': 'center', 'color': 'white'
        }, children=[
            html.H1('Analisis de Opinion Publica', style={'margin': '0', 'fontSize': '2.2em'}),
            html.H2('Copa Mundial de la FIFA - Qatar 2022', style={'margin': '8px 0', 'fontWeight': '300', 'fontSize': '1.4em'}),
            html.P('Analisis de Sentimiento | Procesamiento de Lenguaje Natural | Analisis de Redes Sociales', style={'margin': '0', 'opacity': '0.75'})
        ]),

        html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'marginBottom': '0', 'minWidth': '150px'}, children=[
                html.H3(f"{len(df_limpios):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#2980B9'}),
                html.P("Tuits analizados", style={'margin': '0', 'color': '#7F8C8D'})
            ]),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'marginBottom': '0', 'minWidth': '150px'}, children=[
                html.H3(f"{(df_limpios['Sentiment']=='positive').sum():,}", style={'margin': '0', 'fontSize': '2em', 'color': '#27AE60'}),
                html.P("Tuits positivos", style={'margin': '0', 'color': '#7F8C8D'})
            ]),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'marginBottom': '0', 'minWidth': '150px'}, children=[
                html.H3(f"{(df_limpios['Sentiment']=='negative').sum():,}", style={'margin': '0', 'fontSize': '2em', 'color': '#C0392B'}),
                html.P("Tuits negativos", style={'margin': '0', 'color': '#7F8C8D'})
            ]),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'marginBottom': '0', 'minWidth': '150px'}, children=[
                html.H3(f"{df_limpios['Number of Likes'].sum():,.0f}", style={'margin': '0', 'fontSize': '2em', 'color': '#8E44AD'}),
                html.P("Likes totales", style={'margin': '0', 'color': '#7F8C8D'})
            ]),
        ]),

        card([seccion_titulo('1. Introduccion y Descripcion de los Datos'), dcc.Markdown(TEXTO_INTRO)]),

        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div([dcc.Graph(figure=fig_global, config={'displayModeBar': False})], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
            html.Div([dcc.Graph(figure=fig_likes, config={'displayModeBar': False})], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
        ]),

        card([seccion_titulo('2. Metodologia de Procesamiento de Lenguaje Natural'), dcc.Markdown(TEXTO_NLP)]),
        card([
            seccion_titulo('3. Evolucion Temporal del Sentimiento'),
            html.Div(style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}, children=[
                html.Div([dcc.Graph(figure=fig_time)], style={'flex': '1', 'minWidth': '300px'}),
                html.Div([dcc.Graph(figure=fig_hora)], style={'flex': '1', 'minWidth': '300px'}),
            ])
        ]),

        card([seccion_titulo('4. Metodologia del Analisis de Redes Sociales (ARS) y Gephi'), dcc.Markdown(TEXTO_ARS)]),

        card([
            seccion_titulo('4.1 Sociograma - Red de Menciones (Exportado desde Gephi)'),
            html.P(['Topologia interactiva de los usuarios. Nodos coloreados por comunidad (Algoritmo de Louvain); tamaño proporcional a la influencia central del usuario. Usa la rueda del raton para hacer zoom sobre el nucleo de la red.'], style={'color': '#7F8C8D'}),
            dcc.Graph(
                id='gephi-zoom',
                figure={
                    'data': [],
                    'layout': {
                        'xaxis': {'visible': False, 'range': [0, 1000]},
                        'yaxis': {'visible': False, 'range': [0, 1000], 'scaleanchor': 'x'},
                        'images': [{
                            'source': '/assets/Red_interacciones.png',
                            'xref': 'x', 'yref': 'y', 'x': 0, 'y': 1000,
                            'sizex': 1000, 'sizey': 1000,
                            'sizing': 'stretch', 'layer': 'below'
                        }],
                        'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
                        'height': 750,
                        'plot_bgcolor': 'white', 'paper_bgcolor': 'white'
                    }
                },
                config={'scrollZoom': True}
            )
        ]),

        card([
            seccion_titulo('4.2 Analisis Estadistico Topologico (Reportes de Gephi)'),
            html.P('El analisis de las distribuciones estadisticas confirma matematicamente la topologia visualizada.', style={'color': '#7F8C8D', 'marginBottom': '20px'}),
            
            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Ausencia de Nodos Puente (Betweenness)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/Betweenness_Centrality_Distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('La inmensa mayoria de los nodos (pico en el 0) carecen de capacidad de intermediacion. No hay usuarios que actuen como "puentes" conectando diferentes grupos.', style={'fontSize': '14px', 'color': '#34495E'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Estructura de Estrella (Closeness)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/Closeness_Centrality_Distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('Observamos dos picos extremos en 0 y en 1. Esto demuestra que la red tiene un diametro de 1: los usuarios interactuan en un unico paso con grandes cuentas centrales.', style={'fontSize': '14px', 'color': '#34495E'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Distribucion de Grado (Ley de Potencias)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/degree-distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('El 99% de los usuarios participan como emisores pasivos, mientras que la atencion es acaparada por menos del 1% de los actores (hubs en el eje X).', style={'fontSize': '14px', 'color': '#34495E'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Fragmentacion Extrema (Comunidades)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/communities-size-distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('La Modularidad de Louvain (0.932) es extremadamente alta. Ilustra la formacion de unas pocas "camaras de eco" grandes y miles de micro-comunidades desconectadas.', style={'fontSize': '14px', 'color': '#34495E'})
                ])
            ])
        ]),

        card([
            seccion_titulo('4.3 Analisis Micro: Atomizacion del Discurso por Comunidades'),
            html.P('El analisis de modularidad revela una atomizacion extrema del discurso. Las 5 comunidades principales (top 5) apenas suman el 6% de la red total. Esto evidencia que no hubo "un" Mundial, sino miles de nichos desconectados. A continuacion, se exponen los cinco pilares representativos de este mega-evento:', style={'color': '#7F8C8D', 'marginBottom': '30px'}),
            
            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'alignItems': 'center', 'marginBottom': '40px'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '300px', 'textAlign': 'center'}, children=[
                    html.Img(src='/assets/comunidad_fifa.png', style={'width': '100%', 'maxWidth': '550px', 'border': '1px solid #ECF0F1', 'borderRadius': '8px'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.H4('1. Pilar Institucional: @fifaworldcup (2.02%)', style={'color': '#8E44AD'}),
                    html.P('A pesar de ser la comunidad de mayor tamaño, apenas supera el 2%. Esto demuestra que la autoridad oficial perdio el monopolio discursivo. Opera como un tablon de anuncios unidireccional (modelo Broadcast), absorbiendo menciones pero sin fomentar debate cruzado entre la audiencia.', style={'fontSize': '14px', 'lineHeight': '1.6', 'color': '#34495E'})
                ])
            ]),

            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'alignItems': 'center', 'marginBottom': '40px'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '300px', 'textAlign': 'center'}, children=[
                    html.Img(src='/assets/comunidad_bbc_y_comentarista.png', style={'width': '100%', 'maxWidth': '550px', 'border': '1px solid #ECF0F1', 'borderRadius': '8px'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.H4('2. Pilar Mediatico y Critico: @bbcsport (1.41%)', style={'color': '#27AE60'}),
                    html.P('Sub-red liderada por la BBC y Gary Lineker. Representa la contra-narrativa sociopolitica enfocada en derechos humanos. Demuestra la capacidad del periodismo tradicional para trasladar su agenda al ecosistema digital, creando una burbuja critica aislada de la celebracion deportiva.', style={'fontSize': '14px', 'lineHeight': '1.6', 'color': '#34495E'})
                ])
            ]),

            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'alignItems': 'center', 'marginBottom': '40px'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '300px', 'textAlign': 'center'}, children=[
                    html.Img(src='/assets/comunidad_inglaterra.png', style={'width': '100%', 'maxWidth': '550px', 'border': '1px solid #ECF0F1', 'borderRadius': '8px'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.H4('3. Pilar Tribal y Nacionalista: Fanbase (0.91%)', style={'color': '#2980B9'}),
                    html.P('Aisla la conversacion puramente pasional en torno a la seleccion inglesa ("england"). Muestra aristas con mayor conectividad lateral, probando que las aficiones se agrupan en nichos impermeables, haciendo caso omiso de las controversias institucionales.', style={'fontSize': '14px', 'lineHeight': '1.6', 'color': '#34495E'})
                ])
            ]),

            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'alignItems': 'center', 'marginBottom': '40px'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '300px', 'textAlign': 'center'}, children=[
                    html.Img(src='/assets/comunidad_jiocinema.png', style={'width': '100%', 'maxWidth': '550px', 'border': '1px solid #ECF0F1', 'borderRadius': '8px'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.H4('4. Pilar Infraestructural: Crisis de @JioCinema (0.79%)', style={'color': '#D35400'}),
                    html.P('JioCinema (derechos de emision en India) sufrio caidas tecnicas severas en el partido inaugural. El surgimiento de esta red refleja a Twitter operando como servicio de atencion al cliente de facto, aglutinando la frustracion geolocalizada en tiempo real.', style={'fontSize': '14px', 'lineHeight': '1.6', 'color': '#34495E'})
                ])
            ]),

            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'alignItems': 'center'}, children=[
                html.Div(style={'flex': '1', 'minWidth': '300px', 'textAlign': 'center'}, children=[
                    html.Img(src='/assets/comunidad_elon_musk.png', style={'width': '100%', 'maxWidth': '550px', 'border': '1px solid #ECF0F1', 'borderRadius': '8px'})
                ]),
                html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                    html.H4('5. Pilar Meta-Plataforma: @elonmusk (0.79%)', style={'color': '#F39C12'}),
                    html.P('La adquisicion de la red social apenas unas semanas antes genero un fenomeno de "meta-discurso". Esta comunidad ignora el evento de futbol para interactuar exclusivamente sobre el impacto del Mundial en el rendimiento de los servidores y el trafico de la plataforma.', style={'fontSize': '14px', 'lineHeight': '1.6', 'color': '#34495E'})
                ])
            ])
        ]),

        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div([dcc.Graph(figure=fig_cross)], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}, children=[
                html.H3('Top 10 Influencers (Metricas Estructurales)', style={'textAlign': 'center', 'color': COLOR_SECCION}),
                html.P('Actores con mayor autoridad y alcance en la red.', style={'color': '#7F8C8D', 'textAlign': 'center', 'fontSize': '13px'}),
                dash_table.DataTable(
                    data=df_top_table.to_dict('records'), columns=[{"name": c, "id": c} for c in df_top_table.columns],
                    style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'center', 'padding': '8px', 'fontSize': '13px', 'fontFamily': 'Arial'},
                    style_header={'backgroundColor': '#2C3E50', 'color': 'white', 'fontWeight': 'bold'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#F8F9FA'}]
                )
            ]),
        ]),

        card([seccion_titulo('5. Conclusiones Finales'), dcc.Markdown(TEXTO_CONCLUSIONES)]),

        card([
            seccion_titulo('6. Explorador de Tuits Originales', color='#8E44AD'),
            html.Div(style={'width': '280px', 'marginBottom': '16px'}, children=[
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
                columns=[
                    {"name": "Fecha", "id": "Fecha_Completa"},
                    {"name": "Tuit (Texto Limpio)", "id": "Tweet_Limpio"},
                    {"name": "Sentimiento", "id": "Sentiment"},
                    {"name": "Likes", "id": "Number of Likes"}
                ],
                style_cell={'textAlign': 'left', 'padding': '10px', 'whiteSpace': 'normal', 'height': 'auto', 'fontSize': '13px', 'fontFamily': 'Arial'},
                style_header={'backgroundColor': '#8E44AD', 'color': 'white', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': {'filter_query': '{Sentiment} = "positive"'}, 'backgroundColor': '#EAFAF1'},
                    {'if': {'filter_query': '{Sentiment} = "negative"'}, 'backgroundColor': '#FDEDEC'},
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#F8F9FA'},
                ],
                page_size=10
            )
        ]),

        html.Footer('Trabajo Individual - Modelos Predictivos III | Analisis de Sentimiento y Opinion Publica | Qatar 2022', style={'textAlign': 'center', 'marginTop': '20px', 'color': '#95A5A6', 'fontSize': '13px'})
    ]
)

# =================================================================
# 6. LOGICA DE INTERACTIVIDAD (CALLBACKS)
# =================================================================
@app.callback(Output('tweets-table', 'data'), Input('sentiment-filter', 'value'))
def update_table(selected_sentiment):
    cols = ['Fecha_Completa', 'Tweet_Limpio', 'Sentiment', 'Number of Likes']
    cols_disponibles = [c for c in cols if c in df_limpios.columns]
    df_tweets = df_limpios[cols_disponibles].sort_values(by='Number of Likes', ascending=False)
    
    if selected_sentiment != 'all':
        df_tweets = df_tweets[df_tweets['Sentiment'] == selected_sentiment]
        
    return df_tweets.head(50).to_dict('records')

if __name__ == '__main__':
    print("El servidor del Dashboard esta arrancando...")
    print("Abre tu navegador web y entra en: http://127.0.0.1:8055/")
    app.run(debug=True, port=8055)