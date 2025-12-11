"""
Script para descargar todas las páginas de una wiki de GitLab.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import time
import shutil
import re
from copy import copy
from typing import Set, List, Dict


def download_wiki_pages(base_url: str, output_dir: str = "data/wiki_html") -> Dict[str, str]:
    """
    Descarga todas las páginas de una wiki de GitLab.
    
    Args:
        base_url: URL base de la wiki (ej: https://gitlab.com/dsc-clinic/datascope/-/wikis/Overview)
        output_dir: Directorio donde guardar los archivos HTML descargados
    
    Returns:
        Diccionario con el nombre de la página como clave y el contenido HTML como valor
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Extraer la URL base del proyecto (sin el nombre de la página)
    parsed_url = urlparse(base_url)
    wiki_base = f"{parsed_url.scheme}://{parsed_url.netloc}{'/'.join(parsed_url.path.split('/')[:-1])}"
    
    # Conjunto para rastrear páginas ya descargadas
    downloaded_pages: Set[str] = set()
    pages_to_download: List[str] = []
    pages_content: Dict[str, str] = {}
    
    # Empezar con la página inicial
    initial_page = base_url.split('/')[-1] if '/' in base_url else 'Overview'
    pages_to_download.append(initial_page)
    
    # Headers para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Descargando páginas de la wiki desde: {wiki_base}")
    
    while pages_to_download:
        page_name = pages_to_download.pop(0)
        
        if page_name in downloaded_pages:
            continue
        
        # Construir URL de la página
        page_url = f"{wiki_base}/{page_name}"
        
        try:
            print(f"Descargando: {page_name}...")
            response = requests.get(page_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Guardar HTML en archivo
            html_content = response.text
            file_path = os.path.join(output_dir, f"{page_name}.html")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            pages_content[page_name] = html_content
            downloaded_pages.add(page_name)
            
            # Parsear HTML para encontrar enlaces a otras páginas de la wiki
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar el contenido principal de la página (excluyendo el sidebar)
            # El sidebar suele estar en div.wiki-sidebar-custom-content o aside
            main_content = None
            
            # Intentar encontrar el contenido principal excluyendo el sidebar
            for selector in ['div.wiki-page-details', 'article', 'main', 'div.content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            # Si no se encuentra, usar el body pero excluir el sidebar
            if not main_content:
                body = soup.find('body')
                if body:
                    # Excluir el sidebar
                    sidebar = body.find('aside') or body.find(class_='wiki-sidebar')
                    if sidebar:
                        # Crear una copia del body sin el sidebar
                        main_content = copy(body)
                        if sidebar in main_content:
                            sidebar.decompose()
                    else:
                        main_content = body
                else:
                    main_content = soup
            
            # Buscar enlaces a otras páginas de la wiki SOLO en el contenido principal
            # Los enlaces de wiki de GitLab suelen tener el formato /-/wikis/nombre-pagina
            # y tienen el atributo data-wiki-page o la clase gfm-wiki_page
            links_found = set()
            
            if main_content:
                for link in main_content.find_all('a', href=True):
                    href = link['href']
                    
                    # Verificar si es un enlace a otra página de la wiki
                    # Buscar enlaces que tengan data-wiki-page o sean de tipo wiki_page
                    is_wiki_link = (
                        '/-/wikis/' in href and 
                        (link.get('data-wiki-page') or 
                         'gfm-wiki_page' in link.get('class', []) or
                         link.get('data-reference-type') == 'wiki_page')
                    )
                    
                    if is_wiki_link:
                        # Extraer el nombre de la página del href o del atributo data-wiki-page
                        wiki_page = None
                        
                        # Primero intentar obtener del atributo data-wiki-page
                        if link.get('data-wiki-page'):
                            wiki_page = link.get('data-wiki-page')
                        else:
                            # Si no, extraer del href
                            wiki_path = href.split('/-/wikis/')[-1]
                            # Limpiar parámetros o fragmentos
                            wiki_page = wiki_path.split('#')[0].split('?')[0].strip()
                        
                        if wiki_page and wiki_page not in downloaded_pages and wiki_page not in pages_to_download:
                            links_found.add(wiki_page)
                            pages_to_download.append(wiki_page)
                
                if links_found:
                    print(f"  Encontradas {len(links_found)} páginas relacionadas: {', '.join(sorted(links_found))}")
            
            # Pequeña pausa para no sobrecargar el servidor
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {page_name}: {e}")
            continue
    
    print(f"\nDescarga completada. Total de páginas descargadas: {len(downloaded_pages)}")
    return pages_content


def filter_useful_pages(
    useful_pages_file: str = "pags_utiles.txt",
    source_dir: str = "data/wiki_html",
    output_dir: str = "data/wiki_work_html"
) -> Dict[str, str]:
    """
    Filtra y copia los archivos HTML excluyendo los que están en pags_utiles.txt.
    
    Esta función copia TODAS las páginas HTML del directorio fuente EXCEPTO las que
    están listadas en pags_utiles.txt. La página "Overview" siempre se incluye, incluso
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

