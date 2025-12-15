# Pipeline Datanex - Wiki Processor

Pipeline para descargar, limpiar y procesar la wiki de Datanex (base de datos del Hospital Clínic) y generar un archivo de contexto optimizado para GitHub Copilot.

## 📋 Descripción

Este proyecto descarga todas las páginas de la wiki de Datanex desde GitLab, las procesa, filtra las páginas relevantes, las convierte a Markdown y genera un archivo unificado (`vibe_SQL_copilot.txt`) que combina un prompt personalizado con toda la documentación de la base de datos. Este archivo está diseñado para ser usado como contexto en GitHub Copilot para generar queries SQL de alta calidad.

## 🚀 Características

- **Descarga automática**: Descarga recursiva de páginas wiki desde GitLab
- **Filtrado inteligente**: Filtra solo las páginas útiles según un archivo de configuración
- **Conversión a Markdown**: Convierte HTML a Markdown preservando tablas y estructura
- **Limpieza automática**: Elimina secciones no relevantes y normaliza el formato
- **Unificación**: Combina todos los documentos en un solo archivo optimizado
- **Procesamiento de diccionarios**: Convierte diccionarios CSV a Markdown con optimización de tamaño
- **Compactación inteligente**: Reduce el tamaño eliminando prefijos comunes y texto redundante
- **Pipeline modular**: Cada paso es independiente y testeable

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
│   ├── wiki_html/                # HTML descargado
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
- Menú interactivo para gestionar la lista de páginas a excluir
- Creación automática del entorno virtual si no existe
- Verificación e instalación automática de dependencias
- Gestión de páginas: ver, agregar o quitar páginas de la lista de exclusión
- **Push automático**: Al finalizar el pipeline, sube automáticamente el archivo `vibe_SQL_copilot.txt` al repositorio [vibe_query_DataNex](https://github.com/ramsestein/vibe_query_DataNex)

Este comando ejecuta todos los pasos del pipeline en secuencia:

1. **Descarga del Overview**: Descarga la página principal de la wiki
2. **Extracción a Markdown**: Convierte el Overview a Markdown
3. **Descarga de páginas referenciadas**: Descarga todas las páginas enlazadas en el Overview
4. **Filtrado**: Excluye las páginas listadas en `pags_descarte.txt` (procesa todas las demás)
5. **Extracción a Markdown**: Convierte las páginas útiles a Markdown
6. **Unificación de markdowns**: Combina todos los markdowns de la wiki en un solo archivo
7. **Unificación de diccionarios**: Convierte diccionarios CSV a Markdown optimizado
8. **Archivo final**: Combina `prompt.txt` + `wiki_unified.md` + `dictionaries_unified.md` → `vibe_SQL_copilot.txt`

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
- La página `Overview` **siempre se incluirá**, incluso si está en esta lista de exclusión, ya que es necesaria para descargar las páginas referenciadas.
- Si el archivo está vacío o no existe, se procesarán **todas** las páginas disponibles.
- Esta es una lista de **exclusión**, no de inclusión.

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

### Paso 1: Descarga del Overview
- Descarga la página principal de la wiki
- Guarda el HTML en `data/wiki_html/`

### Paso 2: Extracción a Markdown del Overview
- Extrae el contenido principal del HTML
- Convierte a Markdown preservando tablas
- Guarda en `data/wiki_markdown/Overview.md`

### Paso 3: Descarga de páginas referenciadas
- Lee el Overview.md y extrae todos los enlaces a otras páginas wiki
- Descarga cada página referenciada
- Guarda en `data/wiki_html/`

### Paso 4: Filtrado de páginas útiles
- Lee `pags_descarte.txt` (lista de páginas a EXCLUIR/DESCARTAR)
- Copia TODAS las páginas de `data/wiki_html/` EXCEPTO las listadas en `pags_descarte.txt`
- Siempre incluye `Overview` aunque esté en la lista de exclusión
- Guarda las páginas filtradas en `data/wiki_work_html/`

### Paso 5: Extracción a Markdown de páginas útiles
- Convierte todas las páginas filtradas a Markdown
- Guarda en `data/wiki_markdown/`

### Paso 6: Unificación de markdowns
- Combina todos los markdowns en un solo archivo
- Elimina secciones no relevantes (como "## Wiki Pages")
- Limpia saltos de línea dobles
- Convierte tablas HTML a formato Markdown
- Guarda en `data/wiki_unified.md`

### Paso 7: Unificación de diccionarios
- Lee todos los archivos CSV de la carpeta `dicc/`
- Busca columnas que terminen en `*_ref` y `*_descr` (deben estar renombradas manualmente)
- Extrae las columnas `*_ref` y `*_descr` de cada CSV
- **Optimización de tamaño**:
  - Detecta prefijos comunes en los códigos y los compacta
  - Extrae texto común de las descripciones para evitar repeticiones
  - Para `dic_lab.csv`: elimina conjunciones, determinantes y comas
- Guarda en `dicc/dictionaries_unified.md`

### Paso 8: Archivo final
- Combina `prompt.txt` + `wiki_unified.md` + `dictionaries_unified.md`
- Inserta el contenido de la wiki después de `### CONTEXTO ###`
- Inserta el contenido de diccionarios después de `### DICCIONARIOS ###`
- Guarda en `vibe_SQL_copilot.txt`

## 📝 Archivos Generados

- `data/wiki_unified.md`: Markdown unificado con toda la documentación de la wiki
- `dicc/dictionaries_unified.md`: Diccionarios unificados y optimizados
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
Descarga páginas wiki desde GitLab, usando la API para obtener el contenido real.

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

## 🔗 Enlaces

- [Wiki de Datanex](https://gitlab.com/dsc-clinic/datascope/-/wikis/Overview)
