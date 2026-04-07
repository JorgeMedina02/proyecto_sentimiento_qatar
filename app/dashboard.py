# =================================================================
# FASE 4: DASHBOARD INTERACTIVO FINAL — MUNDIAL QATAR 2022
# Versión final con Data Storytelling y Análisis Estadístico (Gephi)
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
    print("Por favor, asegúrate de haber ejecutado todo el cuaderno de Jupyter primero.")
    exit()

# =================================================================
# 2. CONFIGURACIÓN VISUAL (ESTILOS Y COLORES)
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
# 3. CONSTRUCCIÓN DE FIGURAS ESTÁTICAS (PLOTLY)
# =================================================================

# --- Gráfico Circular: Sentimiento Global ---
fig_global = px.pie(
    df_limpios['Sentiment'].value_counts().reset_index(),
    names='Sentiment', values='count',
    title='Distribución Global del Sentimiento',
    color='Sentiment', color_discrete_map=COLORES,
    hole=0.35
)
fig_global.update_traces(textinfo='percent+label', textfont_size=13)
fig_global.update_layout(legend_title='Sentimiento', title_font_size=16)

# --- Gráfico de Líneas: Evolución Temporal ---
df_dia = df_temporal[df_temporal['granularidad'] == 'dia'] if 'granularidad' in df_temporal.columns else df_temporal
fig_time = px.line(
    df_dia, x='Fecha', y='counts', color='Sentiment',
    title='Evolución Diaria del Sentimiento',
    color_discrete_map=COLORES, markers=True
)
fig_time.update_layout(xaxis_title='Fecha', yaxis_title='Número de Tuits', legend_title='Sentimiento', title_font_size=16)

# --- Gráfico de Barras: Actividad por Hora (Si aplica) ---
df_hora = df_temporal[df_temporal['granularidad'] == 'hora'] if 'granularidad' in df_temporal.columns else pd.DataFrame()
if not df_hora.empty:
    fig_hora = px.bar(
        df_hora, x='Fecha', y='counts', color='Sentiment',
        title='Actividad por Hora del Día',
        color_discrete_map=COLORES, barmode='stack'
    )
    fig_hora.update_layout(xaxis_title='Hora (UTC)', yaxis_title='Tuits', title_font_size=16)
else:
    fig_hora = go.Figure()
    fig_hora.add_annotation(text="Datos horarios no disponibles", showarrow=False)

# --- Gráfico de Barras Agrupadas: Sentimiento por Actor/Tema ---
fig_cross = px.bar(
    df_actores, x='Actor_Tema', y='Porcentaje', color='Sentimiento',
    barmode='group',
    title='Distribución del Sentimiento por Tema/Actor Clave',
    color_discrete_map=COLORES,
    text='Porcentaje'
)
fig_cross.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_cross.update_layout(xaxis_title='Actor / Tema', yaxis_title='Porcentaje (%)', legend_title='Sentimiento', title_font_size=16, yaxis_range=[0, 80])

# --- Boxplot: Distribución de Likes ---
fig_likes = px.box(
    df_limpios, x='Sentiment', y='Number of Likes',
    color='Sentiment', color_discrete_map=COLORES,
    title='Distribución de Likes por Sentimiento',
    points='outliers'
)
fig_likes.update_layout(xaxis_title='Sentimiento', yaxis_title='Número de Likes', showlegend=False, title_font_size=16)
fig_likes.update_yaxes(type='log')  # Escala logarítmica recomendada para Likes

# =================================================================
# 4. TEXTOS ACADÉMICOS PARA EL STORYTELLING (MARKDOWN)
# =================================================================

TEXTO_INTRO = """
### 1. Pregunta de investigación y justificación

¿Cómo se distribuyó y evolucionó la opinión pública en Twitter durante el inicio del **Mundial de la FIFA Qatar 2022**? ¿Qué actores concentraron mayor volumen de conversación y qué polaridad emocional generaron?

Qatar 2022 fue un evento de alcance global con una doble dimensión analítica: la estrictamente **deportiva** (resultados, jugadores, controversias arbitrales) y la **sociopolítica** (derechos humanos, condiciones laborales, postura de la FIFA ante críticas internacionales). Esta dualidad genera un escenario especialmente rico para el análisis de sentimiento, ya que cabe esperar diferencias sustanciales en la polaridad emocional según el tema tratado.

### 2. Descripción de los datos

El dataset proviene de **Kaggle** y contiene aproximadamente **22.500 tuits recopilados durante el primer día de competición** (noviembre de 2022). Las variables principales son: texto original, fecha y hora de publicación, número de likes, fuente del dispositivo y etiqueta de sentimiento pre-asignada.

**Limitaciones reconocidas:** (a) el periodo temporal representa una ventana corta equivalente a una crónica en directo; (b) el idioma dominante es el inglés; (c) la muestra fue filtrada por hashtags específicos de la competición.
"""

TEXTO_NLP = """
### 3. Metodología de Procesamiento de Lenguaje Natural (NLP)

El pipeline de limpieza aplicó las siguientes transformaciones para garantizar la calidad analítica:
1. **Eliminación de ruido:** Purga de URLs y menciones (@usuario) que carecen de valor semántico directo en el análisis de texto.
2. **Normalización:** Conversión a minúsculas y eliminación de caracteres no alfanuméricos.
3. **Análisis de Polaridad:** Agregación estadística de los sentimientos (positivo, neutro, negativo) para cruzar las emociones predominantes con entidades o palabras clave extraídas del texto.
"""

TEXTO_ARS = """
### 4. Metodología del Análisis de Redes Sociales (ARS)

Para comprender la propagación de la información, se construyó un **grafo dirigido de menciones** usando la librería matemática `NetworkX` en Python:
- **Nodos:** Tuits originales y usuarios explícitamente mencionados.
- **Aristas:** Dirección e intensidad de la interacción (mención).

El modelo estructural fue exportado a **Gephi 0.10.1** para su especialización espacial (algoritmo *ForceAtlas2*) y la ejecución de cálculos estadísticos avanzados para la detección de comunidades herméticas (algoritmo *Louvain*).
"""

TEXTO_CONCLUSIONES = """
### 5. Conclusiones y Hallazgos Principales

**1. Sentimiento Global y Polarización Temática:** Predomina el sentimiento neutro, reflejando el carácter puramente informativo de la red en eventos en vivo. Sin embargo, al segmentar por temas, se confirma que las entidades deportivas (*Messi*, *Ronaldo*) operan como catalizadores de positividad, mientras que las instituciones organizativas (*FIFA*, *Qatar*, *VAR*) concentran la negatividad ciudadana.

**2. Topología de Difusión (Broadcast):** El análisis de centralidad demuestra que la opinión pública operó bajo un modelo radial o de estrella. Miles de usuarios enviaron mensajes al vacío o directamente a cuentas hiper-populares, sin tejer verdaderas redes de debate o hilos de respuestas profundos (Diámetro 1 y Grado medio bajo).

**3. Fractura del Discurso (Cámaras de Eco):** La altísima modularidad estadística de la red (0.932) certifica que la conversación global es una ilusión. El debate está profundamente fragmentado en micro-comunidades aisladas que ignoran a las demás, encerrando a los usuarios en cámaras de eco ideológicas, idiomáticas o deportivas.
"""

# =================================================================
# 5. ESTRUCTURA HTML DE LA APLICACIÓN (LAYOUT)
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

        # ---- CABECERA PRINCIPAL ----
        html.Div(style={
            'background': 'linear-gradient(135deg, #1A252F 0%, #2C3E50 100%)',
            'padding': '40px', 'borderRadius': '12px', 'marginBottom': '28px', 'textAlign': 'center', 'color': 'white'
        }, children=[
            html.H1('⚽ Análisis de Opinión Pública', style={'margin': '0', 'fontSize': '2.2em'}),
            html.H2('Copa Mundial de la FIFA — Qatar 2022', style={'margin': '8px 0', 'fontWeight': '300', 'fontSize': '1.4em'}),
            html.P('Análisis de Sentimiento · Procesamiento de Lenguaje Natural · Análisis de Redes Sociales', style={'margin': '0', 'opacity': '0.75'})
        ]),

        # ---- TARJETAS DE INDICADORES (KPIs) ----
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

        # ---- BLOQUE 1: INTRODUCCIÓN Y CONTEXTO ----
        card([seccion_titulo('1. Introducción y Descripción de los Datos'), dcc.Markdown(TEXTO_INTRO)]),

        # ---- BLOQUE 2: SENTIMIENTO GLOBAL Y LIKES ----
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div([dcc.Graph(figure=fig_global, config={'displayModeBar': False})], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
            html.Div([dcc.Graph(figure=fig_likes, config={'displayModeBar': False})], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
        ]),

        # ---- BLOQUE 3: METODOLOGÍA NLP Y EVOLUCIÓN TEMPORAL ----
        card([seccion_titulo('2. Metodología de Procesamiento de Lenguaje Natural'), dcc.Markdown(TEXTO_NLP)]),
        card([
            seccion_titulo('3. Evolución Temporal del Sentimiento'),
            html.P('La serie temporal permite identificar picos de actividad correlacionables con la inauguración del torneo.', style={'color': '#7F8C8D', 'marginTop': '0'}),
            html.Div(style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}, children=[
                html.Div([dcc.Graph(figure=fig_time)], style={'flex': '1', 'minWidth': '300px'}),
                html.Div([dcc.Graph(figure=fig_hora)], style={'flex': '1', 'minWidth': '300px'}),
            ])
        ]),

        # ---- BLOQUE 4: METODOLOGÍA ARS ----
        card([seccion_titulo('4. Metodología del Análisis de Redes Sociales (ARS) y Gephi'), dcc.Markdown(TEXTO_ARS)]),

        # ---- BLOQUE 4.1: VISUALIZACIÓN GEPHI INTERACTIVA ----
        card([
            seccion_titulo('4.1 Sociograma — Red de Menciones (Exportado desde Gephi)'),
            html.P(['Topología interactiva de los usuarios. Nodos coloreados por comunidad (Algoritmo de Louvain); tamaño proporcional a la influencia central del usuario. Usa la rueda del ratón para hacer zoom sobre el núcleo de la red.'], style={'color': '#7F8C8D'}),
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

        # ---- BLOQUE 4.2: GRÁFICOS MATEMÁTICOS DE GEPHI ----
        card([
            seccion_titulo('4.2 Análisis Estadístico Topológico (Reportes de Gephi)'),
            html.P('El análisis de las distribuciones estadísticas confirma matemáticamente la topología visualizada.', style={'color': '#7F8C8D', 'marginBottom': '20px'}),
            
            html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap'}, children=[
                
                # Gráfica 1: Betweenness
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Ausencia de Nodos Puente (Betweenness)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/Betweenness_Centrality_Distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('La inmensa mayoría de los nodos (pico en el 0) carecen de capacidad de intermediación. No hay usuarios que actúen como "puentes" conectando diferentes grupos; la información no fluye de forma transversal.', style={'fontSize': '14px', 'color': '#34495E'})
                ]),

                # Gráfica 2: Closeness
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Estructura de Estrella (Closeness)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/Closeness_Centrality_Distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('Observamos dos picos extremos en 0 y en 1. Esto demuestra que la red tiene un diámetro de 1: los usuarios están aislados (0) o interactúan en un único paso (1) con grandes cuentas centrales. No existen cadenas largas de retuits o respuestas.', style={'fontSize': '14px', 'color': '#34495E'})
                ]),

                # Gráfica 3: Degree
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Distribución de Grado (Ley de Potencias)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/degree-distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('Con un grado medio de apenas 0.257, la curva refleja una distribución Power-Law pura. El 99% de los usuarios participan como emisores pasivos (polvo periférico en el eje Y), mientras que la atención y las menciones son acaparadas por menos del 1% de los actores (hubs en el eje X).', style={'fontSize': '14px', 'color': '#34495E'})
                ]),

                # Gráfica 4: Modularidad
                html.Div(style={'flex': '1', 'minWidth': '45%'}, children=[
                    html.H4('Fragmentación Extrema (Comunidades)', style={'color': '#2980B9'}),
                    html.Img(src='/assets/communities-size-distribution.png', style={'width': '100%', 'border': '1px solid #ECF0F1', 'borderRadius': '5px'}),
                    html.P('La Modularidad de Louvain (0.932) es extremadamente alta. La gráfica de dispersión ilustra la formación de unas pocas "cámaras de eco" grandes y miles de micro-comunidades desconectadas (la línea roja inferior). El debate está completamente fracturado.', style={'fontSize': '14px', 'color': '#34495E'})
                ])
            ])
        ]),

        # ---- BLOQUE 4.3: POLARIZACIÓN Y TOP INFLUENCERS ----
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div([dcc.Graph(figure=fig_cross)], style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'minWidth': '320px', 'marginBottom': '0'}, children=[
                html.H3('Top 10 Influencers (Métricas Estructurales)', style={'textAlign': 'center', 'color': COLOR_SECCION}),
                html.P('Actores con mayor autoridad y alcance en la red.', style={'color': '#7F8C8D', 'textAlign': 'center', 'fontSize': '13px'}),
                dash_table.DataTable(
                    data=df_top_table.to_dict('records'), columns=[{"name": c, "id": c} for c in df_top_table.columns],
                    style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'center', 'padding': '8px', 'fontSize': '13px', 'fontFamily': 'Arial'},
                    style_header={'backgroundColor': '#2C3E50', 'color': 'white', 'fontWeight': 'bold'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#F8F9FA'}]
                )
            ]),
        ]),

        # ---- BLOQUE 5: CONCLUSIONES ----
        card([seccion_titulo('5. Conclusiones Finales'), dcc.Markdown(TEXTO_CONCLUSIONES)]),

        # ---- BLOQUE 6: EXPLORADOR DE DATOS ----
        card([
            seccion_titulo('6. Explorador de Tuits Originales', color='#8E44AD'),
            html.P('Filtra la base de datos por polaridad para explorar cualitativamente el discurso ciudadano que mayor interacción generó.', style={'color': '#7F8C8D'}),
            html.Div(style={'width': '280px', 'marginBottom': '16px'}, children=[
                dcc.Dropdown(
                    id='sentiment-filter',
                    options=[
                        {'label': '🌐 Todos', 'value': 'all'},
                        {'label': '✅ Positivo', 'value': 'positive'},
                        {'label': '➖ Neutral', 'value': 'neutral'},
                        {'label': '❌ Negativo', 'value': 'negative'}
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

        # ---- PIE DE PÁGINA ----
        html.Footer('📊 Trabajo Individual — Modelos Predictivos III · Análisis de Sentimiento y Opinión Pública · Qatar 2022', style={'textAlign': 'center', 'marginTop': '20px', 'color': '#95A5A6', 'fontSize': '13px'})
    ]
)

# =================================================================
# 6. LÓGICA DE INTERACTIVIDAD (CALLBACKS)
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
    print("\n🚀 El servidor del Dashboard está arrancando...")
    print("👉 Abre tu navegador web y entra en: http://127.0.0.1:8055/")
    app.run(debug=True, port=8055)