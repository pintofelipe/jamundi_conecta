"""
Módulo de visualizaciones para el proyecto Jamundí Conectada
Genera mapas y gráficos interactivos con Plotly
Autor: Sistema de Análisis de Datos
Fecha: 2025
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

# Configuración de colores del tema
COLOR_ALTA_PRIORIDAD = '#d62728'  # Rojo
COLOR_MEDIA_PRIORIDAD = '#ff7f0e'  # Naranja
COLOR_BAJA_PRIORIDAD = '#2ca02c'  # Verde
COLOR_URBANO = '#1f77b4'  # Azul
COLOR_RURAL = '#8c564b'  # Marrón


def crear_mapa_prioridades(df_zonas: pd.DataFrame) -> go.Figure:
    """
    Crea un mapa de calor geoespacial con el puntaje de prioridad de cada zona
    
    Args:
        df_zonas: DataFrame con datos de zonas incluyendo latitud, longitud y puntaje_prioridad
        
    Returns:
        Figura de Plotly con el mapa
    """
    # Crear mapa de dispersión con tamaño según población
    fig = px.scatter_mapbox(
        df_zonas,
        lat='latitud',
        lon='longitud',
        size='poblacion',
        color='puntaje_prioridad',
        hover_name='zona',
        hover_data={
            'tipo': True,
            'poblacion': ':,',
            'velocidad_promedio_mbps': ':.2f',
            'puntaje_prioridad': ':.3f',
            'nivel_prioridad': True,
            'ranking': True,
            'latitud': False,
            'longitud': False
        },
        color_continuous_scale='RdYlGn_r',  # Rojo (alto) a Verde (bajo) invertido
        size_max=50,
        zoom=10,
        title='Mapa de Prioridades de Intervención - Jamundí',
        labels={
            'puntaje_prioridad': 'Puntaje de Prioridad',
            'poblacion': 'Población',
            'velocidad_promedio_mbps': 'Velocidad Promedio (Mbps)',
            'nivel_prioridad': 'Nivel de Prioridad',
            'ranking': 'Ranking'
        }
    )
    
    # Configurar el mapa base
    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox=dict(
            center=dict(lat=3.28, lon=-76.58),
            zoom=10
        ),
        height=600,
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    
    return fig


def crear_mapa_velocidades(df_zonas: pd.DataFrame) -> go.Figure:
    """
    Crea un mapa geográfico mostrando la velocidad promedio de conexión por zona
    
    Args:
        df_zonas: DataFrame con datos de zonas
        
    Returns:
        Figura de Plotly con el mapa de velocidades
    """
    fig = px.scatter_mapbox(
        df_zonas,
        lat='latitud',
        lon='longitud',
        size='poblacion',
        color='velocidad_promedio_mbps',
        hover_name='zona',
        hover_data={
            'tipo': True,
            'poblacion': ':,',
            'velocidad_promedio_mbps': ':.2f',
            'penetracion_internet': ':.1%',
            'latitud': False,
            'longitud': False
        },
        color_continuous_scale='Viridis',
        size_max=50,
        zoom=10,
        title='Mapa de Velocidades de Conexión - Jamundí',
        labels={
            'velocidad_promedio_mbps': 'Velocidad (Mbps)',
            'poblacion': 'Población',
            'penetracion_internet': 'Penetración Internet'
        }
    )
    
    fig.update_layout(
        mapbox_style='open-street-map',
        mapbox=dict(
            center=dict(lat=3.28, lon=-76.58),
            zoom=10
        ),
        height=600,
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    
    return fig


def crear_grafico_dispersion_vulnerabilidad(df_zonas: pd.DataFrame) -> go.Figure:
    """
    Crea un gráfico de dispersión relacionando densidad de población vs velocidad de conexión
    
    Args:
        df_zonas: DataFrame con datos de zonas
        
    Returns:
        Figura de Plotly con el gráfico de dispersión
    """
    # Calcular densidad si no existe
    if 'densidad_poblacion' not in df_zonas.columns:
        df_zonas['densidad_poblacion'] = df_zonas['poblacion'] / 10  # Valor estimado
    
    fig = px.scatter(
        df_zonas,
        x='densidad_poblacion',
        y='velocidad_promedio_mbps',
        size='poblacion',
        color='nivel_prioridad',
        hover_name='zona',
        hover_data={
            'tipo': True,
            'poblacion': ':,',
            'puntaje_prioridad': ':.3f',
            'densidad_poblacion': ':.2f'
        },
        color_discrete_map={
            'Alta': COLOR_ALTA_PRIORIDAD,
            'Media': COLOR_MEDIA_PRIORIDAD,
            'Baja': COLOR_BAJA_PRIORIDAD
        },
        title='Zonas Vulnerables: Densidad Poblacional vs Velocidad de Conexión',
        labels={
            'densidad_poblacion': 'Densidad de Población (hab/km²)',
            'velocidad_promedio_mbps': 'Velocidad Promedio (Mbps)',
            'nivel_prioridad': 'Nivel de Prioridad'
        }
    )
    
    # Añadir líneas de referencia
    fig.add_hline(
        y=10, 
        line_dash="dash", 
        line_color="red",
        annotation_text="Umbral mínimo (10 Mbps)",
        annotation_position="right"
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        xaxis_title='Densidad de Población (hab/km²)',
        yaxis_title='Velocidad Promedio (Mbps)'
    )
    
    return fig


def crear_grafico_barras_tecnologias(df_conectividad: pd.DataFrame) -> go.Figure:
    """
    Crea un gráfico de barras mostrando la distribución de accesos por tecnología
    
    Args:
        df_conectividad: DataFrame con datos de conectividad
        
    Returns:
        Figura de Plotly con el gráfico de barras
    """
    # Agrupar por tecnología
    df_tech = df_conectividad.groupby('tecnologia')['accesos'].sum().reset_index()
    df_tech = df_tech.sort_values('accesos', ascending=False)
    
    fig = px.bar(
        df_tech,
        x='tecnologia',
        y='accesos',
        title='Distribución de Accesos por Tecnología',
        labels={
            'tecnologia': 'Tecnología',
            'accesos': 'Número de Accesos'
        },
        color='accesos',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def crear_grafico_evolucion_temporal(df_conectividad: pd.DataFrame) -> go.Figure:
    """
    Crea un gráfico de líneas mostrando la evolución temporal de accesos
    
    Args:
        df_conectividad: DataFrame con datos de conectividad
        
    Returns:
        Figura de Plotly con el gráfico de evolución
    """
    # Crear columna de periodo
    df_temp = df_conectividad.copy()
    df_temp['periodo'] = df_temp['anno'].astype(str) + '-Q' + df_temp['trimestre'].astype(str)
    
    # Agrupar por periodo
    df_evol = df_temp.groupby('periodo')['accesos'].sum().reset_index()
    
    fig = px.line(
        df_evol,
        x='periodo',
        y='accesos',
        title='Evolución Temporal de Accesos a Internet',
        labels={
            'periodo': 'Periodo',
            'accesos': 'Número de Accesos'
        },
        markers=True
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


def crear_grafico_proveedores(df_conectividad: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Crea un gráfico de barras horizontales con los principales proveedores
    
    Args:
        df_conectividad: DataFrame con datos de conectividad
        top_n: Número de proveedores a mostrar
        
    Returns:
        Figura de Plotly con el gráfico
    """
    # Agrupar por proveedor
    df_prov = df_conectividad.groupby('proveedor')['accesos'].sum().reset_index()
    df_prov = df_prov.sort_values('accesos', ascending=False).head(top_n)
    
    fig = px.bar(
        df_prov,
        y='proveedor',
        x='accesos',
        orientation='h',
        title=f'Top {top_n} Proveedores de Internet en Jamundí',
        labels={
            'proveedor': 'Proveedor',
            'accesos': 'Número de Accesos'
        },
        color='accesos',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig


def crear_grafico_segmentos(df_conectividad: pd.DataFrame) -> go.Figure:
    """
    Crea un gráfico de torta mostrando la distribución por segmentos
    
    Args:
        df_conectividad: DataFrame con datos de conectividad
        
    Returns:
        Figura de Plotly con el gráfico de torta
    """
    # Agrupar por segmento
    df_seg = df_conectividad.groupby('segmento')['accesos'].sum().reset_index()
    
    fig = px.pie(
        df_seg,
        values='accesos',
        names='segmento',
        title='Distribución de Accesos por Segmento de Mercado',
        hole=0.4  # Donut chart
    )
    
    fig.update_layout(
        height=400
    )
    
    return fig


def crear_indicadores_kpi(df_zonas: pd.DataFrame, df_conectividad: pd.DataFrame) -> Dict[str, any]:
    """
    Calcula indicadores clave de rendimiento (KPIs) para el dashboard
    
    Args:
        df_zonas: DataFrame con datos de zonas
        df_conectividad: DataFrame con datos de conectividad
        
    Returns:
        Diccionario con KPIs
    """
    kpis = {
        'poblacion_total': int(df_zonas['poblacion'].sum()),
        'zonas_totales': len(df_zonas),
        'zonas_alta_prioridad': len(df_zonas[df_zonas['nivel_prioridad'] == 'Alta']),
        'sedes_sin_conexion': len(df_zonas[
            (df_zonas['tiene_sede_educativa'] == True) & 
            (df_zonas['sede_con_conexion'] == False)
        ]),
        'velocidad_promedio': float(df_zonas['velocidad_promedio_mbps'].mean()),
        'penetracion_promedio': float(df_zonas['penetracion_internet'].mean()),
        'total_accesos': int(df_conectividad['accesos'].sum()),
        'num_proveedores': int(df_conectividad['proveedor'].nunique()),
        'num_tecnologias': int(df_conectividad['tecnologia'].nunique())
    }
    
    return kpis


if __name__ == "__main__":
    # Prueba del módulo
    from data_processing import consolidar_datos_jamundi, crear_datos_zonas_simulados
    from ranking import calcular_puntaje_prioridad
    
    print("="*80)
    print("PRUEBA DEL MÓDULO DE VISUALIZACIONES")
    print("="*80)
    
    # Cargar datos
    print("\n📂 Cargando datos...")
    df_conectividad = consolidar_datos_jamundi()
    df_zonas = crear_datos_zonas_simulados()
    df_zonas_ranked = calcular_puntaje_prioridad(df_zonas)
    
    # Calcular KPIs
    print("\n📊 Calculando KPIs...")
    kpis = crear_indicadores_kpi(df_zonas_ranked, df_conectividad)
    
    print("\n📈 INDICADORES CLAVE:")
    for key, value in kpis.items():
        print(f"   {key}: {value}")
    
    # Crear visualizaciones (sin mostrar, solo verificar que se crean)
    print("\n🎨 Creando visualizaciones...")
    
    fig1 = crear_mapa_prioridades(df_zonas_ranked)
    print("   ✅ Mapa de prioridades creado")
    
    fig2 = crear_mapa_velocidades(df_zonas_ranked)
    print("   ✅ Mapa de velocidades creado")
    
    fig3 = crear_grafico_dispersion_vulnerabilidad(df_zonas_ranked)
    print("   ✅ Gráfico de vulnerabilidad creado")
    
    fig4 = crear_grafico_barras_tecnologias(df_conectividad)
    print("   ✅ Gráfico de tecnologías creado")
    
    fig5 = crear_grafico_evolucion_temporal(df_conectividad)
    print("   ✅ Gráfico de evolución temporal creado")
    
    fig6 = crear_grafico_proveedores(df_conectividad)
    print("   ✅ Gráfico de proveedores creado")
    
    fig7 = crear_grafico_segmentos(df_conectividad)
    print("   ✅ Gráfico de segmentos creado")
    
    print("\n✅ Módulo de visualizaciones funcionando correctamente")
    print("   Total de visualizaciones creadas: 7")
