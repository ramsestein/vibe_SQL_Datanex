# Guía de Scraping Responsable - Wiki Datascope

## Objetivo

Este documento describe el sistema de scraping de nivel producción implementado para descargar la wiki de Datascope desde GitLab, diseñado específicamente para entornos clínicos y de investigación donde la **reproducibilidad**, **trazabilidad** y **scraping responsable** son obligatorios.

## URL del Wiki

**URL raíz**: https://gitlab.com/dsc-clinic/datascope/-/wikis/home

El wiki contiene múltiples páginas internas enlazadas entre sí, incluyendo:
- Datanex (catálogo de datos, tablas clínicas)
- Tutoriales SQL
- FAQs
- Documentación de gobernanza
- Instrucciones de acceso
- Y más...

## Características del Scraper

### 1. Scraping Responsable

#### Rate Limiting
- **Default**: 2 segundos entre requests
- **Justificación**: No sobrecargar el servidor de GitLab
- **Configurable**: Puede ajustarse según necesidades
- **Implementación**: `time.sleep(rate_limit)` entre cada descarga

#### User-Agent Explícito
```python
'User-Agent': 'Mozilla/5.0 (compatible; DataScopeWikiArchiver/1.0; +Clinical/Research)'
```
- Identifica claramente el propósito del scraper
- Indica que es para uso clínico/investigación
- Facilita que administradores de GitLab puedan contactar si hay problemas

#### Reintentos con Backoff Exponencial
- **Máximo**: 3 intentos por página
- **Backoff**: 2^n segundos (2s, 4s, 8s)
- **Justificación**: Maneja errores transitorios sin saturar el servidor
- **Logging**: Cada intento se registra en el log estructurado

### 2. Validación de Integridad

#### Checksums SHA256
- Cada página descargada tiene su checksum SHA256
- Guardados en `data/wiki_html/metadata/page_checksums.json`
- Permite:
  - Verificar integridad de archivos
  - Detectar cambios entre ejecuciones
  - Auditoría y validación

#### Validaciones en Descarga
1. **Content-Type**: Verifica que la respuesta sea HTML
2. **Tamaño mínimo**: Rechaza respuestas sospechosamente cortas (<100 bytes)
3. **Status HTTP**: Solo acepta 200 OK
4. **Encoding**: UTF-8 para caracteres especiales

### 3. Detección de Cambios (Idempotencia)

El scraper es **idempotente**: ejecutarlo múltiples veces con el mismo input produce el mismo output.

#### Funcionamiento
1. **Primera ejecución**: Descarga todas las páginas, guarda checksums
2. **Ejecuciones posteriores**:
   - Lee checksums existentes
   - Calcula checksum del archivo local
   - Compara con checksum guardado
   - Si son iguales: usa versión cacheada (no descarga)
   - Si son diferentes: re-descarga y actualiza checksum

#### Beneficios
- **Ahorro de tiempo**: No re-descarga páginas sin cambios
- **Ahorro de ancho de banda**: Reduce carga en red
- **Trazabilidad**: Log indica si se usó caché o se descargó
- **Reproducibilidad**: Mismo contenido → mismo resultado

### 4. Logging Estructurado

#### Formato JSON Lines (JSONL)
Archivo: `data/wiki_html/metadata/download_log.jsonl`

Cada línea es un objeto JSON con:
```json
{
  "timestamp": "2025-12-15T10:30:45.123456",
  "page_name": "datanex/overview",
  "url": "https://gitlab.com/dsc-clinic/datascope/-/wikis/datanex/overview",
  "status_code": 200,
  "content_length": 45678,
  "sha256": "a1b2c3d4e5f6...",
  "attempt": 1,
  "success": true
}
```

#### Características
- **Append-only**: Nunca se sobrescribe, mantiene histórico completo
- **Parseable**: Fácil de procesar con scripts (jq, Python, etc.)
- **Timestamps ISO 8601**: Formato estándar internacional
- **Completo**: Incluye tanto éxitos como fallos

#### Análisis del Log
```bash
# Contar descargas exitosas
grep '"success":true' data/wiki_html/metadata/download_log.jsonl | wc -l

# Ver páginas con errores
grep '"success":false' data/wiki_html/metadata/download_log.jsonl | jq .

# Páginas descargadas hoy
grep "2025-12-15" data/wiki_html/metadata/download_log.jsonl | jq .page_name
```

### 5. Metadatos de Trazabilidad

#### Manifest (`manifest.json`)
Inventario completo de cada ejecución:
```json
{
  "download_timestamp": "2025-12-15T10:30:45.123456",
  "base_url": "https://gitlab.com/dsc-clinic/datascope/-/wikis/home",
  "wiki_base": "https://gitlab.com/dsc-clinic/datascope/-/wikis",
  "domain": "https://gitlab.com",
  "total_pages": 42,
  "pages": ["home", "datanex/overview", ...],
  "output_directory": "data/wiki_html",
  "rate_limit": 2.0,
  "max_retries": 3,
  "respect_existing": true
}
```

**Uso**: Documentar exactamente qué se descargó, cuándo y con qué configuración.

#### Checksums (`page_checksums.json`)
```json
{
  "home": "a1b2c3d4e5f6...",
  "datanex/overview": "f6e5d4c3b2a1...",
  ...
}
```

**Uso**: Validación de integridad y detección de cambios.

#### README de Metadatos
Archivo legible por humanos que explica:
- Qué contiene cada archivo de metadatos
- Cómo usar los metadatos para reproducibilidad
- Cómo auditar las descargas

### 6. Estructura de Carpetas Jerárquica

El scraper **mantiene la estructura del wiki**:

```
data/wiki_html/
├── metadata/
│   ├── manifest.json
│   ├── download_log.jsonl
│   ├── page_checksums.json
│   └── README.md
├── home.html
├── datanex/
│   ├── overview.html
│   ├── catalog.html
│   └── tables.html
├── sql/
│   ├── tutorial.html
│   └── examples.html
├── governance.html
└── faq.html
```

**Beneficios**:
- Organización clara y navegable
- Refleja la estructura original del wiki
- Facilita encontrar páginas específicas
- Permite versionado en Git de forma coherente

### 7. Seguridad de Dominio

El scraper **solo descarga del dominio del wiki**:

```python
is_same_domain = parsed_link.netloc == parsed_url.netloc
is_wiki_path = '/-/wikis/' in absolute_url

if is_same_domain and is_wiki_path:
    # Descargar
```

**Protecciones**:
- No sigue enlaces externos
- No descarga recursos de otros dominios
- No descarga archivos no-wiki (issues, merge requests, etc.)
- Solo páginas con `/-/wikis/` en la URL

### 8. Manejo Robusto de Errores

#### Estrategia
1. **Reintentos automáticos**: Hasta 3 intentos con backoff
2. **Logging de errores**: Todos los fallos se registran
3. **Continuación**: Un fallo no detiene el scraping completo
4. **Información detallada**: Stack traces y mensajes descriptivos

#### Tipos de Errores Manejados
- `RequestException`: Errores de red, timeouts
- `HTTPError`: Status codes 4xx, 5xx
- `ValueError`: Contenido inválido o sospechoso
- `Exception`: Errores inesperados

## Configuración

### Parámetros de `download_wiki_pages()`

```python
download_wiki_pages(
    base_url="https://gitlab.com/dsc-clinic/datascope/-/wikis/home",
    output_dir="data/wiki_html",
    rate_limit=2.0,        # Segundos entre requests
    max_retries=3,         # Intentos por página
    respect_existing=True  # Usar caché si no hay cambios
)
```

### Ajustes Recomendados

#### Para Descarga Rápida (uso interno, testing)
```python
rate_limit=1.0,
max_retries=2
```

#### Para Scraping Ultra-Conservador (producción)
```python
rate_limit=5.0,
max_retries=5
```

#### Para Re-descarga Completa (forzar actualización)
```python
respect_existing=False
```

## Reproducibilidad

### Ejecución Determinista
Misma entrada → misma salida:
1. URLs fijas (no dependen de hora/fecha)
2. Algoritmos deterministas (SHA256, parsing HTML)
3. Configuración explícita (no valores aleatorios)
4. Dependencias versionadas (`requirements.txt`)

### Versionado en Git
Todos los archivos necesarios están versionados:
- ✅ Código fuente (`src/download_wiki.py`)
- ✅ Configuración (`main.py`)
- ✅ Dependencias (`requirements.txt`)
- ✅ Documentación (este archivo)
- ❌ Datos descargados (`data/` en `.gitignore`)
- ✅ Metadatos (opcional, pueden versionarse)

### Documentación para Publicaciones
Los metadatos generados son suficientes para documentar en papers:

> "Los datos de la wiki de Datascope fueron descargados el [fecha del manifest] 
> desde [base_url del manifest] usando un scraper Python con rate limiting de 
> 2 segundos entre requests. La integridad de los [total_pages] archivos 
> descargados fue verificada mediante checksums SHA256. El código y metadatos 
> completos están disponibles en [URL del repositorio]."

## Actualización del Wiki

### Procedimiento
1. Ejecutar el pipeline:
   ```bash
   python main.py
   # O usar scripts automáticos
   ./ejecutar_pipeline.sh  # Linux/Mac
   ejecutar_pipeline.bat   # Windows
   ```

2. El sistema automáticamente:
   - Detecta páginas modificadas (vía checksums)
   - Re-descarga solo las modificadas
   - Mantiene páginas sin cambios (usa caché)
   - Registra todo en `download_log.jsonl` (append)
   - Actualiza `manifest.json` con nueva fecha

3. Revisar metadatos:
   ```bash
   cat data/wiki_html/metadata/manifest.json
   tail -20 data/wiki_html/metadata/download_log.jsonl
   ```

### Frecuencia Recomendada
- **Desarrollo activo**: Semanal
- **Mantenimiento**: Mensual
- **Producción estable**: Trimestral
- **Bajo demanda**: Cuando se notifiquen cambios importantes

## Limitaciones y Consideraciones

### Dependencias Externas

#### GitLab
- **Cambios en HTML**: Si GitLab modifica su estructura HTML, los selectores pueden requerir ajustes
- **Solución**: Revisar y actualizar selectores en `src/download_wiki.py`
- **Selectores actuales**:
  ```python
  sidebar_selectors = [
      'aside', 
      'div.wiki-sidebar', 
      'div.wiki-sidebar-custom-content',
      'nav.wiki-sidebar',
      # ... más opciones
  ]
  ```

#### Red
- **Conexión estable**: Descargas masivas requieren conexión confiable
- **Solución**: Reintentos automáticos manejan fallos transitorios
- **Recomendación**: Ejecutar en entorno con buena conectividad

#### Permisos
- **Acceso al wiki**: Debe ser público o tener credenciales apropiadas
- **Actual**: Wiki de Datascope es accesible con credenciales del Clínic
- **Futuro**: Si cambian permisos, puede requerir autenticación en requests

### Mantenimiento

#### Logs Acumulativos
`download_log.jsonl` crece con cada ejecución:
- **Problema**: Puede volverse muy grande con el tiempo
- **Solución**: Rotación periódica de logs
- **Ejemplo**:
  ```bash
  # Rotar log mensualmente
  mv data/wiki_html/metadata/download_log.jsonl \
     data/wiki_html/metadata/download_log_$(date +%Y%m).jsonl
  ```

#### Checksums
- **Permanencia**: Se mantienen hasta regeneración completa
- **Limpieza**: Para forzar re-descarga completa, borrar `page_checksums.json`
- **Cuidado**: Borrar checksums invalida detección de cambios

### Rate Limiting de GitLab

GitLab puede tener límites de rate no documentados:
- **Síntoma**: Múltiples errores 429 (Too Many Requests)
- **Solución**: Aumentar `rate_limit` en configuración
- **Ejemplo**: Cambiar de 2.0 a 5.0 segundos

## Uso en Producción Clínica

Este scraper cumple con estándares de:

### ✅ Reproducibilidad Científica
- Código versionado
- Dependencias fijadas
- Configuración explícita
- Metadatos timestamped
- Algoritmos deterministas

### ✅ Trazabilidad Completa
- Manifest de cada ejecución
- Log estructurado de cada operación
- Checksums de validación
- Histórico completo (append-only)
- Documentación exhaustiva

### ✅ Validación de Integridad
- SHA256 checksums
- Validación de Content-Type
- Validación de tamaño
- Detección de cambios
- Verificación post-descarga

### ✅ Scraping Responsable
- Rate limiting conservador
- User-Agent explícito
- Reintentos con backoff
- No sobrecarga servidores
- Respeta estructura del sitio

### ✅ Manejo Robusto de Errores
- Reintentos automáticos
- Logging de errores
- Continuación ante fallos
- Información detallada
- Recuperación automática

### ✅ Documentación Exhaustiva
- README completo
- Guía de scraping (este documento)
- Comentarios en código
- Metadatos auto-documentados
- Ejemplos de uso

## Soporte y Contacto

Para problemas o preguntas sobre el scraper:
1. Revisar logs en `data/wiki_html/metadata/download_log.jsonl`
2. Verificar checksums en `page_checksums.json`
3. Consultar manifest en `manifest.json`
4. Revisar código en `src/download_wiki.py`

## Referencias

- **GitLab Wiki**: https://gitlab.com/dsc-clinic/datascope/-/wikis/home
- **Proyecto Datascope**: https://gitlab.com/dsc-clinic/datascope
- **Documentación de requests**: https://requests.readthedocs.io/
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/

