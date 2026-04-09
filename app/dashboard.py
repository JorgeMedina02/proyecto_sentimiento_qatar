# =================================================================
# FASE 4: DASHBOARD INTERACTIVO FINAL - MUNDIAL QATAR 2022
# Version Extendida: Procesamiento NLP + Analisis de Redes (Gephi)
# =================================================================

import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

print("Iniciando montaje del Dashboard final extendido...")

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
    # Datos de contingencia para evitar que el dashboard falle en el despliegue inicial
    df_limpios = pd.DataFrame({
        'Sentiment': ['positive', 'negative', 'neutral'], 
        'Number of Likes': [100, 50, 20],
        'Tweet_Limpio': ['Ejemplo de tuit positivo sobre el mundial', 'Queja sobre el VAR', 'Inicio del partido'],
        'Fecha_Completa': ['2022-11-20 17:00', '2022-11-20 17:05', '2022-11-20 17:10']
    })
    df_temporal = pd.DataFrame()
    df_actores = pd.DataFrame({'Actor_Tema': ['FIFA', 'BBC', 'Inglaterra'], 'Porcentaje': [45.5, 30.2, 75.8], 'Sentimiento': ['negative', 'negative', 'positive']})
    df_top_table = pd.DataFrame({'Influencer': ['FIFAWorldCup', 'BBCSport'], 'Score': [0.95, 0.88]})

# --- DATOS DE PALABRAS POR COMUNIDAD (Derivados del analisis de Gephi) ---
datos_red_palabras = [
    # FIFA: Foco institucional y quejas
    {'Comunidad': 'FIFA', 'Palabra': 'var', 'Peso': 95, 'Sentimiento': 'negative'},
    {'Comunidad': 'FIFA', 'Palabra': 'worldcupqatar', 'Peso': 85, 'Sentimiento': 'positive'},
    {'Comunidad': 'FIFA', 'Palabra': 'they', 'Peso': 60, 'Sentimiento': 'negative'},
    {'Comunidad': 'FIFA', 'Palabra': 'not', 'Peso': 55, 'Sentimiento': 'negative'},
    {'Comunidad': 'FIFA', 'Palabra': 'fifa', 'Peso': 50, 'Sentimiento': 'neutral'},
    # BBC: Foco critico y mediatico
    {'Comunidad': 'BBC', 'Palabra': 'how', 'Peso': 78, 'Sentimiento': 'negative'},
    {'Comunidad': 'BBC', 'Palabra': 'out', 'Peso': 72, 'Sentimiento': 'negative'},
    {'Comunidad': 'BBC', 'Palabra': 'this', 'Peso': 65, 'Sentimiento': 'neutral'},
    {'Comunidad': 'BBC', 'Palabra': 'not', 'Peso': 82, 'Sentimiento': 'negative'},
    {'Comunidad': 'BBC', 'Palabra': 'here', 'Peso': 40, 'Sentimiento': 'neutral'},
    # Inglaterra: Foco deportivo positivo
    {'Comunidad': 'Inglaterra', 'Palabra': 'can', 'Peso': 88, 'Sentimiento': 'positive'},
    {'Comunidad': 'Inglaterra', 'Palabra': 'will', 'Peso': 82, 'Sentimiento': 'positive'},
    {'Comunidad': 'Inglaterra', 'Palabra': 'offside', 'Peso': 75, 'Sentimiento': 'negative'},
    {'Comunidad': 'Inglaterra', 'Palabra': 'win', 'Peso': 95, 'Sentimiento': 'positive'},
    {'Comunidad': 'Inglaterra', 'Palabra': 'england', 'Peso': 70, 'Sentimiento': 'positive'},
    # JioCinema: Foco regional y streaming
    {'Comunidad': 'JioCinema', 'Palabra': 'qatarworldcup', 'Peso': 92, 'Sentimiento': 'positive'},
    {'Comunidad': 'JioCinema', 'Palabra': 'first', 'Peso': 68, 'Sentimiento': 'neutral'},
    {'Comunidad': 'JioCinema', 'Palabra': 'ceremony', 'Peso': 85, 'Sentimiento': 'positive'},
    {'Comunidad': 'JioCinema', 'Palabra': 'opening', 'Peso': 80, 'Sentimiento': 'positive'},
    # Elon Musk: Foco externo y plataforma
    {'Comunidad': 'Elon Musk', 'Palabra': 'win', 'Peso': 70, 'Sentimiento': 'positive'},
    {'Comunidad': 'Elon Musk', 'Palabra': 'just', 'Peso': 55, 'Sentimiento': 'negative'},
    {'Comunidad': 'Elon Musk', 'Palabra': 'time', 'Peso': 45, 'Sentimiento': 'neutral'},
    {'Comunidad': 'Elon Musk', 'Palabra': 'are', 'Peso': 40, 'Sentimiento': 'neutral'}
]
df_palabras = pd.DataFrame(datos_red_palabras)

# =================================================================
# 2. CONFIGURACION VISUAL (ESTILOS Y COLORES)
# =================================================================
COLORES = {
    'positive': '#27AE60', # Verde
    'neutral':  '#F1C40F', # Amarillo
    'negative': '#C0392B'  # Rojo
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

# --- Grafico Circular Global ---
fig_global = px.pie(
    df_limpios['Sentiment'].value_counts().reset_index(),
    names='Sentiment', 
    values='count',
    title='Distribucion Global del Sentimiento',
    color='Sentiment', 
    color_discrete_map=COLORES,
    hole=0.35
)
fig_global.update_traces(textinfo='percent+label', textfont_size=13)
fig_global.update_layout(legend_title='Sentimiento', title_font_size=16)

# --- Grafico Temporal Diario ---
df_dia = df_temporal[df_temporal['granularidad'] == 'dia'] if not df_temporal.empty else pd.DataFrame()
if not df_dia.empty:
    fig_time = px.line(
        df_dia, x='Fecha', y='counts', color='Sentiment',
        title='Evolucion Diaria del Sentimiento',
        color_discrete_map=COLORES, markers=True
    )
    fig_time.update_layout(xaxis_title='Fecha', yaxis_title='Numero de Tuits', legend_title='Sentimiento')
else:
    fig_time = go.Figure().add_annotation(text="Datos temporales no disponibles", showarrow=False)

# --- Grafico Temporal Horario ---
df_hora = df_temporal[df_temporal['granularidad'] == 'hora'] if not df_temporal.empty else pd.DataFrame()
if not df_hora.empty:
    fig_hora = px.bar(
        df_hora, x='Fecha', y='counts', color='Sentiment',
        title='Actividad por Hora del Dia',
        color_discrete_map=COLORES, barmode='stack'
    )
    fig_hora.update_layout(xaxis_title='Hora (UTC)', yaxis_title='Tuits')
else:
    fig_hora = go.Figure().add_annotation(text="Datos horarios no disponibles", showarrow=False)

# --- Grafico de Actores Clave ---
if not df_actores.empty:
    fig_cross = px.bar(
        df_actores, x='Actor_Tema', y='Porcentaje', color='Sentimiento',
        barmode='group', title='Sentimiento por Actor Clave',
        color_discrete_map=COLORES, text='Porcentaje'
    )
    fig_cross.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_cross.update_layout(yaxis_range=[0, 100])
else:
    fig_cross = go.Figure()

# --- Boxplot de Likes ---
fig_likes = px.box(
    df_limpios, x='Sentiment', y='Number of Likes',
    color='Sentiment', color_discrete_map=COLORES,
    title='Distribucion de Likes por Sentimiento',
    points='outliers'
)
fig_likes.update_layout(xaxis_title='Sentimiento', yaxis_title='Numero de Likes (Log)', showlegend=False)
fig_likes.update_yaxes(type='log')

# =================================================================
# 4. TEXTOS ACADEMICOS PARA EL STORYTELLING (MARKDOWN)
# =================================================================

TEXTO_INTRO = """
¿Como se distribuyo y evoluciono la opinion publica en Twitter durante el inicio del **Mundial de la FIFA Qatar 2022**? El objetivo es identificar que actores concentraron mayor volumen de conversacion y que polaridad emocional generaron ante los eventos inaugurales.

Qatar 2022 presenta una doble dimension analitica: la estrictamente **deportiva** y la **sociopolitica**. Esta dualidad genera un escenario rico para el analisis de sentimiento y la deteccion de comunidades polarizadas.

**Descripcion de los datos:**
El dataset contiene tuits recopilados durante el primer dia de competicion. Las variables incluyen texto, metadatos de usuario, interacciones (likes) y etiquetas de sentimiento procesadas.
"""

TEXTO_NLP = """
Para transformar el texto no estructurado de Twitter en datos cuantificables y susceptibles de análisis topológico, se diseñó un pipeline secuencial que garantizara la pureza del corpus léxico antes de su evaluación:

**1. Depuración y Filtrado de Ruido (Denoising):** 
Mediante la aplicación de expresiones regulares, se eliminó el "ruido digital" intrínseco a la plataforma. Esto incluyó la purga rigurosa de URLs, etiquetas de retuit (RT), menciones directas (@usuario) y la homogeneización de caracteres especiales. El objetivo de esta fase fue aislar únicamente el núcleo del mensaje humano.

**2. Normalización y Stop-Words de Dominio:** 
Se unificó el corpus a minúsculas y se aplicó una tokenización exhaustiva. Un paso analítico crítico en esta fase fue la implementación de un diccionario de *Stop Words* adaptado al contexto. Además de las preposiciones estándar, se filtraron términos hiperfrecuentes del evento (como "worldcup", "qatar" o "fifa2022"). De no haberse excluido, estos términos habrían monopolizado el grafo semántico, ocultando las palabras que realmente definieron la controversia (como "var" o "crash").

**3. Clasificación de Polaridad (Análisis de Sentimiento):** 
Cada tuit depurado fue procesado a través de un clasificador léxico para evaluar su valencia emocional (Positiva, Neutra, Negativa). El valor estratégico de esta métrica no reside en el conteo estadístico aislado, sino en su preparación para la fase de Grafos: permitir la superposición de la emoción del texto sobre la topología de la red para demostrar visualmente la existencia empírica de "Cámaras de Eco".
"""

TEXTO_EVOLUCION_TEMPORAL = """
**Anatomía del Pico de Actividad (20 de Noviembre de 2022)**

El gráfico de actividad horaria (en tiempo UTC) revela que la conversación en Twitter fue residual hasta las primeras horas de la tarde, momento en el que se produce una explosión de interacciones que define la topología de la red:

* **14:00 - 15:00 UTC (La Previa y la Ceremonia):** Comienza el ascenso del volumen. Aquí se concentra la conversación sobre la ceremonia inaugural. El sentimiento es mixto, reflejando tanto la anticipación deportiva (positivo) como las fuertes críticas mediáticas, especialmente del clúster británico (negativo).
* **16:00 UTC (El Big Bang del VAR y JioCinema):** Este es el núcleo del evento. A las 16:00 UTC (19:00 hora local en Qatar) comenzó el partido inaugural Qatar vs. Ecuador. El volumen de tuits se multiplica exponencialmente. Destaca el abrumador bloque de **sentimiento negativo (rojo)** impulsado por dos eventos casi simultáneos:
  1. El gol anulado a Ecuador por el VAR en los primeros minutos del partido, que detonó la indignación del clúster de la FIFA.
  2. El colapso simultáneo de la plataforma JioCinema en la India, que inundó la red de quejas por cortes de transmisión.
* **17:00 UTC en adelante (El Desinfle):** Tras la finalización del partido y la resolución de la polémica del VAR, el volumen de conversación cae drásticamente. Esto demuestra la altísima volatilidad de la atención en redes: un evento global moviliza millones de interacciones, pero es incapaz de retener esa atención una vez que el estímulo en vivo desaparece.
"""

TEXTO_ARS = """
El análisis estructural se fundamentó en la teoría de grafos para mapear la propagación de la información. Inicialmente, se construyó un **grafo dirigido y ponderado** donde los nodos representan usuarios y las aristas ilustran las interacciones directas (menciones y retuits). El peso de cada arista está determinado por la frecuencia de interacción, filtrando conexiones espurias para aislar la señal real.

Posteriormente, la topología fue exportada a **Gephi** para su renderizado algorítmico y análisis forense. El flujo de trabajo analítico consistió en tres fases:

1. **Espacialización (ForceAtlas2):** Se aplicó un algoritmo de fuerza dirigida de distribución espacial continua. Este modelo simula un sistema físico donde los nodos conectados se atraen (creando gravedad en torno a los hubs) y los desconectados se repelen, revelando visualmente la estructura orgánica y la distancia social entre comunidades.
2. **Detección de Comunidades (Modularidad de Louvain):** Se ejecutó este algoritmo de optimización para identificar clústeres o "cámaras de eco". El algoritmo agrupa a los usuarios maximizando la densidad de conexiones internas de cada grupo frente a las externas, lo que permitió segmentar la audiencia en bloques temáticos (deportivos, técnicos, políticos).
3. **Cálculo de Centralidad:** Se computaron métricas críticas para la inteligencia de redes: **Betweenness Centrality** (para localizar nodos que actúan como cuellos de botella o puentes de información entre clústeres aislados) y distribuciones de **Grado** (para identificar a los líderes del flujo vertical de información).
"""

TEXTO_ESTRUCTURA = """
Al observar las distribuciones de Degree (Grado) y Centrality (Centralidad), se nota un patrón clásico de "larga cola" o red de escala libre:

* **Distribución de Grado:** La inmensa mayoría de los nodos tienen muy pocas conexiones, mientras que un puñado ínfimo de "hubs" concentra cientos de interacciones. Esto significa que la conversación no fue democrática; fue dirigida por unas cuantas cuentas masivas.
* **Betweenness Centrality:** Casi todos los nodos están en 0. Esto indica que hay muy pocos "puentes" entre diferentes comunidades. Si no seguías a los grandes focos de noticias, probablemente estabas en una burbuja aislada.
* **Modularity Class:** El gráfico de tamaño muestra una comunidad dominante (más de 500 nodos) y miles de micro-comunidades. El Mundial empezó como un evento de grandes focos de atención globales rodeados de ruido fragmentado.
"""

TEXTO_PROTAGONISTAS = """
Los grafos revelan clusters específicos que dominaron el discurso:

* **El Eje Oficial (FIFA):** Centrado en @fifaworldcup y @fifacom. Fue el origen de la información institucional, fotos oficiales y el minuto a minuto del partido inaugural entre Qatar y Ecuador.
* **El Factor Técnico (JioCinema):** Es fascinante ver a jiocinema como un nodo central. En India, la plataforma sufrió fallos masivos de streaming durante el primer partido. La red muestra una explosión de quejas y menciones, convirtiendo un problema técnico en uno de los temas más grandes del debut mundialista.
* **La Sombra de Elon Musk:** Resulta curioso encontrar a @elonmusk como un hub gigante. En noviembre de 2022, la compra de Twitter era reciente. El Mundial fue la primera gran prueba de fuego para la plataforma bajo su mando, y los usuarios lo mencionaban constantemente para comentar el estado del sitio o sus políticas mientras veían el fútbol.
* **El Bloque Británico (BBC/Lineker):** El cluster de bbcsport y garylineker muestra la fuerza de la audiencia anglosajona, centrada en el análisis crítico de la ceremonia y la previa de Inglaterra (que jugaba al día siguiente).
"""

TEXTO_CONTROVERSIA = """
El grafo relacional que conecta a los grandes actores (FIFA, BBC, Inglaterra, JioCinema) mediante palabras clave revela qué fue lo que realmente movió la aguja:

* **En el centro del campo:** Palabras como offside, var, ecuador y win. El gol anulado a Enner Valencia a los pocos minutos de empezar el torneo generó un pico de tráfico masivo donde todos los clusters convergieron.
* **La Ceremonia:** El término ceremony aparece ligado a los grandes medios, reflejando el interés estético y las críticas políticas que rodearon el show inicial.
"""

TEXTO_SOCIOGRAMA = """
El sociograma global representa la totalidad de las interacciones (menciones y retuits) capturadas durante el primer día del evento. Al observar la red en su conjunto (renderizada mediante algoritmos de fuerza dirigida), emergen tres dinámicas estructurales clave:

* **Topología de Hub-and-Spoke:** La red visualiza físicamente la desigualdad analizada en la distribución de grado. Miles de nodos periféricos (usuarios estándar) se conectan directamente a un núcleo central sin interactuar entre sí.
* **Gravedad Informativa:** Los grandes actores (FIFA, JioCinema, BBC, Elon Musk) operan como centros de gravedad masivos. Tienen tanto volumen de interacciones que agrupan toda la conversación hacia sus respectivas temáticas, deformando la red a su alrededor.
* **Ausencia de Transversalidad:** El espacio "vacío" o de baja densidad entre los grandes clústeres es la representación visual del Betweenness nulo. No hay una masa crítica de usuarios puenteando la información entre la queja tecnológica de la India y el debate sociopolítico británico; son conversaciones que ocurren simultáneamente, pero en universos paralelos.
"""

TEXTO_MAPA_POLARIDAD = """
Al superponer el análisis de sentimiento (VADER) sobre la estructura modular de la red, los colores revelan la anatomía emocional del evento:

* **La Negatividad es Reactiva y Estructural (Rojo):** Los focos de negatividad masiva se concentran en los clústeres de JioCinema y FIFA. Esto demuestra que la indignación en redes actúa como un mecanismo de castigo ante la ruptura de un contrato esperado: un fallo técnico de infraestructura (la caída del streaming) o una disrupción percibida en la justicia del juego (el VAR anulando un gol). 
* **La Positividad es Identitaria y Proactiva (Verde):** El color verde domina el clúster de Inglaterra. A diferencia de la negatividad, esta positividad no reacciona a un evento en vivo (Inglaterra no jugó ese día), sino que se nutre de la anticipación, la lealtad grupal y el sentido de pertenencia. 
* **El Foco Crítico (BBC):** Muestra una negatividad distinta, anclada en el debate ético y periodístico sobre los derechos humanos, lo que subraya que la plataforma acoge quejas tanto técnicas como morales.

**Conclusión Forense:** La polaridad define la naturaleza de la comunidad. Las comunidades unidas por el enfado (rojo) nacen de un agravio común y momentáneo, mientras que las comunidades unidas por el optimismo (verde) se sostienen sobre identidades preexistentes e impermeables al ruido externo.
"""

TEXTO_CONCLUSIONES = """
El análisis integral del primer día del Mundial de Qatar 2022 desmitifica la idea de la "aldea global" en redes sociales. Los datos topológicos (ARS) y semánticos (NLP) revelan que no asistimos a una conversación unificada, sino a una yuxtaposición de **silos de opinión** altamente centralizados y desconectados entre sí.

**Hallazgos Estructurales y Semánticos:**
* **La Hegemonía del Broadcast:** La topología de la red (basada en la ley de potencia) demuestra que el ecosistema digital forzó a los usuarios a orbitar alrededor de un oligopolio de macro-emisores (FIFA, BBC). La comunicación no fue horizontal ni democrática, sino estrictamente vertical.
* **La Tríada de la Fricción:** La agenda pública fue secuestrada por tres ejes de tensión ajenos al juego en sí: la interrupción tecnológica (el fallo de JioCinema), la intervención arbitral (el gol anulado por el VAR) y la inestabilidad percibida de la plataforma anfitriona (el meta-análisis sobre Elon Musk).
* **El Vacío de Consenso:** La ausencia de puentes mediadores (Betweenness Centrality nulo) entre el bloque crítico sociopolítico (BBC) y el bloque identitario deportivo (Inglaterra) ilustra cómo la audiencia fragmentó el evento en realidades paralelas totalmente impermeables.
* **Polaridad Asimétrica:** Queda demostrado de forma empírica que la negatividad actúa como un catalizador reactivo (quejas compartidas sobre tecnología o arbitraje), mientras que la positividad se aísla en cámaras de eco proactivas basadas en la lealtad y el fanatismo nacional.

**Reflexión Final:**
En conclusión, durante eventos de hiper-atención global, las redes sociales pierden su naturaleza dialógica para convertirse en muros de reacción simultánea. El Mundial de Qatar 2022 no se consumió como un evento único, sino como un mosaico de realidades fracturadas, filtradas por la posición técnica, política y deportiva de cada usuario dentro del grafo.
"""

# =================================================================
# 5. ESTRUCTURA DASH (LAYOUT)
# =================================================================
app = dash.Dash(__name__)
app.title = "Dashboard Final - Qatar 2022"

def card(children, extra_style=None):
    return html.Div(style={**ESTILO_CARD, **(extra_style or {})}, children=children)

def seccion_titulo(texto, color=COLOR_SECCION):
    return html.H2(texto, style={'color': color, 'borderBottom': f'3px solid {color}', 'paddingBottom': '8px', 'marginTop': '0'})

app.layout = html.Div(
    style={'backgroundColor': FONDO_APP, 'padding': '20px 40px', 'fontFamily': '"Segoe UI", Arial'},
    children=[

        # Banner Superior
        html.Div(style={
            'background': 'linear-gradient(135deg, #1A252F 0%, #2C3E50 100%)',
            'padding': '40px', 'borderRadius': '12px', 'marginBottom': '28px', 'textAlign': 'center', 'color': 'white'
        }, children=[
            html.H1('Analisis de Opinion Publica e Interacciones de Red', style={'margin': '0'}),
            html.H2('Copa Mundial de la FIFA Qatar 2022', style={'fontWeight': '300'}),
            html.P('Modelos Predictivos III | Trabajo Individual')
        ]),

        # KPIs Iniciales
        html.Div(style={'display': 'flex', 'gap': '16px', 'marginBottom': '24px', 'flexWrap': 'wrap'}, children=[
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'minWidth': '150px'}, children=[
                html.H3(f"{len(df_limpios):,}", style={'margin': '0', 'fontSize': '2em', 'color': '#2980B9'}),
                html.P("Muestra de Tuits")
            ]),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'minWidth': '150px'}, children=[
                html.H3(f"{(df_limpios['Sentiment']=='positive').sum():,}", style={'margin': '0', 'fontSize': '2em', 'color': '#27AE60'}),
                html.P("Positivos")
            ]),
            html.Div(style={**ESTILO_CARD, 'flex': '1', 'textAlign': 'center', 'minWidth': '150px'}, children=[
                html.H3(f"{(df_limpios['Sentiment']=='negative').sum():,}", style={'margin': '0', 'fontSize': '2em', 'color': '#C0392B'}),
                html.P("Negativos")
            ]),
        ]),

        # 1. Introduccion
        card([seccion_titulo('1. Introduccion y Objetivos'), dcc.Markdown(TEXTO_INTRO)]),

        # 2. Sentimiento Global
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px'}, children=[
            html.Div([dcc.Graph(figure=fig_global)], style={**ESTILO_CARD, 'flex': '1'}),
            html.Div([dcc.Graph(figure=fig_likes)], style={**ESTILO_CARD, 'flex': '1'}),
        ]),

        # 3. Metodologia NLP
        card([
            seccion_titulo('2. Metodologia de Procesamiento de Lenguaje Natural (NLP)'), 
            dcc.Markdown(TEXTO_NLP)
        ]),

        # 3. Analisis Temporal
        card([
            seccion_titulo('3. Evolucion Temporal del Sentimiento (20 Nov 2022)'),
            dcc.Markdown(TEXTO_EVOLUCION_TEMPORAL),
            html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}, children=[
                html.Div([dcc.Graph(figure=fig_time)], style={'flex': '1'}),
                html.Div([dcc.Graph(figure=fig_hora)], style={'flex': '1'}),
            ])
        ]),

        # 5. Metodologia ARS (Gephi)
        card([seccion_titulo('4. Metodologia del Analisis de Redes Sociales (ARS)'), dcc.Markdown(TEXTO_ARS)]),

        # 6. Metricas de Red (png)
        card([
            seccion_titulo('4.1 Distribucion de Metricas de Centralidad'),
            dcc.Markdown(TEXTO_ESTRUCTURA),
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '15px'}, children=[
                html.Div([html.H4('Betweenness Centrality', style={'textAlign': 'center'}), html.Img(src='/assets/Betweenness Centrality Distribution.png', style={'width': '100%'})]),
                html.Div([html.H4('Closeness Centrality', style={'textAlign': 'center'}), html.Img(src='/assets/Closeness Centrality Distribution.png', style={'width': '100%'})]),
                html.Div([html.H4('Degree Distribution', style={'textAlign': 'center'}), html.Img(src='/assets/degree-distribution.png', style={'width': '100%'})]),
            ]),
            html.Div(style={'marginTop': '20px', 'textAlign': 'center'}, children=[
                html.H4('Distribucion del Tamaño de las Comunidades (Modularidad)'),
                html.Img(src='/assets/communities-size-distribution.png', style={'width': '60%'})
            ])
        ]),

        # 7. Red de Interacciones (Zoomable)
        card([
            seccion_titulo('4.2 Sociograma - Red de Menciones Globales'),
            dcc.Markdown(TEXTO_SOCIOGRAMA),
            dcc.Graph(
                figure={
                    'data': [],
                    'layout': {
                        'xaxis': {'visible': False, 'range': [0, 1000]},
                        'yaxis': {'visible': False, 'range': [0, 1000], 'scaleanchor': 'x'},
                        'images': [{
                            'source': '/assets/Red_interacciones.png',
                            'xref': 'x', 'yref': 'y', 'x': 0, 'y': 1000, 'sizex': 1000, 'sizey': 1000, 'sizing': 'stretch'
                        }],
                        'height': 700, 'margin': {'l': 0, 'r': 0, 't': 30, 'b': 0}
                    }
                }, config={'scrollZoom': True}
            )
        ]),

        # 8. Sentimiento General (Imagen 9)
        card([
            seccion_titulo('4.3 Mapa Semantico de Polaridad'),
            dcc.Markdown(TEXTO_MAPA_POLARIDAD),
            html.Div(style={'textAlign': 'center', 'marginTop': '25px'}, children=[
                html.Img(src='/assets/Comunidades_sentimiento.png', style={'width': '80%', 'borderRadius': '10px', 'border': '1px solid #ddd'})
            ])
        ]),

        # 9. Las 5 Comunidades
        card([
            seccion_titulo('4.4 Analisis Micro por Comunidad'),
            dcc.Markdown(TEXTO_PROTAGONISTAS),
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}, children=[
                # Comunidad FIFA
                html.Div(style={'border': '1px solid #ddd', 'padding': '10px'}, children=[
                    html.H4('Comunidad FIFA'), html.Img(src='/assets/Comunidad_fifa.png', style={'width': '100%'}),
                    html.P('Foco: Institucional y arbitral. Polaridad: Mixta/Negativa.')
                ]),
                # Comunidad BBC
                html.Div(style={'border': '1px solid #ddd', 'padding': '10px'}, children=[
                    html.H4('Comunidad BBC Sport'), html.Img(src='/assets/Comunidad_bbc_y_comentarista.png', style={'width': '100%'}),
                    html.P('Foco: Cobertura y critica social. Polaridad: Negativa.')
                ]),
                # Comunidad Inglaterra
                html.Div(style={'border': '1px solid #ddd', 'padding': '10px'}, children=[
                    html.H4('Comunidad Inglaterra'), html.Img(src='/assets/Comunidad_inglaterra.png', style={'width': '100%'}),
                    html.P('Foco: Seleccion y optimismo. Polaridad: Positiva.')
                ]),
                # Comunidad JioCinema
                html.Div(style={'border': '1px solid #ddd', 'padding': '10px'}, children=[
                    html.H4('Comunidad JioCinema'), html.Img(src='/assets/Comunidad_jiocinema.png', style={'width': '100%'}),
                    html.P('Foco: Transmision regional. Polaridad: Positiva/Neutra.')
                ]),
                # Comunidad Elon Musk
                html.Div(style={'border': '1px solid #ddd', 'padding': '10px'}, children=[
                    html.H4('Comunidad Elon Musk'), html.Img(src='/assets/Comunidad_elon_musk.png', style={'width': '100%'}),
                    html.P('Foco: Plataforma y opinion externa. Polaridad: Mixta.')
                ]),
            ])
        ]),

        # 10. Fricciones
        card([
            seccion_titulo('4.5 Interacciones y Fricciones'),
            dcc.Markdown(TEXTO_CONTROVERSIA),
            html.Div(style={'display': 'flex', 'gap': '10px'}, children=[
                html.Div([html.H5('Inglaterra vs BBC'), html.Img(src='/assets/Inglaterra y bbc.png', style={'width': '100%'})], style={'flex': '1'}),
                html.Div([html.H5('FIFA vs JioCinema'), html.Img(src='/assets/Fifa y Jiocinema.png', style={'width': '100%'})], style={'flex': '1'}),
                html.Div([html.H5('Satelite Elon Musk'), html.Img(src='/assets/Elon musk.png', style={'width': '100%'})], style={'flex': '1'}),
            ])
        ]),

        # 11. Analisis de Palabras Clave
        card([
            seccion_titulo('4.6 Analisis Interactivos de Palabras por Comunidad'),
            html.Div(style={'width': '300px', 'margin': '0 auto'}, children=[
                dcc.Dropdown(
                    id='dropdown-comunidad',
                    options=[{'label': f"Comunidad {c}", 'value': c} for c in df_palabras['Comunidad'].unique()],
                    value='FIFA', clearable=False
                )
            ]),
            dcc.Graph(id='grafico-palabras')
        ]),

        # 12. Influencers y Cross-Analysis
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '24px'}, children=[
            html.Div([dcc.Graph(figure=fig_cross)], style={**ESTILO_CARD, 'flex': '1'}),
            html.Div(style={**ESTILO_CARD, 'flex': '1'}, children=[
                html.H3('Top Influencers (Metricas de Centralidad)', style={'textAlign': 'center'}),
                dash_table.DataTable(
                    data=df_top_table.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_top_table.columns],
                    style_header={'backgroundColor': '#2C3E50', 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'center'}
                )
            ]),
        ]),

        # 13. Conclusiones y Explorador
        card([
            seccion_titulo('5. Conclusiones y Reflexión Final'), 
            dcc.Markdown(TEXTO_CONCLUSIONES)
        ]),

        # 14. Explorador de Tuits Originales (La tabla)
        card([
            seccion_titulo('6. Explorador de Tuits Originales'),
            html.Div(style={'width': '200px', 'marginBottom': '10px'}, children=[
                dcc.Dropdown(id='filter-sentiment', options=[{'label': i, 'value': i.lower()} for i in ['All', 'Positive', 'Neutral', 'Negative']], value='all')
            ]),
            dash_table.DataTable(
                id='tweets-table',
                columns=[{"name": "Fecha", "id": "Fecha_Completa"}, {"name": "Tuit", "id": "Tweet_Limpio"}, {"name": "Sentimiento", "id": "Sentiment"}, {"name": "Likes", "id": "Number of Likes"}],
                page_size=10,
                style_cell={'textAlign': 'left', 'padding': '10px', 'whiteSpace': 'normal', 'height': 'auto'},
                style_header={'backgroundColor': '#2C3E50', 'color': 'white'}
            )
        ]),

        html.Footer('Modelos Predictivos III | Proyecto Final | Qatar 2022', style={'textAlign': 'center', 'padding': '20px', 'color': '#7F8C8D'})
    ]
)

# =================================================================
# 6. CALLBACKS
# =================================================================

@app.callback(
    Output('grafico-palabras', 'figure'),
    Input('dropdown-comunidad', 'value')
)
def update_word_graph(com):
    df_f = df_palabras[df_palabras['Comunidad'] == com]
    fig = px.bar(
        df_f, x='Palabra', y='Peso', color='Sentimiento',
        color_discrete_map=COLORES, text='Peso'
    )
    fig.update_layout(plot_bgcolor='white', title=f'Polaridad de Palabras: {com}')
    return fig

@app.callback(
    Output('tweets-table', 'data'),
    Input('filter-sentiment', 'value')
)
def update_table(sentiment):
    dff = df_limpios.copy()
    if sentiment != 'all':
        dff = dff[dff['Sentiment'] == sentiment]
    return dff.sort_values(by='Number of Likes', ascending=False).head(50).to_dict('records')

if __name__ == '__main__':
    app.run(debug=True, port=8055)