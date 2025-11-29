# 🌐 Dashboard Jamundí Conectada V3

**Sistema Inteligente de Priorización de Infraestructura Digital (SIPID)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

---

## 📊 Descripción

Dashboard interactivo para analizar y priorizar las necesidades de conectividad a internet en los corregimientos de Jamundí, Valle del Cauca, Colombia. Utiliza datos oficiales de MinTIC y la Alcaldía de Jamundí para tomar decisiones informadas sobre inversión en infraestructura digital.

---

## ✨ Características

- 🗺️ **Mapa Interactivo:** Visualización geográfica de puntos de prioridad por corregimiento
- 📊 **7 Gráficos Avanzados:** Análisis profundo de cada zona (evolución, comparación, tecnologías, radar, etc.)
- 🔍 **Búsqueda Inteligente:** Encuentra zonas específicas con autocompletado
- 📱 **Diseño Responsive:** Optimizado para desktop, tablet y móvil
- 💾 **Exportación a PDF:** Genera reportes profesionales de cada zona
- 🔔 **Sistema de Alertas:** Identifica problemas críticos automáticamente
- 📈 **Análisis de Datos:** Ranking de prioridades basado en educación, población y conectividad

---

## 🎯 Objetivos del Proyecto

1. **Equidad Digital Territorial:** Garantizar acceso equitativo a internet en zonas urbanas y rurales
2. **Priorización Inteligente:** Usar datos para identificar las zonas más críticas
3. **Transparencia:** Proporcionar información pública y verificable
4. **Toma de Decisiones:** Apoyar a la Alcaldía en la planificación de inversiones

---

## 🚀 Instalación Local

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/TU_USUARIO/jamundi-conectada.git
cd jamundi-conectada
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el dashboard:**
```bash
streamlit run app_v3.py
```

4. **Abrir en el navegador:**
El dashboard se abrirá automáticamente en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
jamundi-conectada/
│
├── app_v3.py                          # Aplicación principal de Streamlit
├── data_processing.py                 # Procesamiento y consolidación de datos
├── ranking.py                         # Sistema de priorización
├── visualizations.py                  # Visualizaciones básicas
├── visualizations_advanced.py         # Visualizaciones avanzadas
├── utils.py                           # Utilidades (PDF, alertas, búsqueda)
├── corregimientos_jamundi.geojson     # Datos geográficos de corregimientos
├── requirements.txt                   # Dependencias de Python
└── README.md                          # Este archivo
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.11+ | Lenguaje de programación |
| **Streamlit** | 1.28.0+ | Framework web interactivo |
| **Pandas** | 2.0.0+ | Manipulación de datos |
| **Plotly** | 5.17.0+ | Gráficos interactivos |
| **GeoPandas** | 0.14.0+ | Datos geoespaciales |
| **FPDF2** | 2.7.0+ | Generación de PDFs |

---

## 📊 Fuentes de Datos

**© 2025 | Datos oficiales de:**
- **MinTIC Colombia** - Ministerio de Tecnologías de la Información y las Comunicaciones
- **Alcaldía de Jamundí** - Gobierno Municipal

Ver la pestaña "📄 Información del Proyecto" en el dashboard para las 29 referencias bibliográficas completas.

---

## 🎓 Cómo Usar el Dashboard

### Guía Rápida (5 minutos)

1. **Filtra:** Usa la barra lateral para seleccionar zonas y niveles de prioridad
2. **Analiza:** Explora el mapa interactivo y selecciona un corregimiento
3. **Profundiza:** Navega por los 7 gráficos del panel lateral
4. **Actúa:** Revisa alertas y exporta reportes en PDF

### Documentación Completa

Consulta los tutoriales incluidos en el repositorio:
- `TUTORIAL_COMPLETO_DASHBOARD.md` - Guía paso a paso completa
- `GUIA_RAPIDA_VISUAL.md` - Referencia rápida
- `PREGUNTAS_FRECUENTES_FAQ.md` - Preguntas frecuentes
- `SOLUCION_PROBLEMAS.md` - Solución de problemas comunes
- `GLOSARIO_TERMINOS.md` - Definiciones de términos técnicos

---

## 🤝 Contribuciones

Este es un proyecto de código abierto. Las contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **Desarrollador Principal:** Manus AI
- **Cliente:** Alcaldía de Jamundí
- **Concurso:** Open Data Jamundí 2025

---

## 📞 Contacto y Soporte

- **Repositorio:** [GitHub](https://github.com/TU_USUARIO/jamundi-conectada)
- **Issues:** [GitHub Issues](https://github.com/TU_USUARIO/jamundi-conectada/issues)
- **Documentación:** Ver archivos `TUTORIAL_*.md` en el repositorio

---

## 🏆 Reconocimientos

- **MinTIC Colombia** por proporcionar datos abiertos de conectividad
- **Alcaldía de Jamundí** por el apoyo al proyecto
- **Comunidad de Streamlit** por la plataforma
- **Comunidad Open Data** por promover la transparencia

---

## 📈 Roadmap

### Versión Actual (V3)
- ✅ Mapa interactivo con puntos de prioridad
- ✅ 7 gráficos avanzados en panel lateral
- ✅ Búsqueda con autocompletado
- ✅ Exportación a PDF
- ✅ Sistema de alertas
- ✅ Diseño responsive

### Futuras Versiones
- 🔄 Integración con API de la Alcaldía (datos en tiempo real)
- 🔄 Predicciones con Machine Learning
- 🔄 Módulo de planificación de inversiones
- 🔄 App móvil nativa
- 🔄 Notificaciones por email

---

## 🌟 ¡Dale una Estrella!

Si este proyecto te resulta útil, ¡considera darle una estrella ⭐ en GitHub!

---

**Dashboard Jamundí Conectada V3**  
*Datos abiertos + Análisis inteligente = Decisiones informadas* 🌐
