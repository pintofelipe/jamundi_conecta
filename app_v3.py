"""
Dashboard Interactivo - Jamundí Conectada V3
Sistema Inteligente de Priorización de Infraestructura Digital (SIPID)
Versión Avanzada con Polígonos, Alertas, Exportación PDF y Más

Autor: Sistema de Análisis de Datos
Fecha: 2025
Tecnologías: Streamlit, Pandas, Plotly, GeoPandas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Importar módulos personalizados
from data_processing import (
    consolidar_datos_jamundi,
    crear_datos_zonas_simulados,
    obtener_estadisticas_generales
)
from ranking import (
    calcular_puntaje_prioridad,
    obtener_top_zonas,
    generar_reporte_ranking,
    crear_tabla_ranking_display
)
from visualizations import (
    crear_grafico_barras_tecnologias,
    crear_grafico_evolucion_temporal,
    crear_grafico_proveedores,
    crear_grafico_segmentos,
    crear_indicadores_kpi
)
from visualizations_advanced import (
    crear_grafico_evolucion_zona,
    crear_grafico_comparacion_zonas_similares,
    crear_grafico_distribucion_tecnologias_zona,
    crear_grafico_radar_metricas,
    crear_mini_mapa_ubicacion,
    crear_grafico_barras_componentes_detallado,
    crear_indicador_progreso_meta
)
from utils import (
    generar_alertas,
    obtener_estadisticas_alertas,
    exportar_zona_a_pdf,
    buscar_zonas,
    obtener_sugerencias,
    cargar_geojson_corregimientos,
    obtener_color_prioridad
)

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Jamundí Conectada - Dashboard V3",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS (MEJORADOS PARA MÓVIL)
# ============================================================================

st.markdown("""
<style>
    /* Estilos generales */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    
    /* Cards y badges */
    .zona-card {
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .priority-badge-alta {
        background-color: #d62728;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .priority-badge-media {
        background-color: #ff7f0e;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .priority-badge-baja {
        background-color: #2ca02c;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    
    /* Alertas */
    .alert-critico {
        background-color: #ffebee;
        border-left: 4px solid #d62728;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .alert-urgente {
        background-color: #fff3e0;
        border-left: 4px solid #ff7f0e;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .alert-advertencia {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    
    /* Diseño responsive para móvil */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
        }
        .sub-header {
            font-size: 1rem;
        }
        .zona-card {
            padding: 10px;
        }
        /* Hacer que las columnas se apilen en móvil */
        .stColumns {
            flex-direction: column !important;
        }
    }
    
    /* Mejorar botones en móvil */
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARGA DE DATOS (CON CACHÉ)
# ============================================================================

@st.cache_data
def cargar_todos_los_datos():
    """Carga todos los datos necesarios para el dashboard"""
    df_conectividad = consolidar_datos_jamundi()
    df_zonas = crear_datos_zonas_simulados()
    df_zonas_ranked = calcular_puntaje_prioridad(df_zonas)
    
    # Cargar GeoJSON
    geojson_data = cargar_geojson_corregimientos('/home/ubuntu/jamundi_conectada/corregimientos_jamundi.geojson')
    
    return df_conectividad, df_zonas_ranked, geojson_data

# Cargar datos
with st.spinner('Cargando datos del proyecto Jamundí Conectada...'):
    df_conectividad, df_zonas_ranked, geojson_data = cargar_todos_los_datos()

# ============================================================================
# ESTADO DE LA SESIÓN
# ============================================================================

if 'zona_seleccionada' not in st.session_state:
    st.session_state.zona_seleccionada = None

if 'mostrar_panel_alertas' not in st.session_state:
    st.session_state.mostrar_panel_alertas = False

# ============================================================================
# ENCABEZADO PRINCIPAL
# ============================================================================

col_titulo, col_alertas = st.columns([4, 1])

with col_titulo:
    st.markdown('<div class="main-header">🌐 Jamundí Conectada V3</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sistema Inteligente de Priorización de Infraestructura Digital (SIPID)</div>', unsafe_allow_html=True)

with col_alertas:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔔 Ver Alertas", use_container_width=True):
        st.session_state.mostrar_panel_alertas = not st.session_state.mostrar_panel_alertas

# ============================================================================
# BARRA LATERAL - FILTROS Y BÚSQUEDA
# ============================================================================

st.sidebar.title("🎛️ Panel de Control")
st.sidebar.markdown("---")

# ============================================================================
# BÚSQUEDA CON AUTOCOMPLETADO
# ============================================================================

st.sidebar.subheader("🔍 Búsqueda Rápida")
query_busqueda = st.sidebar.text_input(
    "Buscar zona/corregimiento:",
    placeholder="Ej: Potrerito, San Antonio...",
    help="Escribe para buscar zonas"
)

if query_busqueda:
    sugerencias = obtener_sugerencias(query_busqueda, df_zonas_ranked, max_sugerencias=5)
    if sugerencias:
        st.sidebar.info(f"📍 **Sugerencias:** {', '.join(sugerencias)}")
        zona_sugerida = st.sidebar.selectbox("Seleccionar de sugerencias:", sugerencias)
        if st.sidebar.button("Ir a esta zona"):
            st.session_state.zona_seleccionada = zona_sugerida
    else:
        st.sidebar.warning("No se encontraron zonas que coincidan")

st.sidebar.markdown("---")

# ============================================================================
# FILTRO 1: ZONAS/CORREGIMIENTOS (CON CHECKBOXES)
# ============================================================================

with st.sidebar.expander("📍 Filtrar por Zonas/Corregimientos", expanded=True):
    st.markdown("**Selecciona las zonas a visualizar:**")
    
    # Opción de seleccionar/deseleccionar todas
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Todas", use_container_width=True, key="btn_todas"):
            st.session_state.zonas_seleccionadas = df_zonas_ranked['zona'].tolist()
            st.rerun()
    with col2:
        if st.button("❌ Ninguna", use_container_width=True, key="btn_ninguna"):
            st.session_state.zonas_seleccionadas = []
            st.rerun()
    
    st.markdown("---")
    
    # Inicializar estado si no existe
    if 'zonas_seleccionadas' not in st.session_state:
        st.session_state.zonas_seleccionadas = df_zonas_ranked['zona'].tolist()
    
    # Crear checkboxes para cada zona
    zonas_temp = []
    for zona in sorted(df_zonas_ranked['zona'].unique()):
        zona_info = df_zonas_ranked[df_zonas_ranked['zona'] == zona].iloc[0]
        nivel = zona_info['nivel_prioridad']
        
        # Icono según nivel de prioridad
        if nivel == 'Alta':
            icono = "🔴"
        elif nivel == 'Media':
            icono = "🟠"
        else:
            icono = "🟢"
        
        checkbox_value = st.checkbox(
            f"{icono} {zona}",
            value=zona in st.session_state.zonas_seleccionadas,
            key=f"zona_v3_{zona}"
        )
        
        if checkbox_value:
            zonas_temp.append(zona)
    
    st.session_state.zonas_seleccionadas = zonas_temp

# ============================================================================
# FILTRO 2: NIVEL DE PRIORIDAD (CON CHECKBOXES)
# ============================================================================

with st.sidebar.expander("🎯 Filtrar por Nivel de Prioridad", expanded=True):
    st.markdown("**Selecciona los niveles a visualizar:**")
    
    # Inicializar estado si no existe
    if 'niveles_seleccionados' not in st.session_state:
        st.session_state.niveles_seleccionados = ['Alta', 'Media', 'Baja']
    
    niveles_temp = []
    
    nivel_alta = st.checkbox(
        "🔴 Alta Prioridad",
        value='Alta' in st.session_state.niveles_seleccionados,
        key="nivel_alta_v3"
    )
    if nivel_alta:
        niveles_temp.append('Alta')
    
    nivel_media = st.checkbox(
        "🟠 Media Prioridad",
        value='Media' in st.session_state.niveles_seleccionados,
        key="nivel_media_v3"
    )
    if nivel_media:
        niveles_temp.append('Media')
    
    nivel_baja = st.checkbox(
        "🟢 Baja Prioridad",
        value='Baja' in st.session_state.niveles_seleccionados,
        key="nivel_baja_v3"
    )
    if nivel_baja:
        niveles_temp.append('Baja')
    
    st.session_state.niveles_seleccionados = niveles_temp

st.sidebar.markdown("---")

# Información de filtros aplicados
st.sidebar.info(f"""
**Filtros Activos:**
- Zonas: {len(st.session_state.zonas_seleccionadas)} de {len(df_zonas_ranked)}
- Niveles: {len(st.session_state.niveles_seleccionados)} de 3
""")

# ============================================================================
# APLICAR FILTROS A LOS DATOS
# ============================================================================

# Filtrar zonas según selección
df_zonas_filtrado = df_zonas_ranked[
    (df_zonas_ranked['zona'].isin(st.session_state.zonas_seleccionadas)) &
    (df_zonas_ranked['nivel_prioridad'].isin(st.session_state.niveles_seleccionados))
].copy()

# Generar alertas
alertas = generar_alertas(df_zonas_filtrado)
stats_alertas = obtener_estadisticas_alertas(alertas)

# Recalcular KPIs con datos filtrados
if len(df_zonas_filtrado) > 0:
    kpis = crear_indicadores_kpi(df_zonas_filtrado, df_conectividad)
else:
    kpis = {
        'poblacion_total': 0,
        'zonas_totales': 0,
        'zonas_alta_prioridad': 0,
        'sedes_sin_conexion': 0,
        'velocidad_promedio': 0,
        'penetracion_promedio': 0,
        'total_accesos': 0,
        'num_proveedores': 0,
        'num_tecnologias': 0
    }

# ============================================================================
# PANEL DE ALERTAS (OPCIONAL)
# ============================================================================

if st.session_state.mostrar_panel_alertas:
    st.markdown("### 🔔 Panel de Alertas Activas")
    
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
        st.metric("Total Alertas", stats_alertas['total'])
    with col_stats2:
        st.metric("Críticas", stats_alertas['criticas'], delta="Urgente", delta_color="inverse")
    with col_stats3:
        st.metric("Urgentes", stats_alertas['urgentes'])
    with col_stats4:
        st.metric("Advertencias", stats_alertas['advertencias'])
    
    if alertas:
        for alerta in alertas[:10]:  # Mostrar solo las primeras 10
            clase_css = f"alert-{alerta['tipo'].lower()}"
            st.markdown(f"""
            <div class="{clase_css}">
                <strong>{alerta['icono']} {alerta['tipo']}</strong> - {alerta['zona']}<br>
                {alerta['mensaje']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No hay alertas activas en este momento")
    
    st.markdown("---")

# ============================================================================
# INDICADORES CLAVE (KPIs)
# ============================================================================

st.markdown("### 📊 Indicadores Clave")

if len(df_zonas_filtrado) > 0:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(
            label="👥 Población",
            value=f"{kpis['poblacion_total']:,}",
            help="Población total de las zonas seleccionadas"
        )
    
    with col2:
        st.metric(
            label="🎯 Alta Prioridad",
            value=kpis['zonas_alta_prioridad'],
            delta=f"{len(df_zonas_filtrado)} totales",
            help="Zonas que requieren intervención urgente"
        )
    
    with col3:
        st.metric(
            label="🏫 Sin Conexión",
            value=kpis['sedes_sin_conexion'],
            delta="Crítico" if kpis['sedes_sin_conexion'] > 5 else "Moderado",
            delta_color="inverse",
            help="Instituciones educativas sin acceso"
        )
    
    with col4:
        st.metric(
            label="⚡ Velocidad",
            value=f"{kpis['velocidad_promedio']:.1f} Mbps",
            help="Velocidad promedio de conexión"
        )
    
    with col5:
        st.metric(
            label="📡 Penetración",
            value=f"{kpis['penetracion_promedio']*100:.1f}%",
            help="Porcentaje de penetración de internet"
        )
    
    with col6:
        st.metric(
            label="🔔 Alertas",
            value=stats_alertas['total'],
            delta=f"{stats_alertas['criticas']} críticas",
            delta_color="inverse" if stats_alertas['criticas'] > 0 else "off",
            help="Total de alertas activas"
        )
else:
    st.warning("⚠️ No hay zonas seleccionadas. Por favor, activa al menos un filtro.")

st.markdown("---")

# ============================================================================
# PESTAÑAS PRINCIPALES
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Mapa Interactivo",
    "📈 Análisis Detallado",
    "📄 Información del Proyecto",
    "🔍 Explorador de Datos"
])

# ============================================================================
# PESTAÑA 1: MAPA INTERACTIVO CON PANEL LATERAL EXPANDIDO
# ============================================================================

with tab1:
    if len(df_zonas_filtrado) > 0:
        st.header("🗺️ Mapa Interactivo de Prioridades")
        
        # Crear dos columnas: mapa (65%) y panel lateral (35%)
        col_mapa, col_panel = st.columns([65, 35])
        
        with col_mapa:
            st.subheader("Mapa con Polígonos de Corregimientos")
            
            # Crear mapa con Plotly
            fig_mapa = go.Figure()
            
            # Polígonos desactivados - Solo mostrar puntos geográficos
            # (Los datos de GeoJSON se mantienen para uso futuro)
            
            # Añadir puntos de calor por zona
            for idx, row in df_zonas_filtrado.iterrows():
                # Color según nivel de prioridad
                if row['nivel_prioridad'] == 'Alta':
                    color = '#d62728'
                    size = 25
                elif row['nivel_prioridad'] == 'Media':
                    color = '#ff7f0e'
                    size = 20
                else:
                    color = '#2ca02c'
                    size = 15
                
                # Añadir marcador
                fig_mapa.add_trace(go.Scattermapbox(
                    lat=[row['latitud']],
                    lon=[row['longitud']],
                    mode='markers',
                    marker=dict(
                        size=size,
                        color=color,
                        opacity=0.8
                    ),
                    text=row['zona'],
                    name=row['zona'],
                    customdata=[[
                        row['zona'],
                        row['poblacion'],
                        row['velocidad_promedio_mbps'],
                        row['puntaje_prioridad'],
                        row['nivel_prioridad'],
                        row['ranking']
                    ]],
                    hovertemplate="<b>%{customdata[0]}</b><br>" +
                                  "Población: %{customdata[1]:,}<br>" +
                                  "Velocidad: %{customdata[2]:.2f} Mbps<br>" +
                                  "Puntaje: %{customdata[3]:.3f}<br>" +
                                  "Nivel: %{customdata[4]}<br>" +
                                  "Ranking: #%{customdata[5]}<br>" +
                                  "<extra></extra>",
                    showlegend=False
                ))
            
            # Configurar el mapa
            fig_mapa.update_layout(
                mapbox=dict(
                    style='open-street-map',
                    center=dict(lat=3.28, lon=-76.58),
                    zoom=10
                ),
                height=600,
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                showlegend=False,
                hovermode='closest'
            )
            
            # Mostrar mapa
            st.plotly_chart(fig_mapa, use_container_width=True, key="mapa_principal_v3")
            
            # Selector manual de zona
            st.markdown("**Selecciona un corregimiento para ver detalles:**")
            zona_seleccionada_manual = st.selectbox(
                "Zona:",
                options=df_zonas_filtrado['zona'].tolist(),
                index=0,
                key="selector_zona_manual_v3"
            )
            
            if zona_seleccionada_manual:
                st.session_state.zona_seleccionada = zona_seleccionada_manual
        
        with col_panel:
            st.subheader("📊 Panel de Información Detallada")
            
            if st.session_state.zona_seleccionada:
                zona_data = df_zonas_filtrado[
                    df_zonas_filtrado['zona'] == st.session_state.zona_seleccionada
                ].iloc[0]
                
                # Título de la zona con botón de exportación
                nivel = zona_data['nivel_prioridad']
                if nivel == 'Alta':
                    badge_class = "priority-badge-alta"
                elif nivel == 'Media':
                    badge_class = "priority-badge-media"
                else:
                    badge_class = "priority-badge-baja"
                
                st.markdown(f"""
                <div class="zona-card">
                    <h3>{zona_data['zona']}</h3>
                    <span class="{badge_class}">{nivel}</span>
                    <p style="margin-top: 10px; color: #666;">Ranking: #{int(zona_data['ranking'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón de exportación a PDF
                if st.button("📥 Exportar a PDF", use_container_width=True, key="btn_exportar_pdf"):
                    ruta_pdf = f"/home/ubuntu/reporte_{zona_data['zona'].replace(' ', '_')}.pdf"
                    if exportar_zona_a_pdf(zona_data, ruta_pdf):
                        with open(ruta_pdf, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Descargar PDF",
                                data=pdf_file,
                                file_name=f"reporte_{zona_data['zona'].replace(' ', '_')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        st.success("✅ PDF generado correctamente")
                    else:
                        st.error("❌ Error al generar PDF")
                
                st.markdown("---")
                
                # Métricas principales
                st.markdown("### 📈 Métricas Principales")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("👥 Población", f"{int(zona_data['poblacion']):,}")
                    st.metric("⚡ Velocidad", f"{zona_data['velocidad_promedio_mbps']:.1f} Mbps")
                with col2:
                    st.metric("🎯 Puntaje", f"{zona_data['puntaje_prioridad']:.3f}")
                    st.metric("📡 Penetración", f"{zona_data['penetracion_internet']*100:.1f}%")
                
                st.markdown("---")
                
                # Tabs para organizar gráficos
                tab_graficos = st.tabs(["📊 Componentes", "📈 Evolución", "🎯 Comparación", "🔧 Tecnologías", "📡 Radar", "🎯 Meta"])
                
                with tab_graficos[0]:
                    fig_comp = crear_grafico_barras_componentes_detallado(zona_data)
                    st.plotly_chart(fig_comp, use_container_width=True)
                
                with tab_graficos[1]:
                    fig_evol = crear_grafico_evolucion_zona(zona_data['zona'], df_conectividad)
                    st.plotly_chart(fig_evol, use_container_width=True)
                
                with tab_graficos[2]:
                    fig_comp_zonas = crear_grafico_comparacion_zonas_similares(zona_data, df_zonas_filtrado)
                    st.plotly_chart(fig_comp_zonas, use_container_width=True)
                
                with tab_graficos[3]:
                    fig_tech = crear_grafico_distribucion_tecnologias_zona(zona_data['zona'], df_conectividad)
                    st.plotly_chart(fig_tech, use_container_width=True)
                
                with tab_graficos[4]:
                    fig_radar = crear_grafico_radar_metricas(zona_data, df_zonas_filtrado)
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                with tab_graficos[5]:
                    fig_meta = crear_indicador_progreso_meta(zona_data, meta_velocidad=25)
                    st.plotly_chart(fig_meta, use_container_width=True)
                
                st.markdown("---")
                
                # Información adicional
                st.markdown("### ℹ️ Información Adicional")
                
                st.info(f"""
                **Tipo:** {zona_data['tipo']}  
                **Sede Educativa:** {'Sí' if zona_data['tiene_sede_educativa'] else 'No'}  
                **Sede Conectada:** {'Sí' if zona_data['sede_con_conexion'] else 'No'}  
                **Densidad:** {zona_data['densidad_poblacion']:.2f} hab/km²
                """)
                
            else:
                st.info("👆 Selecciona un corregimiento en el mapa o en el selector para ver información detallada.")
    else:
        st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")

# ============================================================================
# PESTAÑA 2: ANÁLISIS DETALLADO
# ============================================================================

with tab2:
    st.header("📈 Análisis Detallado de Conectividad")
    
    if len(df_zonas_filtrado) > 0:
        # Tabla de ranking
        st.subheader("🏆 Ranking de Zonas Priorizadas")
        df_display = crear_tabla_ranking_display(df_zonas_filtrado, len(df_zonas_filtrado))
        st.dataframe(df_display, use_container_width=True, height=400, hide_index=True)
        
        st.markdown("---")
        
        # Gráficos en columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Distribución por Tecnología")
            fig_tech = crear_grafico_barras_tecnologias(df_conectividad)
            st.plotly_chart(fig_tech, use_container_width=True)
        
        with col2:
            st.subheader("👥 Distribución por Segmento")
            fig_seg = crear_grafico_segmentos(df_conectividad)
            st.plotly_chart(fig_seg, use_container_width=True)
        
        st.markdown("---")
        
        # Evolución temporal
        st.subheader("📅 Evolución Temporal de Accesos")
        fig_evol = crear_grafico_evolucion_temporal(df_conectividad)
        st.plotly_chart(fig_evol, use_container_width=True)
        
        # Proveedores
        st.subheader("🏢 Principales Proveedores")
        fig_prov = crear_grafico_proveedores(df_conectividad, top_n=10)
        st.plotly_chart(fig_prov, use_container_width=True)
    else:
        st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")

# ============================================================================
# PESTAÑA 3: INFORMACIÓN DEL PROYECTO
# ============================================================================

with tab3:
    st.header("📄 Información del Proyecto Jamundí Conectada")
    
    st.markdown("""
    ## 🎯 Objetivos del Proyecto
    
    El proyecto **"Jamundí Conectada"** busca cerrar la brecha digital en el municipio mediante 
    un enfoque estratégico basado en datos y priorización inteligente de recursos.
    
    ### 🌟 Objetivos Estratégicos
    
    1. **Equidad Digital Territorial**
       - Garantizar acceso equitativo a internet en zonas urbanas y rurales
       - Priorizar zonas con instituciones educativas sin conexión
       - Reducir la brecha digital entre estratos socioeconómicos
    
    2. **Infraestructura Resiliente**
       - Implementar tecnologías apropiadas según características geográficas
       - Desarrollar redes híbridas (fibra óptica, microondas, satelital)
       - Asegurar sostenibilidad y escalabilidad de la infraestructura
    
    3. **Inteligencia de Datos**
       - Utilizar análisis de datos para toma de decisiones informadas
       - Monitorear indicadores clave de conectividad
       - Evaluar impacto de intervenciones en tiempo real
    """)
    
    st.success("""
    ### 📈 Metas del Proyecto
    
    - ✅ Conectar 100% de instituciones educativas rurales
    - ✅ Aumentar penetración en Estrato 1 de 29% a 50%
    - ✅ Reducir brecha digital urbano-rural en 40%
    - ✅ Implementar 20 puntos de acceso público en zonas rurales
    - ✅ Beneficiar directamente a 40,000 personas en zonas rurales
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📊 Fuentes de Datos
    
    **© 2025 | Datos oficiales de:**
    - **MinTIC Colombia** - Ministerio de Tecnologías de la Información y las Comunicaciones
    - **Alcaldía de Jamundí** - Gobierno Municipal
    
    ### 📚 Referencias Bibliográficas
    
    1. Alcaldía de Cali. (2022, 7 de julio). Plan de expansión de fibra óptica de Emcali dejará en este gobierno 200 mil hogares conectados. [https://www.cali.gov.co/gobierno/publicaciones/170000/](https://www.cali.gov.co/gobierno/publicaciones/170000/)
    
    2. Alcaldía Municipal de Jamundí. (2017, 19 de julio). PUNTOS VIVE DIGITAL POR TODO EL MUNICIPIO. [https://jamundi.gov.co/NuestraAlcaldia/SaladePrensa/Paginas/PUNTOS-VIVE-DIGITAL-POR-TODO-EL-MUNICIPIO-.aspx](https://jamundi.gov.co/NuestraAlcaldia/SaladePrensa/Paginas/PUNTOS-VIVE-DIGITAL-POR-TODO-EL-MUNICIPIO-.aspx)
    
    3. Celsia. (2019, 2 de agosto). No más filas, Disfruta de nuestros puntos digitales en Valle del Cauca. [https://www.celsia.com/es/blog-celsia/no-mas-filas-disfruta-de-nuestros-puntos-digitales-en-valle-del-cauca/](https://www.celsia.com/es/blog-celsia/no-mas-filas-disfruta-de-nuestros-puntos-digitales-en-valle-del-cauca/)
    
    4. Celsia. (2023, 17 de mayo). Celsia no es solo energía: ya lleva internet a 50 mil clientes en Valle del Cauca y Tolima. [https://www.celsia.com/es/noticias/celsia-no-es-solo-energia-ya-lleva-internet-a-50-mil-clientes-en-valle-del-cauca-y-tolima/](https://www.celsia.com/es/noticias/celsia-no-es-solo-energia-ya-lleva-internet-a-50-mil-clientes-en-valle-del-cauca-y-tolima/)
    
    5. Celsia. (2023, 18 de julio). Celsia y Directv se unen para ofrecer combos de internet y entretenimiento a bajo costo. [https://www.celsia.com/es/noticias/celsia-y-directv-se-unen-para-ofrecer-combos-de-internet-y-entretenimiento-a-bajo-costo/](https://www.celsia.com/es/noticias/celsia-y-directv-se-unen-para-ofrecer-combos-de-internet-y-entretenimiento-a-bajo-costo/)
    
    6. Celsia Internet. (s.f.). Planes internet fibra óptica: Palmira, Jamundí, Tuluá, Buga. [https://celsiainternet.com/nuevos-planes/](https://celsiainternet.com/nuevos-planes/)
    
    7. Celsia Internet. (s.f.). TESTIMONIAL CELSIA INTERNET JAMUNDÍ. [Video]. YouTube. [https://www.youtube.com/shorts/fC7yTeGOMEU](https://www.youtube.com/shorts/fC7yTeGOMEU)
    
    8. Claro Colombia. (s.f.). Internet hogar & planes Fibra Óptica. [https://www.claro.com.co/personas/servicios/servicios-hogar/internet/](https://www.claro.com.co/personas/servicios/servicios-hogar/internet/)
    
    9. Claro Planes. (s.f.). Planes Tripleplay Claro Hogar. [https://claroplanes.com.co/tripleplay-jamundi-tv-internet-hogar/](https://claroplanes.com.co/tripleplay-jamundi-tv-internet-hogar/)
    
    10. Comparaíso. (2024, 8 de octubre). Internet EMCALI: planes, precios y beneficios. [https://comparaiso.com.co/internet-hogar/fibra/emcali](https://comparaiso.com.co/internet-hogar/fibra/emcali)
    
    11. CSIDELVALLE - Expertos Valle del Cauca. (s.f.). Configuración de Redes en Jamundí. [https://www.csidelvalle.com/configuracion-redes.html](https://www.csidelvalle.com/configuracion-redes.html)
    
    12. Emcali. (2020, 5 de octubre). LA FIBRA ÓPTICA DE EMCALI ES LA MEJOR OPCIÓN DE CONECTIVIDAD A INTERNET EN EL SUR DE CALI. [https://www.emcali.com.co/w/la-fibra-optica-de-emcali-es-la-mejor-opcion-de-conectividad-a-internet-en-el-sur-de-cali](https://www.emcali.com.co/w/la-fibra-optica-de-emcali-es-la-mejor-opcion-de-conectividad-a-internet-en-el-sur-de-cali)
    
    13. Emcali. (2023, 6 de octubre). Red de fibra óptica de Emcali se expande con calidad. [https://www.emcali.com.co/w/red-de-fibra-optica-de-emcali-se-expande-con-calidad](https://www.emcali.com.co/w/red-de-fibra-optica-de-emcali-se-expande-con-calidad)
    
    14. Instabridge. (s.f.). Jamundí, Colombia. Free-wifi. [https://instabridge.com/free-wifi/Colombia-CO/Jamund%C3%AD-3680387/](https://instabridge.com/free-wifi/Colombia-CO/Jamund%C3%AD-3680387/)
    
    15. Instabridge. (s.f.). Parque Municipal Jamundí. Free-wifi. [https://instabridge.com/gratis-wifi/Colombia-CO/Jamund%C3%AD-3680387/4891053/hotspot/](https://instabridge.com/gratis-wifi/Colombia-CO/Jamund%C3%AD-3680387/4891053/hotspot/)
    
    16. Ministerio de Tecnologías de la Información y las Comunicaciones (MinTIC). (2014, 21 de diciembre). Viceministra TIC inaugura Kiosco Vive Digital en Jamundí (Valle). [https://mintic.gov.co/portal/715/w3-article-8070.html](https://mintic.gov.co/portal/715/w3-article-8070.html)
    
    17. nPerf.com. (s.f.). Cobertura 3G / 4G / 5G Movistar Movil en Jamundi, Sur, Valle del Cauca, Colombia. [https://www.nperf.com/es/map/CO/3680387.Jamundi/7239.Movistar-Movil/signal](https://www.nperf.com/es/map/CO/3680387.Jamundi/7239.Movistar-Movil/signal)
    
    18. nPerf.com. (s.f.). Mapa de cobertura 3G / 4G / 5G en Jamundi, Sur, Valle del Cauca, Colombia. [https://www.nperf.com/es/map/CO/3680387.Jamundi/-/signal](https://www.nperf.com/es/map/CO/3680387.Jamundi/-/signal)
    
    19. Noticias Caracol. (s.f.). La respuesta de Epsa y constructora por fallas en fluido eléctrico de urbanización en Jamundí. [Video]. YouTube. [https://www.youtube.com/watch?v=CtAOkDrklGw](https://www.youtube.com/watch?v=CtAOkDrklGw)
    
    20. Ookla. (2025, octubre). Colombia's Mobile and Broadband Internet Speeds. Speedtest Global Index. [https://www.speedtest.net/global-index/colombia](https://www.speedtest.net/global-index/colombia)
    
    21. Promociones Tigo Hogar. (s.f.). Promociones TIGO Hogar | Internet y TV al mejor precio. [https://promocionestigohogar.com.co/](https://promocionestigohogar.com.co/)
    
    22. Rodas Torres, E. (2025, 16 de mayo). Planes Hogar Emcali: internet y planes dúo con telefonía. Selectra. [https://selectra.com.co/empresas/emcali/hogar](https://selectra.com.co/empresas/emcali/hogar)
    
    23. Selectra. (2025, 25 de noviembre). EMCALI, ¿Qué tal es? Opiniones de clientes en Noviembre 2025. [https://selectra.com.co/opiniones/emcali](https://selectra.com.co/opiniones/emcali)
    
    24. Tigo. (s.f.). Internet Tigo Hogar | TIGO®. [https://internethogares.co/](https://internethogares.co/)
    
    25. Tigo. (s.f.). Mapa de cobertura fibra óptica y móvil 5G Tigo | Tu mejor opción. [https://www.tigo.com.co/mapas-de-cobertura](https://www.tigo.com.co/mapas-de-cobertura)
    
    26. Tigo. (s.f.). Planes prepago Tigo con minutos ilimitados | Tu mejor opción. [https://www.tigo.com.co/prepago](https://www.tigo.com.co/prepago)
    
    27. Waze. (s.f.). Información de tráfico en tiempo real para llegar a Punto Vive Digital Ciro Velazco, Cra. 13a, calle 17, Jamundí. [https://www.waze.com/es/live-map/directions/co/valle-del-cauca/jamundi/punto-vive-digital-ciro-velazco?to=place.ChIJqUSLseefMI4RCnxA5SUogQ8](https://www.waze.com/es/live-map/directions/co/valle-del-cauca/jamundi/punto-vive-digital-ciro-velazco?to=place.ChIJqUSLseefMI4RCnxA5SUogQ8)
    
    28. WIFIMAX TELECOMUNICACIONES SAS. (2024). Planes. [https://wifimax.com.co/planes/](https://wifimax.com.co/planes/)
    
    29. WISP TELECOMUNICACIONES S.A.S. (s.f.). Jamundí. [https://wisptelecomunicaciones.com/jamundi/](https://wisptelecomunicaciones.com/jamundi/)
    """)

# ============================================================================
# PESTAÑA 4: EXPLORADOR DE DATOS
# ============================================================================

with tab4:
    st.header("🔍 Explorador de Datos")
    
    if len(df_zonas_filtrado) > 0:
        st.subheader("🗺️ Datos de Zonas Filtradas")
        
        df_display_zonas = df_zonas_filtrado[[
            'ranking', 'zona', 'tipo', 'poblacion', 'velocidad_promedio_mbps',
            'penetracion_internet', 'tiene_sede_educativa', 'sede_con_conexion',
            'puntaje_prioridad', 'nivel_prioridad'
        ]].copy()
        
        df_display_zonas.columns = [
            'Ranking', 'Zona', 'Tipo', 'Población', 'Velocidad (Mbps)',
            'Penetración', 'Tiene Sede', 'Sede Conectada', 'Puntaje', 'Nivel'
        ]
        
        st.dataframe(df_display_zonas, use_container_width=True, height=400)
        
        # Estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Zonas", len(df_display_zonas))
        with col2:
            st.metric("Población Total", f"{df_zonas_filtrado['poblacion'].sum():,}")
        with col3:
            st.metric("Velocidad Promedio", f"{df_zonas_filtrado['velocidad_promedio_mbps'].mean():.2f} Mbps")
        
        # Botón de descarga
        csv_zonas = df_display_zonas.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Datos Filtrados (CSV)",
            data=csv_zonas,
            file_name=f"jamundi_zonas_filtradas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No hay datos para mostrar con los filtros seleccionados.")

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Dashboard Jamundí Conectada V3</strong> | Sistema Inteligente de Priorización de Infraestructura Digital (SIPID)</p>
    <p>Desarrollado con ❤️ usando Streamlit, Pandas, Plotly y GeoPandas</p>

</div>
""", unsafe_allow_html=True)
