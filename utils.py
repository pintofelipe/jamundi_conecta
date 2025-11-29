"""
Módulo de Utilidades para el Dashboard Jamundí Conectada
Incluye funciones para exportación a PDF y sistema de alertas
"""

import pandas as pd
from datetime import datetime
from fpdf import FPDF
import json

# ============================================================================
# SISTEMA DE ALERTAS
# ============================================================================

def generar_alertas(df_zonas):
    """
    Genera alertas para zonas críticas basándose en múltiples criterios
    
    Args:
        df_zonas: DataFrame con información de zonas
    
    Returns:
        Lista de diccionarios con alertas
    """
    alertas = []
    
    for idx, zona in df_zonas.iterrows():
        # Alerta 1: Zona de alta prioridad sin sede educativa conectada
        if zona['nivel_prioridad'] == 'Alta' and zona['tiene_sede_educativa'] and not zona['sede_con_conexion']:
            alertas.append({
                'tipo': 'CRÍTICO',
                'zona': zona['zona'],
                'mensaje': f"Sede educativa sin conexión en zona de alta prioridad",
                'prioridad': 1,
                'icono': '🚨',
                'color': '#d62728'
            })
        
        # Alerta 2: Velocidad muy baja (<3 Mbps)
        if zona['velocidad_promedio_mbps'] < 3:
            alertas.append({
                'tipo': 'URGENTE',
                'zona': zona['zona'],
                'mensaje': f"Velocidad crítica: {zona['velocidad_promedio_mbps']:.1f} Mbps (< 3 Mbps)",
                'prioridad': 2,
                'icono': '⚠️',
                'color': '#ff7f0e'
            })
        
        # Alerta 3: Baja penetración (<20%)
        if zona['penetracion_internet'] < 0.20:
            alertas.append({
                'tipo': 'ADVERTENCIA',
                'zona': zona['zona'],
                'mensaje': f"Penetración muy baja: {zona['penetracion_internet']*100:.1f}%",
                'prioridad': 3,
                'icono': 'ℹ️',
                'color': '#1f77b4'
            })
        
        # Alerta 4: Alta densidad poblacional con baja conectividad
        if zona['densidad_poblacion'] > 1000 and zona['velocidad_promedio_mbps'] < 10:
            alertas.append({
                'tipo': 'ATENCIÓN',
                'zona': zona['zona'],
                'mensaje': f"Alta densidad ({zona['densidad_poblacion']:.0f} hab/km²) con baja velocidad",
                'prioridad': 2,
                'icono': '👥',
                'color': '#ff7f0e'
            })
    
    # Ordenar por prioridad
    alertas_ordenadas = sorted(alertas, key=lambda x: x['prioridad'])
    
    return alertas_ordenadas

def obtener_estadisticas_alertas(alertas):
    """
    Obtiene estadísticas de las alertas generadas
    
    Args:
        alertas: Lista de alertas
    
    Returns:
        Diccionario con estadísticas
    """
    if not alertas:
        return {
            'total': 0,
            'criticas': 0,
            'urgentes': 0,
            'advertencias': 0,
            'atencion': 0
        }
    
    df_alertas = pd.DataFrame(alertas)
    
    return {
        'total': len(alertas),
        'criticas': len(df_alertas[df_alertas['tipo'] == 'CRÍTICO']),
        'urgentes': len(df_alertas[df_alertas['tipo'] == 'URGENTE']),
        'advertencias': len(df_alertas[df_alertas['tipo'] == 'ADVERTENCIA']),
        'atencion': len(df_alertas[df_alertas['tipo'] == 'ATENCIÓN'])
    }

# ============================================================================
# EXPORTACIÓN A PDF
# ============================================================================

class PDFReporte(FPDF):
    """Clase personalizada para generar reportes PDF"""
    
    def header(self):
        """Encabezado del PDF"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Jamundí Conectada - Reporte de Zona', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Pie de página del PDF"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def exportar_zona_a_pdf(zona_data, ruta_salida):
    """
    Exporta la información de una zona a PDF
    
    Args:
        zona_data: Serie de pandas con datos de la zona
        ruta_salida: Ruta donde guardar el PDF
    
    Returns:
        True si se exportó correctamente, False en caso contrario
    """
    try:
        pdf = PDFReporte()
        pdf.add_page()
        
        # Título de la zona
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Corregimiento: {zona_data['zona']}", 0, 1)
        pdf.ln(2)
        
        # Badge de prioridad
        nivel = zona_data['nivel_prioridad']
        if nivel == 'Alta':
            color = (214, 39, 40)
        elif nivel == 'Media':
            color = (255, 127, 14)
        else:
            color = (44, 160, 44)
        
        pdf.set_fill_color(*color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(40, 8, f'  {nivel}  ', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        # Ranking
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 6, f"Ranking: #{int(zona_data['ranking'])}", 0, 1)
        pdf.ln(3)
        
        # Sección: Métricas Principales
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Métricas Principales', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        metricas = [
            ('Población', f"{int(zona_data['poblacion']):,} habitantes"),
            ('Velocidad Promedio', f"{zona_data['velocidad_promedio_mbps']:.2f} Mbps"),
            ('Puntaje de Prioridad', f"{zona_data['puntaje_prioridad']:.3f}"),
            ('Penetración Internet', f"{zona_data['penetracion_internet']*100:.1f}%"),
            ('Densidad Poblacional', f"{zona_data['densidad_poblacion']:.2f} hab/km²")
        ]
        
        for metrica, valor in metricas:
            pdf.cell(80, 6, f"  • {metrica}:", 0, 0)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, valor, 0, 1)
            pdf.set_font('Arial', '', 10)
        
        pdf.ln(5)
        
        # Sección: Componentes del Puntaje
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Componentes del Puntaje de Prioridad', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        componentes = [
            ('Educación (50%)', zona_data['componente_educacion']),
            ('Población (20%)', zona_data['componente_poblacion']),
            ('Conectividad (30%)', zona_data['componente_conectividad'])
        ]
        
        for comp, valor in componentes:
            pdf.cell(80, 6, f"  • {comp}:", 0, 0)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f"{valor:.3f}", 0, 1)
            pdf.set_font('Arial', '', 10)
        
        pdf.ln(5)
        
        # Sección: Información Adicional
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Información Adicional', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        info_adicional = [
            ('Tipo de Zona', zona_data['tipo']),
            ('Tiene Sede Educativa', 'Sí' if zona_data['tiene_sede_educativa'] else 'No'),
            ('Sede Conectada', 'Sí' if zona_data['sede_con_conexion'] else 'No')
        ]
        
        for info, valor in info_adicional:
            pdf.cell(80, 6, f"  • {info}:", 0, 0)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, str(valor), 0, 1)
            pdf.set_font('Arial', '', 10)
        
        pdf.ln(10)
        
        # Pie de página informativo
        pdf.set_font('Arial', 'I', 9)
        pdf.multi_cell(0, 5, 
            'Este reporte fue generado automáticamente por el Sistema Inteligente de Priorización '
            'de Infraestructura Digital (SIPID) del proyecto Jamundí Conectada. '
            'Los datos presentados se basan en información oficial de MinTIC Colombia y la Alcaldía de Jamundí.'
        )
        
        # Guardar PDF
        pdf.output(ruta_salida)
        return True
    
    except Exception as e:
        print(f"Error al exportar PDF: {e}")
        return False

# ============================================================================
# BÚSQUEDA Y AUTOCOMPLETADO
# ============================================================================

def buscar_zonas(query, df_zonas):
    """
    Busca zonas que coincidan con el query
    
    Args:
        query: Texto de búsqueda
        df_zonas: DataFrame con zonas
    
    Returns:
        DataFrame filtrado con zonas que coinciden
    """
    if not query:
        return df_zonas
    
    query_lower = query.lower()
    
    # Buscar en nombre de zona
    mask = df_zonas['zona'].str.lower().str.contains(query_lower, na=False)
    
    return df_zonas[mask]

def obtener_sugerencias(query, df_zonas, max_sugerencias=5):
    """
    Obtiene sugerencias de zonas basadas en el query
    
    Args:
        query: Texto de búsqueda
        df_zonas: DataFrame con zonas
        max_sugerencias: Número máximo de sugerencias
    
    Returns:
        Lista de nombres de zonas sugeridas
    """
    if not query or len(query) < 2:
        return []
    
    resultados = buscar_zonas(query, df_zonas)
    
    if len(resultados) == 0:
        return []
    
    # Ordenar por ranking (prioridad)
    resultados_ordenados = resultados.sort_values('ranking')
    
    return resultados_ordenados['zona'].head(max_sugerencias).tolist()

# ============================================================================
# CARGA DE GEOJSON
# ============================================================================

def cargar_geojson_corregimientos(ruta_geojson):
    """
    Carga el archivo GeoJSON de corregimientos
    
    Args:
        ruta_geojson: Ruta al archivo GeoJSON
    
    Returns:
        Diccionario con datos GeoJSON
    """
    try:
        with open(ruta_geojson, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        return geojson_data
    except Exception as e:
        print(f"Error al cargar GeoJSON: {e}")
        return None

def obtener_color_prioridad(nivel):
    """
    Obtiene el color según el nivel de prioridad
    
    Args:
        nivel: Nivel de prioridad ('Alta', 'Media', 'Baja')
    
    Returns:
        Color en formato hexadecimal
    """
    colores = {
        'Alta': '#d62728',
        'Media': '#ff7f0e',
        'Baja': '#2ca02c'
    }
    return colores.get(nivel, '#999999')
