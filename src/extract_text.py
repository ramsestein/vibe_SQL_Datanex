"""
Script para extraer texto y convertir HTML a Markdown.
"""

from bs4 import BeautifulSoup
import os
import json
import html
from typing import Dict
from markdownify import markdownify as md


def extract_text(
    source_dir: str = "data/wiki_work_html",
    output_dir: str = "data/wiki_markdown"
) -> Dict[str, str]:
    """
    Extrae el contenido textual y tablas de los archivos HTML y los convierte a Markdown.
    
    Args:
        source_dir: Directorio donde están los archivos HTML
        output_dir: Directorio donde guardar los archivos Markdown
    
    Returns:
        Diccionario con el nombre de la página como clave y el contenido Markdown como valor
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtener todos los archivos HTML del directorio fuente
    html_files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
    
    if not html_files:
        print(f"No se encontraron archivos HTML en {source_dir}")
        return {}
    
    markdown_pages: Dict[str, str] = {}
    converted_count = 0
    error_count = 0
    
    print(f"\nExtrayendo texto y convirtiendo a Markdown desde {source_dir}...")
    
    for html_file in html_files:
        page_name = html_file.replace('.html', '')
        html_path = os.path.join(source_dir, html_file)
        markdown_path = os.path.join(output_dir, f"{page_name}.md")
        
        try:
            # Leer el archivo HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parsear con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            markdown_content = ""
            
            # GitLab wiki tiene el contenido en el atributo data-page-info como JSON
            wiki_app = soup.find('div', attrs={'data-page-info': True})
            
            if wiki_app and wiki_app.get('data-page-info'):
                try:
                    # Extraer y parsear el JSON
                    page_info_json = wiki_app.get('data-page-info')
                    # El JSON está HTML-escapado, necesitamos des-escaparlo
                    page_info_json = html.unescape(page_info_json)
                    page_info = json.loads(page_info_json)
                    
                    # El contenido está en el campo 'content'
                    if 'content' in page_info:
                        markdown_content = page_info['content']
                        # El contenido puede tener \r\n, normalizarlos a \n
                        markdown_content = markdown_content.replace('\r\n', '\n')
                    else:
                        print(f"    [WARN] No se encontró 'content' en data-page-info para {page_name}")
                        
                except json.JSONDecodeError as e:
                    print(f"    [WARN] Error al parsear JSON de data-page-info: {e}")
                except Exception as e:
                    print(f"    [WARN] Error al extraer contenido de data-page-info: {e}")
            
            # Si no se pudo obtener del JSON, intentar fallback
            if not markdown_content:
                print(f"    [INFO] Usando fallback para extraer contenido de {page_name}")
                # Buscar contenido principal tradicional
                for selector in ['div.wiki-content', 'div.wiki', 'article', 'main', 'div.content']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break
                
                if not main_content:
                    main_content = soup.find('body')
                    if not main_content:
                        main_content = soup
                
                markdown_content = md(
                    str(main_content),
                    heading_style="ATX",
                    bullets="-",
                    strip=['script', 'style', 'nav', 'header', 'footer'],
                )
            
            # Limpiar el markdown (eliminar líneas vacías excesivas)
            lines = markdown_content.split('\n')
            cleaned_lines = []
            prev_empty = False
            for line in lines:
                is_empty = not line.strip()
                if not (is_empty and prev_empty):  # No añadir líneas vacías consecutivas
                    cleaned_lines.append(line)
                prev_empty = is_empty
            
            markdown_content = '\n'.join(cleaned_lines).strip()
            
            # Añadir título de la página al inicio
            title = page_name.replace('-', ' ').title()
            markdown_content = f"# {title}\n\n{markdown_content}"
            
            # Guardar el archivo Markdown
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            markdown_pages[page_name] = markdown_content
            converted_count += 1
            print(f"  [OK] Convertido: {page_name}")
            
        except Exception as e:
            error_count += 1
            print(f"  [FAIL] Error al convertir {page_name}: {e}")
            continue
    
    print(f"\nConversión completada:")
    print(f"  - Archivos convertidos: {converted_count}")
    print(f"  - Errores: {error_count}")
    print(f"  - Total guardado en: {output_dir}")
    
    return markdown_pages

