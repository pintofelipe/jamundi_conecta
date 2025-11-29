"""
Visualizaciones Avanzadas para el Panel Lateral
Gráficos adicionales para análisis detallado de zonas
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ============================================================================
# GRÁFICOS PARA EL PANEL LATERAL
# ============================================================================

def crear_grafico_evolucion_zona(zona_nombre, df_conectividad):
    """
    Crea un gráfico de evolución temporal de accesos para una zona específica
    (Simulado ya que no tenemos datos por zona en el dataset)
    
    Args:
        zona_nombre: Nombre de la zona
        df_conectividad: DataFrame con datos de conectividad
    
    Returns:
        Figura de Plotly
    """
    # Simular datos de evolución (en producción, filtrar por zona)
    df_evol = df_conectividad.groupby(['anno', 'trimestre'])['accesos'].sum().reset_index()
    df_evol = df_evol.sort_values(['anno', 'trimestre'])
    df_evol['periodo'] = df_evol['anno'].astype(str) + '-T' + df_evol['trimestre'].astype(str)
    
    # Tomar últimos 8 trimestres
    df_evol = df_evol.tail(8)
    
    # Simular variación para la zona específica (±20% del promedio)
    np.random.seed(hash(zona_nombre) % 1000)
    factor = 1 + (np.random.random(len(df_evol)) - 0.5) * 0.4
    df_evol['accesos_zona'] = (df_evol['accesos'] * factor / 100).astype(int)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_evol['periodo'],
        y=df_evol['accesos_zona'],
        mode='lines+markers',
        name='Accesos',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))
    
    fig.update_layout(
        title=dict(text='Evolución de Accesos (últimos 8 trimestres)', font=dict(size=11)),
        xaxis_title='',
        yaxis_title='Accesos',
        height=200,
        margin=dict(l=40, r=10, t=40, b=30),
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

def crear_grafico_comparacion_zonas_similares(zona_data, df_zonas):
    """
    Compara la zona seleccionada con zonas similares (mismo tipo)
    
    Args:
        zona_data: Datos de la zona seleccionada
        df_zonas: DataFrame con todas las zonas
    
    Returns:
        Figura de Plotly
    """
    # Filtrar zonas del mismo tipo
    zonas_similares = df_zonas[df_zonas['tipo'] == zona_data['tipo']].copy()
    
    # Tomar top 5 por ranking
    zonas_similares = zonas_similares.nsmallest(5, 'ranking')
    
    # Resaltar la zona seleccionada
    zonas_similares['color'] = zonas_similares['zona'].apply(
        lambda x: '#1f77b4' if x == zona_data['zona'] else '#cccccc'
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=zonas_similares['zona'],
        y=zonas_similares['puntaje_prioridad'],
        marker=dict(color=zonas_similares['color']),
        text=zonas_similares['puntaje_prioridad'].round(3),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Puntaje: %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'Comparación con Zonas {zona_data["tipo"]}s', font=dict(size=11)),
        xaxis_title='',
        yaxis_title='Puntaje de Prioridad',
        height=220,
        margin=dict(l=40, r=10, t=40, b=60),
        showlegend=False,
        xaxis=dict(tickangle=-45)
    )
    
    return fig

def crear_grafico_distribucion_tecnologias_zona(zona_nombre, df_conectividad):
    """
    Muestra la distribución de tecnologías en la zona
    (Simulado ya que no tenemos datos por zona)
    
    Args:
        zona_nombre: Nombre de la zona
        df_conectividad: DataFrame con datos de conectividad
    
    Returns:
        Figura de Plotly
    """
    # Obtener distribución general de tecnologías
    df_tech = df_conectividad.groupby('tecnologia')['accesos'].sum().reset_index()
    df_tech = df_tech.nlargest(6, 'accesos')
    
    # Simular variación para la zona
    np.random.seed(hash(zona_nombre) % 1000)
    df_tech['accesos_zona'] = (df_tech['accesos'] * (0.5 + np.random.random(len(df_tech))) / 100).astype(int)
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=df_tech['tecnologia'],
        values=df_tech['accesos_zona'],
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Accesos: %{value:,}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='Distribución de Tecnologías', font=dict(size=11)),
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False
    )
    
    return fig

def crear_grafico_radar_metricas(zona_data, df_zonas):
    """
    Crea un gráfico de radar comparando métricas de la zona con promedios
    
    Args:
        zona_data: Datos de la zona seleccionada
        df_zonas: DataFrame con todas las zonas
    
    Returns:
        Figura de Plotly
    """
    # Calcular promedios
    promedios = {
        'Velocidad': df_zonas['velocidad_promedio_mbps'].mean(),
        'Penetración': df_zonas['penetracion_internet'].mean() * 100,
        'Densidad': df_zonas['densidad_poblacion'].mean(),
        'Población': df_zonas['poblacion'].mean()
    }
    
    # Normalizar valores de la zona (0-100)
    valores_zona = {
        'Velocidad': min(zona_data['velocidad_promedio_mbps'] / promedios['Velocidad'] * 50, 100),
        'Penetración': zona_data['penetracion_internet'] * 100,
        'Densidad': min(zona_data['densidad_poblacion'] / promedios['Densidad'] * 50, 100),
        'Población': min(zona_data['poblacion'] / promedios['Población'] * 50, 100)
    }
    
    categorias = list(valores_zona.keys())
    valores = list(valores_zona.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name=zona_data['zona'],
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    # Añadir línea de promedio (50)
    fig.add_trace(go.Scatterpolar(
        r=[50, 50, 50, 50],
        theta=categorias,
        fill=None,
        name='Promedio',
        line=dict(color='red', width=1, dash='dash'),
        showlegend=True
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title=dict(text='Radar de Métricas', font=dict(size=11)),
        height=280,
        margin=dict(l=40, r=40, t=40, b=20),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def crear_mini_mapa_ubicacion(zona_data):
    """
    Crea un mini mapa mostrando solo la ubicación de la zona seleccionada
    
    Args:
        zona_data: Datos de la zona seleccionada
    
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    # Color según prioridad
    if zona_data['nivel_prioridad'] == 'Alta':
        color = '#d62728'
        size = 20
    elif zona_data['nivel_prioridad'] == 'Media':
        color = '#ff7f0e'
        size = 18
    else:
        color = '#2ca02c'
        size = 16
    
    fig.add_trace(go.Scattermapbox(
        lat=[zona_data['latitud']],
        lon=[zona_data['longitud']],
        mode='markers',
        marker=dict(
            size=size,
            color=color,
            opacity=0.8
        ),
        text=zona_data['zona'],
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=zona_data['latitud'], lon=zona_data['longitud']),
            zoom=11
        ),
        height=200,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False
    )
    
    return fig

def crear_grafico_barras_componentes_detallado(zona_data):
    """
    Versión mejorada del gráfico de componentes con más detalles
    
    Args:
        zona_data: Datos de la zona seleccionada
    
    Returns:
        Figura de Plotly
    """
    componentes_data = {
        'Componente': ['Educación\n(50%)', 'Población\n(20%)', 'Conectividad\n(30%)'],
        'Valor': [
            zona_data['componente_educacion'],
            zona_data['componente_poblacion'],
            zona_data['componente_conectividad']
        ],
        'Peso': [0.5, 0.2, 0.3],
        'Contribucion': [
            zona_data['componente_educacion'] * 0.5,
            zona_data['componente_poblacion'] * 0.2,
            zona_data['componente_conectividad'] * 0.3
        ]
    }
    df_comp = pd.DataFrame(componentes_data)
    
    fig = go.Figure()
    
    # Barras de valor
    fig.add_trace(go.Bar(
        x=df_comp['Componente'],
        y=df_comp['Valor'],
        name='Valor Normalizado',
        marker=dict(
            color=df_comp['Valor'],
            colorscale='RdYlGn_r',
            showscale=False
        ),
        text=df_comp['Valor'].round(3),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Valor: %{y:.3f}<extra></extra>'
    ))
    
    # Línea de contribución
    fig.add_trace(go.Scatter(
        x=df_comp['Componente'],
        y=df_comp['Contribucion'],
        name='Contribución al Puntaje',
        mode='lines+markers',
        line=dict(color='blue', width=2, dash='dash'),
        marker=dict(size=10, symbol='diamond'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Contribución: %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='Componentes del Puntaje (Detallado)', font=dict(size=11)),
        xaxis_title='',
        yaxis_title='Valor Normalizado',
        yaxis2=dict(
            title='Contribución',
            overlaying='y',
            side='right',
            range=[0, max(df_comp['Contribucion']) * 1.2]
        ),
        height=250,
        margin=dict(l=40, r=50, t=40, b=60),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            font=dict(size=9)
        ),
        hovermode='x unified'
    )
    
    return fig

def crear_indicador_progreso_meta(zona_data, meta_velocidad=25):
    """
    Crea un indicador de progreso hacia la meta de velocidad
    
    Args:
        zona_data: Datos de la zona seleccionada
        meta_velocidad: Meta de velocidad en Mbps (default: 25)
    
    Returns:
        Figura de Plotly
    """
    velocidad_actual = zona_data['velocidad_promedio_mbps']
    progreso = min((velocidad_actual / meta_velocidad) * 100, 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=velocidad_actual,
        delta={'reference': meta_velocidad, 'relative': False, 'suffix': ' Mbps'},
        title={'text': f"Progreso hacia Meta ({meta_velocidad} Mbps)", 'font': {'size': 11}},
        number={'suffix': ' Mbps'},
        gauge={
            'axis': {'range': [None, meta_velocidad * 1.2]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, meta_velocidad * 0.3], 'color': "#ffcccc"},
                {'range': [meta_velocidad * 0.3, meta_velocidad * 0.7], 'color': "#ffffcc"},
                {'range': [meta_velocidad * 0.7, meta_velocidad], 'color': "#ccffcc"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': meta_velocidad
            }
        }
    ))
    
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig
