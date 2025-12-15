"""
Script para descargar todas las páginas de una wiki de GitLab.

Este módulo implementa scraping responsable y robusto para entornos de producción,
con énfasis en reproducibilidad y trazabilidad para uso clínico/investigación.

Características:
- Logging estructurado con niveles apropiados
- Rate limiting configurable para scraping responsable
- Reintentos automáticos con backoff exponencial
- Validación de integridad de descargas
- Metadatos de descarga (timestamp, URL, hash)
- Detección de cambios (idempotente)
- Estructura de carpetas jerárquica que refleja la wiki
- No sale del dominio del wiki
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, unquote
import os
import time
import shutil
import re
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Set, List, Dict, Optional, Tuple
from copy import copy

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def download_wiki_pages(
    base_url: str, 
    output_dir: str = "data/wiki_html",
    rate_limit: float = 2.0,
    max_retries: int = 3,
    respect_existing: bool = True
) -> Dict[str, str]:
    """
    Descarga todas las páginas de una wiki de GitLab de forma robusta y responsable.
    
    Este scraper está diseñado para entornos de producción clínica/investigación con
    énfasis en reproducibilidad, trazabilidad y scraping responsable.
    
    Args:
        base_url: URL base de la wiki (ej: https://gitlab.com/dsc-clinic/datascope/-/wikis/home)
        output_dir: Directorio raíz donde guardar los archivos HTML
        rate_limit: Segundos de espera entre requests (default: 2.0 para ser conservador)
        max_retries: Número máximo de reintentos por página (default: 3)
        respect_existing: Si True, no redownload páginas sin cambios (default: True)
    
    Returns:
        Diccionario con el nombre de la página como clave y el contenido HTML como valor
        
    Estructura de salida:
        output_dir/
          ├── metadata/
          │   ├── manifest.json          # Inventario completo de descarga
          │   ├── download_log.jsonl     # Log estructurado de cada operación
          │   └── page_checksums.json    # Hashes para detección de cambios
          ├── home.html
          ├── datanex/
          │   ├── overview.html
          │   └── catalog.html
          └── ...
    """
    # Crear directorios
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    metadata_dir = output_path / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    logger.info(f"Iniciando descarga de wiki desde: {base_url}")
    logger.info(f"Directorio de salida: {output_dir}")
    logger.info(f"Rate limit: {rate_limit}s | Reintentos: {max_retries} | Respetar existentes: {respect_existing}")
    
    # Extraer información del dominio
    parsed_url = urlparse(base_url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    wiki_base = f"{domain}{'/'.join(parsed_url.path.split('/')[:-1])}"
    
    # Validar que estamos en un wiki de GitLab
    if '/-/wikis/' not in base_url:
        logger.error("URL no parece ser un wiki de GitLab (falta /-/wikis/)")
        raise ValueError("URL debe contener '/-/wikis/' para ser un wiki de GitLab válido")
    
    # Cargar checksums existentes si existen
    checksums_file = metadata_dir / "page_checksums.json"
    existing_checksums = {}
    if respect_existing and checksums_file.exists():
        try:
            with open(checksums_file, 'r', encoding='utf-8') as f:
                existing_checksums = json.load(f)
            logger.info(f"Cargados {len(existing_checksums)} checksums existentes")
        except Exception as e:
            logger.warning(f"No se pudieron cargar checksums existentes: {e}")
    
    # Conjunto para rastrear páginas procesadas
    downloaded_pages: Set[str] = set()
    pages_to_download: List[str] = []
    pages_content: Dict[str, str] = {}
    download_log: List[Dict] = []
    
    # Empezar con la página inicial
    initial_page = base_url.split('/')[-1] if '/' in base_url else 'home'
    pages_to_download.append(initial_page)
    
    # Headers explícitos para identificación responsable
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; DataScopeWikiArchiver/1.0; +Clinical/Research)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }
    
    logger.info(f"Comenzando desde página inicial: {initial_page}")
    
    session = requests.Session()
    session.headers.update(headers)
    
    while pages_to_download:
        page_name = pages_to_download.pop(0)
        
        if page_name in downloaded_pages:
            continue
        
        # Construir URL de la página
        page_url = f"{wiki_base}/{page_name}"
        
        # Determinar estructura de carpetas (detectar rutas anidadas)
        # Ej: "datanex/overview" -> crear carpeta datanex/
        page_path_parts = page_name.split('/')
        if len(page_path_parts) > 1:
            # Página anidada
            subfolder = output_path / Path(*page_path_parts[:-1])
            subfolder.mkdir(parents=True, exist_ok=True)
            file_name = page_path_parts[-1] + '.html'
            file_path = subfolder / file_name
        else:
            # Página en raíz
            file_path = output_path / f"{page_name}.html"
        
        # Verificar si ya existe y tiene el mismo checksum
        skip_download = False
        if respect_existing and file_path.exists():
            existing_hash = existing_checksums.get(page_name)
            if existing_hash:
                # Calcular hash del archivo existente
                with open(file_path, 'rb') as f:
                    current_hash = hashlib.sha256(f.read()).hexdigest()
                if current_hash == existing_hash:
                    logger.info(f"✓ Sin cambios: {page_name} (usando versión cacheada)")
                    downloaded_pages.add(page_name)
                    # Aún así leer el contenido para extraer enlaces
                    with open(file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    pages_content[page_name] = html_content
                    skip_download = True
        
        if not skip_download:
            # Descargar con reintentos
            html_content = None
            last_error = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"[{attempt}/{max_retries}] Descargando: {page_name}")
                    
                    response = session.get(page_url, timeout=30, allow_redirects=True)
                    response.raise_for_status()
                    
                    # Validar que la respuesta es HTML
                    content_type = response.headers.get('Content-Type', '')
                    if 'text/html' not in content_type:
                        logger.warning(f"⚠ Página {page_name} no es HTML (Content-Type: {content_type})")
                    
                    html_content = response.text
                    
                    # Validar que el contenido no está vacío
                    if len(html_content) < 100:
                        raise ValueError(f"Contenido sospechosamente corto: {len(html_content)} bytes")
                    
                    # Calcular checksum
                    content_hash = hashlib.sha256(html_content.encode('utf-8')).hexdigest()
                    
                    # Guardar HTML
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Registrar en log estructurado
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'page_name': page_name,
                        'url': page_url,
                        'status_code': response.status_code,
                        'content_length': len(html_content),
                        'sha256': content_hash,
                        'attempt': attempt,
                        'success': True
                    }
                    download_log.append(log_entry)
                    
                    # Guardar checksum para futuras comparaciones
                    existing_checksums[page_name] = content_hash
                    
                    pages_content[page_name] = html_content
                    downloaded_pages.add(page_name)
                    
                    logger.info(f"✓ Descargado: {page_name} ({len(html_content)} bytes, SHA256: {content_hash[:12]}...)")
                    break  # Éxito, salir del loop de reintentos
                    
                except requests.exceptions.RequestException as e:
                    last_error = e
                    logger.warning(f"✗ Intento {attempt} fallido para {page_name}: {e}")
                    
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'page_name': page_name,
                        'url': page_url,
                        'attempt': attempt,
                        'success': False,
                        'error': str(e)
                    }
                    download_log.append(log_entry)
                    
                    if attempt < max_retries:
                        # Backoff exponencial: 2^attempt segundos
                        backoff = 2 ** attempt
                        logger.info(f"  Reintentando en {backoff}s...")
                        time.sleep(backoff)
                    else:
                        logger.error(f"✗ Error permanente en {page_name} tras {max_retries} intentos: {last_error}")
                        continue
                
                except Exception as e:
                    last_error = e
                    logger.error(f"✗ Error inesperado en {page_name}: {e}")
                    break
            
            # Si no se pudo descargar, continuar con la siguiente
            if html_content is None:
                continue
            
            # Rate limiting: esperar antes de la siguiente request
            time.sleep(rate_limit)
        
        # Parsear HTML para encontrar enlaces a otras páginas de la wiki
        soup = BeautifulSoup(html_content, 'html.parser')
            
        # Buscar enlaces en el sidebar/menú lateral y contenido principal
        links_found = set()
        
        # Buscar el sidebar/menú lateral primero (contiene todas las páginas)
        sidebar_selectors = [
            'aside', 
            'div.wiki-sidebar', 
            'div.wiki-sidebar-custom-content',
            'nav.wiki-sidebar',
            'div[class*="sidebar"]',
            'ul.wiki-pages-list',
            'div[data-testid="wiki-sidebar"]',
            'nav[aria-label*="Wiki"]'
        ]
        
        sidebar = None
        for selector in sidebar_selectors:
            sidebar = soup.select_one(selector)
            if sidebar:
                logger.debug(f"Sidebar encontrado con selector: {selector}")
                break
        
        # Buscar también en el contenido principal
        main_content = None
        for selector in ['div.wiki-page-details', 'article', 'main', 'div.content', 'div[class*="wiki-page"]']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            body = soup.find('body')
            if body:
                main_content = body
            else:
                main_content = soup
        
        # Áreas donde buscar enlaces (sidebar primero, luego contenido principal)
        search_areas = []
        if sidebar:
            search_areas.append(('sidebar', sidebar))
        if main_content:
            search_areas.append(('content', main_content))
        
        # Buscar enlaces en todas las áreas
        for area_name, area in search_areas:
            for link in area.find_all('a', href=True):
                href = link['href']
                
                # Normalizar URL (resolver relativos)
                absolute_url = urljoin(page_url, href)
                parsed_link = urlparse(absolute_url)
                
                # Verificar que el enlace pertenece al mismo dominio y al wiki
                is_same_domain = parsed_link.netloc == parsed_url.netloc
                is_wiki_path = '/-/wikis/' in absolute_url
                
                if is_same_domain and is_wiki_path:
                    # Extraer el nombre de la página
                    wiki_page = None
                    
                    # Intentar obtener del atributo data-wiki-page (más confiable)
                    if link.get('data-wiki-page'):
                        wiki_page = link.get('data-wiki-page')
                    else:
                        # Extraer del path de la URL
                        wiki_path = absolute_url.split('/-/wikis/')[-1]
                        # Limpiar parámetros y fragmentos
                        wiki_page = wiki_path.split('#')[0].split('?')[0].strip()
                    
                    # URL decode (por si hay caracteres especiales)
                    if wiki_page:
                        wiki_page = unquote(wiki_page)
                        wiki_page = wiki_page.strip('/')
                        
                        # Validar que no es vacío y no es el mismo que ya estamos procesando
                        if wiki_page and wiki_page not in ['', '#'] and wiki_page != page_name:
                            if wiki_page not in downloaded_pages and wiki_page not in pages_to_download:
                                links_found.add(wiki_page)
                                pages_to_download.append(wiki_page)
                                logger.debug(f"  Nuevo enlace encontrado en {area_name}: {wiki_page}")
        
        if links_found:
            logger.info(f"  → {len(links_found)} páginas nuevas encontradas: {', '.join(sorted(list(links_found)[:5]))}{'...' if len(links_found) > 5 else ''}")
    
    # Guardar metadatos de la descarga
    logger.info("\n" + "="*60)
    logger.info("Guardando metadatos de la descarga...")
    
    # 1. Manifest completo
    manifest = {
        'download_timestamp': datetime.now().isoformat(),
        'base_url': base_url,
        'wiki_base': wiki_base,
        'domain': domain,
        'total_pages': len(downloaded_pages),
        'pages': sorted(list(downloaded_pages)),
        'output_directory': str(output_path),
        'rate_limit': rate_limit,
        'max_retries': max_retries,
        'respect_existing': respect_existing
    }
    
    manifest_file = metadata_dir / 'manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ Manifest guardado: {manifest_file}")
    
    # 2. Log estructurado (append para mantener histórico)
    log_file = metadata_dir / 'download_log.jsonl'
    with open(log_file, 'a', encoding='utf-8') as f:
        for entry in download_log:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    logger.info(f"✓ Log de descarga guardado: {log_file} ({len(download_log)} entradas)")
    
    # 3. Checksums actualizados
    with open(checksums_file, 'w', encoding='utf-8') as f:
        json.dump(existing_checksums, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ Checksums guardados: {checksums_file} ({len(existing_checksums)} páginas)")
    
    # 4. README de metadatos
    readme_file = metadata_dir / 'README.md'
    readme_content = f"""# Metadatos de Descarga - Wiki Datascope

## Última Descarga
- **Fecha**: {manifest['download_timestamp']}
- **URL Base**: {base_url}
- **Total Páginas**: {len(downloaded_pages)}

## Archivos de Metadatos

### `manifest.json`
Inventario completo de la descarga incluyendo:
- Timestamp de descarga
- URLs base
- Lista completa de páginas descargadas
- Configuración utilizada

### `download_log.jsonl`
Log estructurado en formato JSON Lines con una entrada por cada operación de descarga:
- Timestamp
- Página descargada
- URL completa
- Status HTTP
- Tamaño del contenido
- SHA256 checksum
- Número de intento
- Resultado (éxito/fallo)

**Nota**: Este archivo es append-only para mantener histórico completo.

### `page_checksums.json`
Checksums SHA256 de cada página para:
- Detección de cambios entre ejecuciones
- Validación de integridad
- Optimización (evitar re-descargas innecesarias)

## Reproducibilidad

Para reproducir esta descarga exacta:
```bash
python main.py
```

La configuración está documentada en el manifest y el código usa parámetros deterministas.

## Trazabilidad

Todos los archivos HTML descargados pueden ser verificados contra los checksums.
El log completo permite auditar cada operación realizada.
"""
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    logger.info(f"✓ README de metadatos creado: {readme_file}")
    
    logger.info("="*60)
    logger.info(f"✓ Descarga completada exitosamente")
    logger.info(f"  Total de páginas: {len(downloaded_pages)}")
    logger.info(f"  Directorio: {output_path}")
    logger.info(f"  Metadatos: {metadata_dir}")
    logger.info("="*60)
    
    return pages_content


def filter_useful_pages(
    useful_pages_file: str = "pags_descarte.txt",
    source_dir: str = "data/wiki_html",
    output_dir: str = "data/wiki_work_html"
) -> Dict[str, str]:
    """
    Filtra y copia los archivos HTML excluyendo los que están en pags_descarte.txt.
    
    Esta función copia TODAS las páginas HTML del directorio fuente EXCEPTO las que
    están listadas en pags_descarte.txt. La página "Overview" siempre se incluye, incluso
    si está en la lista de exclusión.
    
    Args:
        useful_pages_file: Archivo de texto con los nombres de páginas a EXCLUIR (uno por línea)
        source_dir: Directorio donde están los HTML descargados
        output_dir: Directorio donde guardar los HTML filtrados
    
    Returns:
        Diccionario con el nombre de la página como clave y el contenido HTML como valor
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Leer la lista de páginas a excluir
    excluded_pages = set()
    try:
        with open(useful_pages_file, 'r', encoding='utf-8') as f:
            for line in f:
                page_name = line.strip()
                if page_name:  # Ignorar líneas vacías
                    excluded_pages.add(page_name)
        print(f"Páginas a excluir leídas: {len(excluded_pages)}")
    except FileNotFoundError:
        print(f"⚠ Advertencia: No se encontró el archivo {useful_pages_file}")
        print("  Se procesarán todas las páginas disponibles")
        excluded_pages = set()
    
    # Obtener todos los archivos HTML en el directorio fuente
    if not os.path.exists(source_dir):
        print(f"Error: No se encontró el directorio {source_dir}")
        return {}
    
    all_html_files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
    all_pages = {f.replace('.html', '') for f in all_html_files}
    
    # Filtrar páginas: incluir todas EXCEPTO las que están en excluded_pages
    # Pero siempre incluir Overview aunque esté en excluded_pages
    pages_to_include = all_pages - excluded_pages
    pages_to_include.add('Overview')  # Overview siempre se incluye
    
    print(f"\nFiltrando páginas desde {source_dir}...")
    print(f"  - Total de páginas disponibles: {len(all_pages)}")
    print(f"  - Páginas a excluir: {len(excluded_pages)}")
    print(f"  - Páginas que se incluirán: {len(pages_to_include)}")
    
    # Copiar los archivos que deben incluirse
    filtered_pages: Dict[str, str] = {}
    copied_count = 0
    skipped_count = 0
    
    for page_name in sorted(pages_to_include):
        source_file = os.path.join(source_dir, f"{page_name}.html")
        output_file = os.path.join(output_dir, f"{page_name}.html")
        
        if os.path.exists(source_file):
            # Copiar el archivo
            shutil.copy2(source_file, output_file)
            
            # Leer el contenido para devolverlo
            with open(source_file, 'r', encoding='utf-8') as f:
                filtered_pages[page_name] = f.read()
            
            copied_count += 1
            print(f"  ✓ Incluido: {page_name}")
        else:
            skipped_count += 1
            print(f"  ⚠ No encontrado (será omitido): {page_name}")
    
    # Mostrar páginas excluidas
    excluded_but_found = excluded_pages & all_pages
    if excluded_but_found:
        print(f"\n  Páginas excluidas: {', '.join(sorted(excluded_but_found))}")
    
    print(f"\nFiltrado completado:")
    print(f"  - Páginas incluidas: {copied_count}")
    print(f"  - Páginas excluidas: {len(excluded_but_found)}")
    print(f"  - Total guardado en: {output_dir}")
    
    return filtered_pages


def download_linked_pages(
    markdown_dir: str = "data/wiki_markdown",
    output_dir: str = "data/wiki_html",
    base_url: str = "https://gitlab.com/dsc-clinic/datascope/-/wikis"
) -> Dict[str, str]:
    """
    Lee los archivos markdown y descarga los HTML de las páginas referenciadas.
    
    Args:
        markdown_dir: Directorio donde están los archivos markdown
        output_dir: Directorio donde guardar los archivos HTML descargados
        base_url: URL base de la wiki (sin el nombre de la página)
    
    Returns:
        Diccionario con el nombre de la página como clave y el contenido HTML como valor
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtener todos los archivos markdown
    if not os.path.exists(markdown_dir):
        print(f"Error: No se encontró el directorio {markdown_dir}")
        return {}
    
    md_files = [f for f in os.listdir(markdown_dir) if f.endswith('.md')]
    
    if not md_files:
        print(f"No se encontraron archivos markdown en {markdown_dir}")
        return {}
    
    # Extraer todos los enlaces a páginas de la wiki de los markdown
    wiki_links = set()
    
    print(f"Leyendo archivos markdown desde {markdown_dir}...")
    
    # Patrón regex para encontrar enlaces markdown a páginas de la wiki
    # Formato: [texto](url "título opcional") donde url contiene /wikis/nombre-pagina
    # El regex captura la URL hasta antes de las comillas o el paréntesis de cierre
    wiki_link_pattern = re.compile(
        r'\[([^\]]+)\]\(([^"\)]+)',  # Captura [texto](url sin comillas ni paréntesis de cierre)
        re.IGNORECASE
    )
    
    for md_file in md_files:
        md_path = os.path.join(markdown_dir, md_file)
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar todos los enlaces
            matches = wiki_link_pattern.findall(content)
            
            for link_text, link_url in matches:
                # Limpiar espacios al inicio y final
                link_url = link_url.strip()
                
                # Verificar si es un enlace a una página de la wiki
                if '/wikis/' in link_url:
                    # Extraer el nombre de la página
                    # Formato: https://gitlab.com/.../-/wikis/Nombre-Pagina#fragmento?params
                    # Extraer la parte después de /-/wikis/
                    wiki_path = link_url.split('/-/wikis/')[-1]
                    # Limpiar fragmentos y parámetros
                    page_name = wiki_path.split('#')[0].split('?')[0].strip()
                    
                    if page_name:
                        wiki_links.add(page_name)
            
        except Exception as e:
            print(f"  ⚠ Error al leer {md_file}: {e}")
            continue
    
    print(f"  ✓ Encontrados {len(wiki_links)} enlaces únicos a páginas de la wiki")
    
    if not wiki_links:
        print("No se encontraron enlaces a páginas de la wiki")
        return {}
    
    # Verificar qué páginas ya están descargadas
    existing_pages = set()
    if os.path.exists(output_dir):
        existing_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
        existing_pages = {f.replace('.html', '') for f in existing_files}
    
    # Filtrar páginas que ya están descargadas
    pages_to_download = wiki_links - existing_pages
    
    if not pages_to_download:
        print(f"\nTodas las páginas referenciadas ya están descargadas ({len(wiki_links)} páginas)")
        return {}
    
    print(f"\nDescargando {len(pages_to_download)} páginas nuevas...")
    print(f"  (Omitiendo {len(existing_pages)} páginas ya descargadas)")
    
    # Headers para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    downloaded_pages: Dict[str, str] = {}
    success_count = 0
    error_count = 0
    
    for page_name in sorted(pages_to_download):
        page_url = f"{base_url}/{page_name}"
        
        try:
            print(f"  Descargando: {page_name}...")
            response = requests.get(page_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parsear el HTML para extraer información de la API
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar el elemento con data-content-api que contiene la URL de la API
            wiki_app = soup.find('div', {'id': 'js-vue-wiki-app'})
            api_url = None
            
            if wiki_app:
                api_url = wiki_app.get('data-content-api')
            
            # Si encontramos la URL de la API, obtener el contenido desde ahí
            if api_url:
                try:
                    # La URL de la API puede ser relativa, convertirla a absoluta si es necesario
                    if api_url.startswith('/'):
                        parsed_base = urlparse(page_url)
                        api_url = f"{parsed_base.scheme}://{parsed_base.netloc}{api_url}"
                    
                    print(f"    Obteniendo contenido desde API...")
                    api_response = requests.get(api_url, headers=headers, timeout=30)
                    api_response.raise_for_status()
                    api_data = api_response.json()
                    
                    # El contenido está en el campo 'content' del JSON
                    # Reemplazar el contenido del HTML con el contenido real de la API
                    if 'content' in api_data:
                        # Buscar el div donde debería estar el contenido y reemplazarlo
                        # O crear un HTML más simple con el contenido real
                        content_markdown = api_data['content']
                        
                        # Crear un HTML estructurado con el contenido real
                        # Buscar el contenedor del contenido en el HTML original
                        content_container = soup.find('div', class_='wiki-page-details') or soup.find('main')
                        
                        if content_container:
                            # Limpiar el contenido existente y añadir el contenido real
                            # Por ahora, inyectamos el contenido markdown en un div específico
                            new_content_div = soup.new_tag('div', class_='wiki-content-real')
                            new_content_div.string = content_markdown
                            content_container.insert(0, new_content_div)
                            html_content = str(soup)
                        else:
                            # Si no encontramos el contenedor, usar el HTML original
                            html_content = response.text
                    else:
                        html_content = response.text
                except Exception as api_error:
                    print(f"    ⚠ No se pudo obtener contenido desde API: {api_error}")
                    # Continuar con el HTML normal
                    html_content = response.text
            else:
                # Si no hay API URL, usar el HTML normal
                html_content = response.text
            
            # Guardar HTML en archivo
            file_path = os.path.join(output_dir, f"{page_name}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            downloaded_pages[page_name] = html_content
            success_count += 1
            
            # Pequeña pausa para no sobrecargar el servidor
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"  ✗ Error al descargar {page_name}: {e}")
            continue
    
    print(f"\nDescarga completada:")
    print(f"  - Páginas descargadas: {success_count}")
    print(f"  - Errores: {error_count}")
    print(f"  - Total guardado en: {output_dir}")
    
    return downloaded_pages

