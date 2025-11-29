"""
Módulo de cálculo de ranking de prioridad para el proyecto Jamundí Conectada
Implementa la lógica de negocio central del sistema de priorización
Autor: Sistema de Análisis de Datos
Fecha: 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

# Pesos del sistema de ranking (priorizando educación)
PESO_EDUCACION = 0.5
PESO_POBLACION = 0.2
PESO_CONECTIVIDAD = 0.3


def normalizar_valores(serie: pd.Series) -> pd.Series:
    """
    Normaliza una serie de valores a escala 0-1
    
    Args:
        serie: Serie de pandas con valores numéricos
        
    Returns:
        Serie normalizada entre 0 y 1
    """
    min_val = serie.min()
    max_val = serie.max()
    
    if max_val == min_val:
        return pd.Series([0.5] * len(serie), index=serie.index)
    
    return (serie - min_val) / (max_val - min_val)


def calcular_bono_educativo(tiene_sede: bool, sede_con_conexion: bool) -> float:
    """
    Calcula el bono educativo para una zona
    
    Args:
        tiene_sede: Si la zona tiene sede educativa
        sede_con_conexion: Si la sede tiene conexión a internet
        
    Returns:
        Bono educativo (1 si tiene sede sin conexión, 0 en caso contrario)
    """
    if tiene_sede and not sede_con_conexion:
        return 1.0
    return 0.0


def calcular_puntaje_prioridad(df_zonas: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el Puntaje de Prioridad (PP) para cada zona según la fórmula:
    PP = (Peso_Educación * Bono_Educativo) + 
         (Peso_Población * Población_Normalizada) + 
         (Peso_Conectividad * Conectividad_Inversa_Normalizada)
    
    Args:
        df_zonas: DataFrame con datos de zonas que debe incluir:
                 - poblacion: Población de la zona
                 - tiene_sede_educativa: Si tiene sede educativa
                 - sede_con_conexion: Si la sede tiene conexión
                 - velocidad_promedio_mbps: Velocidad promedio de conexión
    
    Returns:
        DataFrame con columnas adicionales de scoring
    """
    df = df_zonas.copy()
    
    # 1. Calcular Bono Educativo
    df['bono_educativo'] = df.apply(
        lambda row: calcular_bono_educativo(
            row['tiene_sede_educativa'], 
            row['sede_con_conexion']
        ), 
        axis=1
    )
    
    # 2. Normalizar Población (mayor población = mayor puntaje)
    df['poblacion_normalizada'] = normalizar_valores(df['poblacion'])
    
    # 3. Normalizar Conectividad de forma INVERSA (menor velocidad = mayor puntaje)
    # Primero invertimos los valores
    velocidad_invertida = df['velocidad_promedio_mbps'].max() - df['velocidad_promedio_mbps']
    df['conectividad_inversa_normalizada'] = normalizar_valores(velocidad_invertida)
    
    # 4. Calcular componentes ponderados
    df['componente_educacion'] = PESO_EDUCACION * df['bono_educativo']
    df['componente_poblacion'] = PESO_POBLACION * df['poblacion_normalizada']
    df['componente_conectividad'] = PESO_CONECTIVIDAD * df['conectividad_inversa_normalizada']
    
    # 5. Calcular Puntaje de Prioridad Total
    df['puntaje_prioridad'] = (
        df['componente_educacion'] + 
        df['componente_poblacion'] + 
        df['componente_conectividad']
    )
    
    # 6. Crear ranking (1 = mayor prioridad)
    df['ranking'] = df['puntaje_prioridad'].rank(ascending=False, method='min').astype(int)
    
    # 7. Clasificar nivel de prioridad
    df['nivel_prioridad'] = pd.cut(
        df['puntaje_prioridad'],
        bins=[0, 0.3, 0.6, 1.0],
        labels=['Baja', 'Media', 'Alta'],
        include_lowest=True
    )
    
    return df


def obtener_top_zonas(df_zonas_ranked: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Obtiene las N zonas con mayor prioridad
    
    Args:
        df_zonas_ranked: DataFrame con zonas y puntajes calculados
        n: Número de zonas a retornar
        
    Returns:
        DataFrame con las top N zonas ordenadas por prioridad
    """
    return df_zonas_ranked.nsmallest(n, 'ranking')


def generar_reporte_ranking(df_zonas_ranked: pd.DataFrame) -> Dict:
    """
    Genera un reporte resumen del ranking de zonas
    
    Args:
        df_zonas_ranked: DataFrame con zonas y puntajes calculados
        
    Returns:
        Diccionario con estadísticas del ranking
    """
    reporte = {
        'total_zonas': len(df_zonas_ranked),
        'zonas_prioridad_alta': len(df_zonas_ranked[df_zonas_ranked['nivel_prioridad'] == 'Alta']),
        'zonas_prioridad_media': len(df_zonas_ranked[df_zonas_ranked['nivel_prioridad'] == 'Media']),
        'zonas_prioridad_baja': len(df_zonas_ranked[df_zonas_ranked['nivel_prioridad'] == 'Baja']),
        'zonas_con_sedes_sin_conexion': len(df_zonas_ranked[df_zonas_ranked['bono_educativo'] == 1.0]),
        'puntaje_promedio': float(df_zonas_ranked['puntaje_prioridad'].mean()),
        'puntaje_maximo': float(df_zonas_ranked['puntaje_prioridad'].max()),
        'puntaje_minimo': float(df_zonas_ranked['puntaje_prioridad'].min()),
        'zona_maxima_prioridad': df_zonas_ranked.loc[df_zonas_ranked['puntaje_prioridad'].idxmax(), 'zona']
    }
    
    return reporte


def crear_tabla_ranking_display(df_zonas_ranked: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Crea una tabla formateada para visualización del ranking
    
    Args:
        df_zonas_ranked: DataFrame con zonas y puntajes calculados
        top_n: Número de zonas a incluir
        
    Returns:
        DataFrame formateado para display
    """
    df_top = obtener_top_zonas(df_zonas_ranked, top_n)
    
    df_display = df_top[[
        'ranking', 'zona', 'tipo', 'poblacion', 
        'velocidad_promedio_mbps', 'puntaje_prioridad',
        'componente_educacion', 'componente_poblacion', 'componente_conectividad',
        'nivel_prioridad'
    ]].copy()
    
    # Renombrar columnas para mejor visualización
    df_display.columns = [
        'Ranking', 'Zona', 'Tipo', 'Población',
        'Velocidad (Mbps)', 'Puntaje Total',
        'Comp. Educación', 'Comp. Población', 'Comp. Conectividad',
        'Nivel Prioridad'
    ]
    
    # Redondear valores numéricos
    df_display['Puntaje Total'] = df_display['Puntaje Total'].round(3)
    df_display['Comp. Educación'] = df_display['Comp. Educación'].round(3)
    df_display['Comp. Población'] = df_display['Comp. Población'].round(3)
    df_display['Comp. Conectividad'] = df_display['Comp. Conectividad'].round(3)
    df_display['Velocidad (Mbps)'] = df_display['Velocidad (Mbps)'].round(2)
    
    return df_display


if __name__ == "__main__":
    # Prueba del módulo
    from data_processing import crear_datos_zonas_simulados
    
    print("="*80)
    print("PRUEBA DEL MÓDULO DE RANKING DE PRIORIDAD")
    print("="*80)
    
    # Cargar datos de zonas
    df_zonas = crear_datos_zonas_simulados()
    
    print("\n📊 DATOS DE ENTRADA:")
    print(df_zonas[['zona', 'poblacion', 'tiene_sede_educativa', 
                    'sede_con_conexion', 'velocidad_promedio_mbps']].head(10))
    
    # Calcular puntajes de prioridad
    print("\n🔢 Calculando puntajes de prioridad...")
    df_ranked = calcular_puntaje_prioridad(df_zonas)
    
    # Generar reporte
    reporte = generar_reporte_ranking(df_ranked)
    
    print("\n📈 REPORTE DE RANKING:")
    for key, value in reporte.items():
        print(f"   {key}: {value}")
    
    # Mostrar top 10
    print("\n🏆 TOP 10 ZONAS PRIORITARIAS:")
    df_display = crear_tabla_ranking_display(df_ranked, 10)
    print(df_display.to_string(index=False))
    
    print("\n✅ Módulo de ranking funcionando correctamente")
    print(f"\n💡 Pesos utilizados:")
    print(f"   - Educación: {PESO_EDUCACION} (50%)")
    print(f"   - Población: {PESO_POBLACION} (20%)")
    print(f"   - Conectividad: {PESO_CONECTIVIDAD} (30%)")
