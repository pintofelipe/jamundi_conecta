# ❓ Preguntas Frecuentes (FAQ) - Dashboard Jamundí Conectada

---

### **1. Sobre el Dashboard**

**P: ¿Qué es el Dashboard Jamundí Conectada?**

**R:** Es una herramienta interactiva que utiliza datos oficiales para analizar y priorizar las necesidades de conectividad a internet en los corregimientos de Jamundí. Su objetivo es ayudar a tomar decisiones informadas para cerrar la brecha digital.

**P: ¿De dónde vienen los datos?**

**R:** Los datos principales provienen del **Ministerio de Tecnologías de la Información y las Comunicaciones (MinTIC)** de Colombia y de la **Alcaldía de Jamundí**. Además, se complementan con 29 fuentes bibliográficas que puedes consultar en la pestaña "📄 Información del Proyecto".

**P: ¿Cada cuánto se actualizan los datos?**

**R:** Esta versión (V3) utiliza los datos más recientes disponibles a noviembre de 2025. El sistema está diseñado para poder actualizarse trimestralmente a medida que MinTIC libera nueva información.

---

### **2. Uso de Funcionalidades**

**P: ¿Por qué el mapa a veces se ve vacío?**

**R:** Esto sucede si tu combinación de filtros no produce ningún resultado. Por ejemplo, si filtras por "Alta Prioridad" y no hay ninguna zona que cumpla ese criterio en tu selección. 

**Solución:** Prueba a ser menos restrictivo con los filtros. Usa los botones "✅ Todas" en la barra lateral para reiniciar la vista.

**P: ¿Puedo ver los límites geográficos de los corregimientos?**

**R:** En la versión V3, se priorizó una vista más limpia mostrando solo puntos de calor. Sin embargo, los datos de los polígonos (GeoJSON) están integrados y pueden reactivarse en futuras versiones si se considera necesario.

**P: ¿Qué significa el "Puntaje de Prioridad"?**

**R:** Es un valor de 0 a 1 que calcula la necesidad de intervención de una zona. Un puntaje más alto significa mayor prioridad. Se calcula con la siguiente fórmula:

> **Puntaje = (Componente Educación * 50%) + (Componente Población * 20%) + (Componente Conectividad * 30%)**

Puedes ver el desglose de estos componentes en el panel lateral de cada zona.

**P: El botón "Descargar PDF" no aparece.**

**R:** El botón de descarga solo aparece *después* de haber hecho clic en "📥 Exportar a PDF" y el archivo se haya generado. El proceso es:
1. Clic en "Exportar a PDF".
2. Esperar 2-3 segundos.
3. Clic en "Descargar PDF".

---

### **3. Interpretación de Datos**

**P: Mi corregimiento tiene "Baja Prioridad", ¿significa que no necesita mejoras?**

**R:** No necesariamente. "Baja Prioridad" es un término **relativo** en comparación con las otras zonas de Jamundí. Puede que aún tenga áreas de oportunidad. Revisa los 7 gráficos del panel lateral para entender sus debilidades específicas, como la velocidad o la penetración.

**P: ¿Qué es una "Alerta Crítica"?**

**R:** Es la alerta más grave. Se activa principalmente cuando una **zona de alta prioridad tiene una sede educativa sin conexión a internet**. Esto representa una emergencia educativa que debe ser atendida de inmediato.

**P: ¿Por qué la "Evolución Temporal" es simulada?**

**R:** Los datos públicos de MinTIC a menudo se proporcionan a nivel municipal, no desglosados por corregimiento. Para mostrar la funcionalidad, el gráfico simula una evolución para cada zona. En un escenario de producción con acceso a datos más granulares de la Alcaldía, este gráfico mostraría la evolución real.

---

### **4. Aspectos Técnicos**

**P: ¿En qué tecnología está construido el dashboard?**

**R:** Está desarrollado en **Python** utilizando las siguientes librerías principales:
- **Streamlit:** Para la interfaz web interactiva.
- **Pandas:** Para la manipulación y análisis de datos.
- **Plotly:** Para los gráficos y mapas interactivos.
- **FPDF2:** Para la exportación de reportes a PDF.

**P: ¿Puedo usar el dashboard en mi celular?**

**R:** ¡Sí! El dashboard tiene un diseño **responsive**, lo que significa que se adapta a diferentes tamaños de pantalla, incluyendo tabletas y smartphones. La experiencia está optimizada para una fácil navegación en dispositivos móviles.

**P: ¿Es de código abierto?**

**R:** Sí, el proyecto se entrega con todo el código fuente, lo que permite que sea auditado, modificado y mejorado por la comunidad o por la Alcaldía de Jamundí.

---

**¿Tienes más preguntas?**

No dudes en contactar al equipo de desarrollo o explorar la pestaña "📄 Información del Proyecto" para más detalles.
