# Pipeline Datanex - Wiki Processor

Pipeline de nivel producción para descargar, procesar y unificar la wiki de Datanex (base de datos del Hospital Clínic) con scraping responsable, trazabilidad completa y reproducibilidad científica.

> **📖 Para documentación detallada del sistema de scraping**, ver [SCRAPING_GUIDE.md](SCRAPING_GUIDE.md)

## 📋 Descripción

Este proyecto descarga todas las páginas de la wiki de Datanex desde GitLab, las procesa, filtra las páginas relevantes, las convierte a Markdown y genera un archivo unificado (`vibe_SQL_copilot.txt`) que combina un prompt personalizado con toda la documentación de la base de datos. Este archivo está diseñado para ser usado como contexto en GitHub Copilot para generar queries SQL de alta calidad.

## 🚀 Características

### Scraping de Nivel Producción
- **Scraping responsable**: Rate limiting configurable (default: 2s entre requests)
- **Reintentos automáticos**: Backoff exponencial con hasta 3 intentos por página
- **Validación de integridad**: Checksums SHA256 de cada página descargada
- **Detección de cambios**: Solo re-descarga páginas modificadas (ahorra tiempo y ancho de banda)
- **Logging estructurado**: Logs JSON con timestamp, URL, checksums y resultados
- **Metadatos completos**: Manifest, logs y checksums para auditoría y reproducibilidad
- **Manejo robusto de errores**: Continúa ante fallos individuales, registra todo
- **Dominio seguro**: Solo sigue enlaces dentro del wiki (no sale del dominio)
- **User-Agent explícito**: Identificación clara como archivador clínico/investigación

### Pipeline de Procesamiento
- **Descarga automática**: Descarga recursiva de todas las páginas del wiki de GitLab
- **Estructura jerárquica**: Mantiene organización de carpetas reflejando la wiki
- **Filtrado inteligente**: Excluye páginas no relevantes según configuración
- **Conversión a Markdown**: HTML → Markdown preservando tablas y estructura
- **Limpieza automática**: Elimina secciones no relevantes y normaliza formato
- **Unificación**: Combina todos los documentos en un solo archivo optimizado
- **Procesamiento de diccionarios**: Convierte CSV a Markdown con optimización de tamaño
- **Compactación inteligente**: Reduce tamaño eliminando prefijos comunes y redundancia
- **Pipeline modular**: Cada paso es independiente, testeable y auditable

## 📁 Estructura del Proyecto

```
pipeline_datanex/
├── src/                          # Código fuente
│   ├── download_wiki.py          # Descarga de páginas wiki
│   ├── extract_text.py           # Extracción a Markdown
│   ├── unify_markdown.py         # Unificación de markdowns
│   ├── unify_dictionaries.py     # Unificación de diccionarios CSV
│   └── create_final_output.py    # Creación del archivo final
├── test/                         # Tests/Pasos del pipeline
│   ├── test_download_wiki.py
│   ├── test_filter_useful_pages.py
│   ├── test_extract_text.py
│   ├── test_download_linked_pages.py
│   ├── test_unify_markdown.py
│   ├── test_unify_dictionaries.py
│   ├── test_create_final_output.py
│   └── run_all_tests.py          # Ejecuta todo el pipeline
├── dicc/                         # Diccionarios CSV
│   ├── dic_diagnostic.csv        # Diccionario de diagnósticos
│   ├── dic_lab.csv               # Diccionario de laboratorio
│   └── dictionaries_unified.md   # Diccionarios unificados
├── data/                         # Datos procesados (ignorado en git)
│   ├── wiki_html/                # HTML descargado (con estructura jerárquica)
│   │   ├── metadata/             # Metadatos de descarga (manifest, logs, checksums)
│   │   ├── home.html
│   │   ├── datanex/              # Subcarpetas según estructura del wiki
│   │   └── ...
│   ├── wiki_work_html/           # HTML filtrado (páginas útiles)
│   ├── wiki_markdown/            # Markdowns generados
│   └── wiki_unified.md            # Markdown unificado
├── main.py                       # Script principal
├── ejecutar_pipeline.bat         # Script batch para ejecutar en Windows
├── ejecutar_pipeline.sh          # Script bash para ejecutar en Linux/Mac
├── prompt.txt                    # Prompt para Copilot
├── pags_descarte.txt             # Lista de páginas a descartar/excluir
└── vibe_SQL_copilot.txt          # Archivo final generado
```

## 🔧 Instalación

### Requisitos

- Python 3.8 o superior
- pip

### Pasos

1. **Clonar el repositorio**:
```bash
git clone https://github.com/ramsestein/vibe_SQL_Datanex.git
cd vibe_SQL_Datanex
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 📦 Dependencias

- `requests` - Para descargar páginas web
- `beautifulsoup4` - Para parsear HTML
- `markdownify` - Para convertir HTML a Markdown

## 🎯 Uso

### Ejecutar el pipeline completo

**Windows (más fácil)**:
```bash
ejecutar_pipeline.bat
```

**Linux/Mac (más fácil)**:
```bash
./ejecutar_pipeline.sh
```

**Desde la línea de comandos**:
```bash
python main.py
```

Ambos scripts (`ejecutar_pipeline.bat` y `ejecutar_pipeline.sh`) incluyen:
- Creación automática del entorno virtual si no existe
- Verificación e instalación automática de dependencias
- Ejecución automática del pipeline completo
- **Push automático**: Al finalizar el pipeline, sube automáticamente el archivo `vibe_SQL_copilot.txt` al repositorio [vibe_query_DataNex](https://github.com/ramsestein/vibe_query_DataNex)

Este comando ejecuta todos los pasos del pipeline en secuencia:

1. **Descarga desde home**: Descarga la página "home" de la wiki que contiene el menú lateral con todas las páginas disponibles
2. **Filtrado**: Excluye las páginas listadas en `pags_descarte.txt` (procesa todas las demás)
3. **Extracción a Markdown**: Convierte las páginas útiles a Markdown
4. **Unificación de markdowns**: Combina todos los markdowns de la wiki en un solo archivo (excluyendo las de `pags_descarte.txt`)
5. **Unificación de diccionarios**: Convierte diccionarios CSV a Markdown optimizado
6. **Archivo final**: Combina `prompt.txt` + `wiki_unified.md` + `dictionaries_unified.md` → `vibe_SQL_copilot.txt`

### Ejecutar pasos individuales

Cada paso puede ejecutarse de forma independiente usando los scripts de test:

```bash
# Paso 1: Descarga
python test/test_download_wiki.py

# Paso 2: Filtrado
python test/test_filter_useful_pages.py

# Paso 3: Extracción
python test/test_extract_text.py

# Paso 4: Descarga de referencias
python test/test_download_linked_pages.py

# Paso 5: Unificación de markdowns
python test/test_unify_markdown.py

# Paso 6: Unificación de diccionarios
python test/test_unify_dictionaries.py

# Paso 7: Archivo final
python test/test_create_final_output.py
```

### Ejecutar todos los pasos en secuencia

```bash
python test/run_all_tests.py
```

## ⚙️ Configuración

### Archivo `pags_descarte.txt`

Este archivo define qué páginas de la wiki se **EXCLUIRÁN** (descartarán) del prompt final. Cada línea debe contener el nombre de la página a excluir (sin extensión):

```
News
FAQs
Access-Instructions
...
```

**⚠️ Importante**: 
- La página `Overview` **siempre se incluirá**, incluso si está en esta lista de exclusión.
- Si el archivo está vacío o no existe, se procesarán **todas** las páginas disponibles.
- Esta es una lista de **exclusión**, no de inclusión.
- Las páginas listadas aquí también se excluirán automáticamente durante la unificación de markdowns.

### Archivo `prompt.txt`

Este archivo contiene el prompt que se incluirá al inicio del archivo final. Define el comportamiento esperado de Copilot al usar el contexto. Debe contener las secciones `### CONTEXTO ###` y `### DICCIONARIOS ###` donde se insertará el contenido correspondiente.

### Carpeta `dicc/`

Contiene los diccionarios CSV que se procesarán:
- `dic_diagnostic.csv`: Diccionario de diagnósticos con códigos y descripciones
- `dic_lab.csv`: Diccionario de laboratorio con códigos y descripciones

**⚠️ Configuración de columnas**: Para que el sistema procese correctamente los CSV, **debes renombrar manualmente** las columnas en tus archivos CSV para que terminen en `_ref` y `_descr`. Por ejemplo:
- Columna de códigos: `codigo_ref`, `id_ref`, `diagnostic_ref`, etc.
- Columna de descripciones: `descripcion_descr`, `nombre_descr`, `diagnostic_descr`, etc.

El sistema buscará automáticamente columnas que terminen en `*_ref` y `*_descr` en todos los archivos CSV de esta carpeta.

Los diccionarios se procesan automáticamente y se optimizan para reducir el tamaño del archivo final.

## 📊 Pipeline Detallado

### Paso 1: Descarga desde home (Scraping Responsable)
- Descarga la página "home" de la wiki desde [GitLab](https://gitlab.com/dsc-clinic/datascope/-/wikis/home)
- Extrae todos los enlaces del sidebar/menú lateral y contenido principal
- Sigue recursivamente enlaces internos del wiki (no sale del dominio)
- **Rate limiting**: 2 segundos entre requests (configurable)
- **Reintentos**: Hasta 3 intentos con backoff exponencial (2, 4, 8 segundos)
- **Validación**: Checksums SHA256, tamaño mínimo, Content-Type
- **Detección de cambios**: Solo re-descarga si el contenido cambió
- Guarda HTML en estructura jerárquica: `data/wiki_html/` con subcarpetas
- **Metadatos completos**:
  - `metadata/manifest.json`: Inventario completo (timestamp, URLs, lista de páginas)
  - `metadata/download_log.jsonl`: Log estructurado de cada operación (append-only)
  - `metadata/page_checksums.json`: SHA256 de cada página para detección de cambios
  - `metadata/README.md`: Documentación de metadatos y reproducibilidad

### Paso 2: Filtrado de páginas útiles
- Lee `pags_descarte.txt` (lista de páginas a EXCLUIR/DESCARTAR)
- Copia TODAS las páginas de `data/wiki_html/` EXCEPTO las listadas en `pags_descarte.txt`
- Siempre incluye `Overview` aunque esté en la lista de exclusión
- Guarda las páginas filtradas en `data/wiki_work_html/`

### Paso 3: Extracción a Markdown de páginas útiles
- Convierte todas las páginas filtradas a Markdown
- Guarda en `data/wiki_markdown/`

### Paso 4: Unificación de markdowns
- Combina todos los markdowns en un solo archivo
- **Excluye automáticamente** las páginas listadas en `pags_descarte.txt`
- Elimina secciones no relevantes (como "## Wiki Pages")
- Limpia saltos de línea dobles
- Convierte tablas HTML a formato Markdown
- Guarda en `data/wiki_unified.md`

### Paso 5: Unificación de diccionarios
- Lee todos los archivos CSV de la carpeta `dicc/`
- Busca columnas que terminen en `*_ref` y `*_descr` (deben estar renombradas manualmente)
- Extrae las columnas `*_ref` y `*_descr` de cada CSV
- **Optimización de tamaño**:
  - Detecta prefijos comunes en los códigos y los compacta
  - Extrae texto común de las descripciones para evitar repeticiones
  - Para `dic_lab.csv`: elimina conjunciones, determinantes y comas
- Guarda en `dicc/dictionaries_unified.md`

### Paso 6: Archivo final
- Combina `prompt.txt` + `wiki_unified.md` + `dictionaries_unified.md`
- Inserta el contenido de la wiki después de `### CONTEXTO ###`
- Inserta el contenido de diccionarios después de `### DICCIONARIOS ###`
- Guarda en `vibe_SQL_copilot.txt`

## 📝 Archivos Generados

Durante la ejecución del pipeline se generan los siguientes archivos:

### Datos de Descarga
- `data/wiki_html/`: Archivos HTML descargados con estructura jerárquica
  - `metadata/manifest.json`: Inventario completo de la descarga
  - `metadata/download_log.jsonl`: Log estructurado (append-only, mantiene histórico)
  - `metadata/page_checksums.json`: SHA256 checksums para validación
  - `metadata/README.md`: Documentación de metadatos
  - `home.html`, `datanex/`, etc.: Páginas organizadas en carpetas

### Datos Procesados
- `data/wiki_work_html/`: Archivos HTML filtrados (solo páginas útiles)
- `data/wiki_markdown/`: Archivos Markdown generados de cada página
- `data/wiki_unified.md`: Markdown unificado con todo el contenido de la wiki
- `dicc/dictionaries_unified.md`: Diccionarios CSV convertidos a Markdown

### Salida Final
- `vibe_SQL_copilot.txt`: Archivo final listo para usar en Copilot con estructura:
  ```
  [Contenido de prompt.txt]
  ### CONTEXTO ###
  [Contenido de wiki_unified.md]
  ### DICCIONARIOS ###
  [Contenido de dictionaries_unified.md]
  ```

## 🔍 Funciones Principales

### `download_wiki_pages()`
Descarga páginas wiki desde GitLab con scraping responsable de nivel producción:
- Rate limiting configurable (default: 2s)
- Reintentos automáticos con backoff exponencial
- Validación de integridad (SHA256 checksums)
- Detección de cambios (no re-descarga sin modificaciones)
- Logging estructurado completo
- Metadatos de trazabilidad (manifest, logs, checksums)

### `download_linked_pages()`
Extrae enlaces de archivos Markdown y descarga las páginas referenciadas.

### `filter_useful_pages()`
Filtra páginas excluyendo las que están en `pags_descarte.txt`. Procesa todas las páginas disponibles excepto las listadas. La página `Overview` siempre se incluye.

### `extract_text()`
Convierte HTML a Markdown preservando tablas y estructura.

### `unify_markdowns()`
Combina múltiples archivos Markdown en uno solo, limpiando contenido no relevante.

### `unify_dictionaries()`
Convierte diccionarios CSV a Markdown optimizado:
- Detecta prefijos comunes en códigos (sistema de árbol)
- Extrae texto común de descripciones para evitar repeticiones
- Aplica limpieza especial al diccionario de lab (elimina conjunciones, determinantes, comas)
- Formato compacto: `prefix:texto_comun|suffix1:diff1|suffix2:diff2|...`

### `create_final_output()`
Combina el prompt con la documentación unificada y los diccionarios, organizándolos en las secciones `### CONTEXTO ###` y `### DICCIONARIOS ###`.

## 🧪 Testing

Los archivos en `test/` actúan como pasos individuales del pipeline y pueden ejecutarse de forma independiente para debugging o para ejecutar solo una parte del proceso.

## 📄 Licencia

Este proyecto es de uso interno para el Hospital Clínic.

## 🔬 Reproducibilidad y Trazabilidad

Este pipeline está diseñado para entornos clínicos y de investigación donde la reproducibilidad y trazabilidad son **obligatorias**:

### Reproducibilidad
1. **Determinismo**: Misma entrada → misma salida
2. **Versionado completo**: Todo el código está en Git
3. **Dependencias fijadas**: `requirements.txt` con versiones específicas
4. **Metadatos timestamped**: Cada descarga registra fecha, hora y configuración
5. **Configuración explícita**: Todos los parámetros están documentados

### Trazabilidad
1. **Manifest completo** (`manifest.json`): Qué se descargó, cuándo, desde dónde
2. **Log estructurado** (`download_log.jsonl`): Cada operación registrada con:
   - Timestamp ISO 8601
   - URL completa
   - Status code HTTP
   - Tamaño del contenido
   - SHA256 checksum
   - Número de intento
   - Resultado (éxito/error)
3. **Checksums SHA256**: Validación de integridad de cada archivo
4. **Append-only log**: El log nunca se sobrescribe, mantiene histórico completo
5. **README de metadatos**: Documentación legible por humanos

### Detección de Cambios
- En ejecuciones posteriores, el sistema:
  1. Lee checksums existentes
  2. Compara con versión actual del archivo
  3. Solo re-descarga si hay cambios
  4. Registra en el log si se usó versión cacheada o se re-descargó

### Auditoría
Todos los archivos de metadatos pueden usarse para:
- Auditar qué datos se usaron en análisis específicos
- Verificar integridad de datos
- Reproducir análisis exactos
- Documentar para publicaciones científicas

### Actualización del Wiki
Para actualizar el contenido del wiki manteniendo trazabilidad:
```bash
# Simplemente ejecuta de nuevo el pipeline
python main.py
# O usa los scripts automáticos
./ejecutar_pipeline.sh  # Linux/Mac
ejecutar_pipeline.bat   # Windows
```

El sistema:
1. Detecta qué páginas cambiaron (vía checksums)
2. Solo re-descarga las modificadas
3. Registra todo en `download_log.jsonl` (append)
4. Actualiza `manifest.json` con nueva fecha
5. Mantiene histórico completo en el log

## ⚠️ Consideraciones y Limitaciones

### Rate Limiting
- **Default**: 2 segundos entre requests
- **Justificación**: Scraping responsable, no sobrecargar servidor GitLab
- **Configurable**: Puede ajustarse en `main.py` si es necesario
- **Reintentos**: Backoff exponencial (2, 4, 8 segundos) ante errores

### Dependencias Externas
- **GitLab**: Cambios en la estructura HTML pueden requerir ajustes en selectores
- **Red**: Requiere conexión estable para descargas masivas
- **Permisos**: Debe tener acceso al wiki (público o credenciales apropiadas)

### Mantenimiento
- **Selectores HTML**: Pueden requerir actualización si GitLab cambia su UI
- **Logs acumulativos**: `download_log.jsonl` crece con cada ejecución (considerar rotación)
- **Checksums**: Permanecen hasta regeneración completa

### Uso en Producción Clínica
Este código cumple con prácticas de:
- ✅ Reproducibilidad científica
- ✅ Trazabilidad completa
- ✅ Validación de integridad
- ✅ Logging estructurado
- ✅ Manejo robusto de errores
- ✅ Documentación exhaustiva

## 🔗 Enlaces

- Wiki original: [Datanex Wiki (home)](https://gitlab.com/dsc-clinic/datascope/-/wikis/home)
- Proyecto Datascope: [GitLab - dsc-clinic/datascope](https://gitlab.com/dsc-clinic/datascope)
- GitHub Copilot: [GitHub Copilot](https://github.com/features/copilot)
