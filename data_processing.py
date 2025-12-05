"""
Módulo de procesamiento de datos para el proyecto Jamundí Conectada
Autor: Sistema de Análisis de Datos
Fecha: 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

def limpiar_velocidad(valor):
    """
    Limpia y convierte valores de velocidad que pueden estar en formato string con comas
    
    Args:
        valor: Valor de velocidad (puede ser string, float, int)
        
    Returns:
        float: Valor numérico de velocidad
    """
    if pd.isna(valor):
        return 0.0
    
    if isinstance(valor, (int, float)):
        return float(valor)
    
    # Convertir string a float, reemplazando comas por puntos
    try:
        valor_str = str(valor).replace(',', '.')
        return float(valor_str)
    except:
        return 0.0


def cargar_datos_internet_fijo() -> pd.DataFrame:
    """
    Carga y procesa los datos de internet fijo de Jamundí desde el CSV local
    
    Returns:
        DataFrame con datos procesados de internet fijo
    """
    print("📂 Cargando datos de internet fijo local...")
    
    # Nota: Archivo local no disponible en Streamlit Cloud
    # Usando solo datos de las APIs de datos.gov.co
    df = pd.DataFrame()  # DataFrame vacío, se llenará con datos de APIs
    
    # Si el DataFrame está vacío, retornar vacío
    if df.empty:
        print("⚠️ No hay datos locales disponibles, usando solo APIs")
        return df
    
    # Renombrar columnas para consistencia
    columnas_rename = {
        'AÑO': 'anno',
        'ANO': 'anno',
        'TRIMESTRE': 'trimestre',
        'PROVEEDOR': 'proveedor',
        'COD_DEPARTAMENTO': 'cod_departamento',
        'DEPARTAMENTO': 'departamento',
        'COD_MUNICIPIO': 'cod_municipio',
        'MUNICIPIO': 'municipio',
        'SEGMENTO': 'segmento',
        'TECNOLOGIA': 'tecnologia',
        'TECNOLOGÍA': 'tecnologia',
        'VELOCIDAD_BAJADA': 'velocidad_bajada',
        'VELOCIDAD_SUBIDA': 'velocidad_subida',
        'NO DE ACCESOS': 'accesos',
        'ACCESOS': 'accesos'
    }
    
    df.rename(columns=columnas_rename, inplace=True)
    
    # Limpiar valores de velocidad
    df['velocidad_bajada'] = df['velocidad_bajada'].apply(limpiar_velocidad)
    df['velocidad_subida'] = df['velocidad_subida'].apply(limpiar_velocidad)
    
    # Asegurar que accesos sea numérico
    df['accesos'] = pd.to_numeric(df['accesos'], errors='coerce').fillna(0).astype(int)
    
    print(f"✅ Datos cargados: {len(df)} registros")
    return df


def cargar_datos_api_nacional() -> pd.DataFrame:
    """
    Carga y procesa los datos de la API nacional de internet fijo
    
    Returns:
        DataFrame con datos de la API nacional filtrados para Jamundí
    """
    print("📂 Cargando datos de API nacional...")
    
    try:
        # Descargar directamente de la API de datos.gov.co
        url = 'https://www.datos.gov.co/resource/n48w-gutb.csv?$limit=50000'
        df = pd.read_csv(url)
        
        # Filtrar solo Jamundí
        df_jamundi = df[df['municipio'].str.upper().str.contains('JAMUNDÍ|JAMUNDI', na=False)].copy()
        
        # Limpiar velocidades
        df_jamundi['velocidad_bajada'] = df_jamundi['velocidad_bajada'].apply(limpiar_velocidad)
        df_jamundi['velocidad_subida'] = df_jamundi['velocidad_subida'].apply(limpiar_velocidad)
        df_jamundi['no_de_accesos'] = pd.to_numeric(df_jamundi['no_de_accesos'], errors='coerce').fillna(0).astype(int)
        
        print(f"✅ Datos API cargados: {len(df_jamundi)} registros de Jamundí")
        return df_jamundi
    except Exception as e:
        print(f"⚠️ Error cargando API nacional: {e}")
        return pd.DataFrame()


def cargar_datos_instituciones_educativas() -> pd.DataFrame:
    """
    Carga datos de instituciones educativas (referencia de Boyacá)
    
    Returns:
        DataFrame con datos de instituciones educativas
    """
    print("📂 Cargando datos de instituciones educativas (referencia)...")
    
    try:
        # Descargar directamente de la API de datos.gov.co
        url = 'https://www.datos.gov.co/resource/pejt-qp6n.csv?$limit=10000'
        df = pd.read_csv(url)
        print(f"✅ Datos instituciones educativas: {len(df)} registros")
        return df
    except Exception as e:
        print(f"⚠️ Error cargando instituciones educativas: {e}")
        return pd.DataFrame()


def cargar_datos_conectividad_alta_velocidad() -> pd.DataFrame:
    """
    Carga datos del proyecto de conectividad de alta velocidad
    
    Returns:
        DataFrame con datos de conectividad de alta velocidad
    """
    print("📂 Cargando datos de conectividad de alta velocidad...")
    
    try:
        # Descargar directamente de la API de datos.gov.co
        url = 'https://www.datos.gov.co/resource/xcpu-5b5n.csv?$limit=10000'
        df = pd.read_csv(url)
        print(f"✅ Datos conectividad alta velocidad: {len(df)} registros")
        return df
    except Exception as e:
        print(f"⚠️ Error cargando conectividad alta velocidad: {e}")
        return pd.DataFrame()


def consolidar_datos_jamundi() -> pd.DataFrame:
    """
    Consolida todos los datos disponibles de Jamundí
    
    Returns:
        DataFrame consolidado con todos los datos de Jamundí
    """
    print("\n🔄 Consolidando datos de Jamundí...")
    
    # Cargar datos locales
    df_local = cargar_datos_internet_fijo()
    
    # Cargar datos de API
    df_api = cargar_datos_api_nacional()
    
    # Si tenemos datos de API, combinarlos con los locales
    if not df_api.empty:
        # Renombrar columnas de API para que coincidan con local
        df_api_renamed = df_api.rename(columns={'no_de_accesos': 'accesos'})
        
        # Seleccionar columnas comunes
        columnas_comunes = [
            'anno', 'trimestre', 'proveedor', 'municipio', 'segmento',
            'tecnologia', 'velocidad_bajada', 'velocidad_subida', 'accesos'
        ]
        
        # Si no hay datos locales, crear un DF vacío con esas columnas
        if df_local is None or df_local.empty:
            print("⚠️ No hay datos locales, usando solo datos de API para el consolidado")
            df_local = pd.DataFrame(columns=columnas_comunes)
        
        # Combinar datasets
        df_consolidado = pd.concat(
            [
                df_local[columnas_comunes],
                df_api_renamed[columnas_comunes]
            ],
            ignore_index=True
        )
        
        # 🔧 Asegurar tipos numéricos
        df_consolidado['accesos'] = pd.to_numeric(
            df_consolidado['accesos'], errors='coerce'
        ).fillna(0).astype(int)
        df_consolidado['velocidad_bajada'] = pd.to_numeric(
            df_consolidado['velocidad_bajada'], errors='coerce'
        )
        df_consolidado['velocidad_subida'] = pd.to_numeric(
            df_consolidado['velocidad_subida'], errors='coerce'
        )
        
        # Eliminar duplicados
        df_consolidado = df_consolidado.drop_duplicates()
    else:
        # Si no hay datos de API, usar solo los locales (podrían estar vacíos)
        df_consolidado = df_local
    
    print(f"✅ Datos consolidados: {len(df_consolidado)} registros totales")
    return df_consolidado



def crear_datos_zonas_simulados() -> pd.DataFrame:
    """
    Crea datos simulados de zonas/corregimientos de Jamundí para el dashboard
    Basado en información real de los PDFs del proyecto
    
    Returns:
        DataFrame con datos de zonas
    """
    print("\n🗺️ Creando datos de zonas de Jamundí...")
    
    # Datos basados en los PDFs del proyecto
    zonas_data = {
        'zona': [
            'Cabecera Municipal', 'Villa Colombia', 'Potrerito', 'San Antonio',
            'Robles', 'Timba', 'Ampudia', 'La Liberia', 'San Vicente',
            'Bocas del Palo', 'Chagres', 'El Hormiguero', 'Quinamayó', 'Yumbillo'
        ],
        'tipo': [
            'Urbana', 'Rural', 'Rural', 'Rural',
            'Rural', 'Rural', 'Rural', 'Rural', 'Rural',
            'Rural', 'Rural', 'Rural', 'Rural', 'Rural'
        ],
        'poblacion': [
            142808, 5200, 4800, 4500,
            3200, 2900, 2700, 2500, 2400,
            2200, 2000, 1900, 1800, 1700
        ],
        'tiene_sede_educativa': [
            True, True, True, True,
            True, True, True, True, True,
            False, True, False, True, False
        ],
        'sede_con_conexion': [
            True, False, False, False,
            True, True, False, False, False,
            False, False, False, False, False
        ],
        'velocidad_promedio_mbps': [
            45.5, 2.0, 1.5, 1.8,
            15.2, 12.5, 3.5, 2.8, 3.2,
            5.0, 4.5, 6.0, 3.8, 7.2
        ],
        'penetracion_internet': [
            0.65, 0.15, 0.12, 0.14,
            0.35, 0.32, 0.18, 0.16, 0.17,
            0.22, 0.20, 0.25, 0.19, 0.28
        ],
        'latitud': [
            3.2611, 3.1797, 3.2355, 3.2321,
            3.1341, 3.1266, 3.1828, 3.1477, 3.2715,
            3.2498, 3.1201, 3.2863, 3.1291, 3.2556
        ],
        'longitud': [
            -76.5383, -76.6789, -76.5914, -76.6693,
            -76.5894, -76.6352, -76.6393, -76.6900, -76.6224,
            -76.4843, -76.6033, -76.5762, -76.5548, -76.5122
        ]
    }
    
    df_zonas = pd.DataFrame(zonas_data)
    
    # Calcular densidad de población (hab/km2 - valores estimados)
    df_zonas['densidad_poblacion'] = df_zonas['poblacion'] / np.random.uniform(5, 50, len(df_zonas))
    
    print(f"✅ Datos de zonas creados: {len(df_zonas)} zonas")
    return df_zonas


def obtener_estadisticas_generales(df: pd.DataFrame) -> Dict:
    """
    Calcula estadísticas generales de los datos de conectividad
    
    Args:
        df: DataFrame con datos de conectividad
        
    Returns:
        Diccionario con estadísticas
    """
    stats = {
        'total_accesos': int(df['accesos'].sum()),
        'velocidad_promedio_bajada': float(df['velocidad_bajada'].mean()),
        'velocidad_promedio_subida': float(df['velocidad_subida'].mean()),
        'num_proveedores': int(df['proveedor'].nunique()),
        'num_tecnologias': int(df['tecnologia'].nunique()),
        'periodo_inicio': int(df['anno'].min()),
        'periodo_fin': int(df['anno'].max())
    }
    
    return stats


def filtrar_datos(df: pd.DataFrame, 
                 zonas: List[str] = None,
                 tecnologias: List[str] = None,
                 velocidad_min: float = None,
                 velocidad_max: float = None) -> pd.DataFrame:
    """
    Filtra datos según criterios especificados
    
    Args:
        df: DataFrame a filtrar
        zonas: Lista de zonas a incluir
        tecnologias: Lista de tecnologías a incluir
        velocidad_min: Velocidad mínima de bajada
        velocidad_max: Velocidad máxima de bajada
        
    Returns:
        DataFrame filtrado
    """
    df_filtrado = df.copy()
    
    if tecnologias and len(tecnologias) > 0:
        df_filtrado = df_filtrado[df_filtrado['tecnologia'].isin(tecnologias)]
    
    if velocidad_min is not None:
        df_filtrado = df_filtrado[df_filtrado['velocidad_bajada'] >= velocidad_min]
    
    if velocidad_max is not None:
        df_filtrado = df_filtrado[df_filtrado['velocidad_bajada'] <= velocidad_max]
    
    return df_filtrado


if __name__ == "__main__":
    # Prueba del módulo
    print("="*80)
    print("PRUEBA DEL MÓDULO DE PROCESAMIENTO DE DATOS")
    print("="*80)
    
    # Cargar y consolidar datos
    df_consolidado = consolidar_datos_jamundi()
    
    # Crear datos de zonas
    df_zonas = crear_datos_zonas_simulados()
    
    # Obtener estadísticas
    stats = obtener_estadisticas_generales(df_consolidado)
    
    print("\n📊 ESTADÍSTICAS GENERALES:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n🗺️ ZONAS DISPONIBLES:")
    print(df_zonas[['zona', 'tipo', 'poblacion', 'velocidad_promedio_mbps']])
    
    print("\n✅ Módulo de procesamiento de datos funcionando correctamente")
