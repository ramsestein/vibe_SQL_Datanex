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
- **Pipeline modular**: Cada paso es independiente y testeable

## 📁 Estructura del Proyecto

```
pipeline_datanex/
├── src/                          # Código fuente
│   ├── download_wiki.py          # Descarga de páginas wiki
│   ├── extract_text.py           # Extracción a Markdown
│   ├── unify_markdown.py         # Unificación de markdowns
│   └── create_final_output.py    # Creación del archivo final
├── test/                         # Tests/Pasos del pipeline
│   ├── test_download_wiki.py
│   ├── test_filter_useful_pages.py
│   ├── test_extract_text.py
│   ├── test_download_linked_pages.py
│   ├── test_unify_markdown.py
│   ├── test_create_final_output.py
│   └── run_all_tests.py          # Ejecuta todo el pipeline
├── data/                         # Datos procesados (ignorado en git)
│   ├── wiki_html/                # HTML descargado
│   ├── wiki_work_html/           # HTML filtrado (páginas útiles)
│   ├── wiki_markdown/            # Markdowns generados
│   └── wiki_unified.md            # Markdown unificado
├── main.py                       # Script principal
├── prompt.txt                    # Prompt para Copilot
├── pags_utiles.txt               # Lista de páginas a procesar
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

```bash
python main.py
```

Este comando ejecuta todos los pasos del pipeline en secuencia:

1. **Descarga del Overview**: Descarga la página principal de la wiki
2. **Extracción a Markdown**: Convierte el Overview a Markdown
3. **Descarga de páginas referenciadas**: Descarga todas las páginas enlazadas en el Overview
4. **Filtrado**: Filtra solo las páginas listadas en `pags_utiles.txt`
5. **Extracción a Markdown**: Convierte las páginas útiles a Markdown
6. **Unificación**: Combina todos los markdowns en un solo archivo
7. **Archivo final**: Combina `prompt.txt` + `wiki_unified.md` → `vibe_SQL_copilot.txt`

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

# Paso 5: Unificación
python test/test_unify_markdown.py

# Paso 6: Archivo final
python test/test_create_final_output.py
```

### Ejecutar todos los pasos en secuencia

```bash
python test/run_all_tests.py
```

## ⚙️ Configuración

### Archivo `pags_utiles.txt`

Este archivo contiene la lista de páginas wiki que se procesarán. Cada línea debe contener el nombre de la página (sin extensión):

```
Overview
Administrations
Diagnostics-and-DRG
...
```

### Archivo `prompt.txt`

Este archivo contiene el prompt que se incluirá al inicio del archivo final. Define el comportamiento esperado de Copilot al usar el contexto.

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
- Lee `pags_utiles.txt`
- Copia solo las páginas listadas a `data/wiki_work_html/`

### Paso 5: Extracción a Markdown de páginas útiles
- Convierte todas las páginas filtradas a Markdown
- Guarda en `data/wiki_markdown/`

### Paso 6: Unificación
- Combina todos los markdowns en un solo archivo
- Elimina secciones no relevantes (como "## Wiki Pages")
- Limpia saltos de línea dobles
- Convierte tablas HTML a formato Markdown
- Guarda en `data/wiki_unified.md`

### Paso 7: Archivo final
- Combina `prompt.txt` + `wiki_unified.md`
- Guarda en `vibe_SQL_copilot.txt`

## 📝 Archivos Generados

- `data/wiki_unified.md`: Markdown unificado con toda la documentación
- `vibe_SQL_copilot.txt`: Archivo final listo para usar en Copilot

## 🔍 Funciones Principales

### `download_wiki_pages()`
Descarga páginas wiki desde GitLab, usando la API para obtener el contenido real.

### `download_linked_pages()`
Extrae enlaces de archivos Markdown y descarga las páginas referenciadas.

### `filter_useful_pages()`
Filtra páginas según la lista en `pags_utiles.txt`.

### `extract_text()`
Convierte HTML a Markdown preservando tablas y estructura.

### `unify_markdowns()`
Combina múltiples archivos Markdown en uno solo, limpiando contenido no relevante.

### `create_final_output()`
Combina el prompt con la documentación unificada.

## 🧪 Testing

Los archivos en `test/` actúan como pasos individuales del pipeline y pueden ejecutarse de forma independiente para debugging o para ejecutar solo una parte del proceso.

## 📄 Licencia

Este proyecto es de uso interno para el Hospital Clínic.

## 👤 Autor

Ramsés Stein

## 🔗 Enlaces

- [Wiki de Datanex](https://gitlab.com/dsc-clinic/datascope/-/wikis/Overview)
- [Repositorio GitHub](https://github.com/ramsestein/vibe_SQL_Datanex)

