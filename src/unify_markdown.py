"""
Script para unificar todos los archivos markdown en uno solo.
"""

import os
import re
from typing import Dict
from bs4 import BeautifulSoup


def convert_html_tables_to_markdown(content: str) -> str:
    """
    Convierte tablas HTML a formato markdown.
    
    Args:
        content: Contenido markdown que puede contener tablas HTML
    
    Returns:
        Contenido con tablas convertidas a markdown
    """
    # Buscar todas las tablas HTML en el contenido
    table_pattern = re.compile(
        r'<table>.*?</table>',
        re.DOTALL | re.IGNORECASE
    )
    
    def replace_table(match):
        table_html = match.group(0)
        soup = BeautifulSoup(table_html, 'html.parser')
        table = soup.find('table')
        
        if not table:
            return table_html
        
        # Extraer filas
        rows = []
        for tr in table.find_all('tr'):
            cells = []
            for cell in tr.find_all(['th', 'td']):
                # Extraer texto de la celda, preservando saltos de línea
                cell_text = cell.get_text(separator=' ', strip=True)
                # Limpiar espacios múltiples
                cell_text = ' '.join(cell_text.split())
                cells.append(cell_text)
            if cells:
                rows.append(cells)
        
        if not rows:
            return table_html
        
        # Convertir a markdown
        markdown_lines = []
        
        # Primera fila es el encabezado
        if rows:
            header = rows[0]
            markdown_lines.append('| ' + ' | '.join(header) + ' |')
            # Separador
            markdown_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
            # Resto de filas
            for row in rows[1:]:
                # Asegurar que todas las filas tengan el mismo número de columnas
                while len(row) < len(header):
                    row.append('')
                markdown_lines.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(markdown_lines)
    
    # Reemplazar todas las tablas HTML
    content = table_pattern.sub(replace_table, content)
    
    return content


def unify_markdowns(
    markdown_dir: str = "data/wiki_markdown",
    output_file: str = "data/wiki_unified.md",
    excluded_pages_file: str = "pags_descarte.txt"
) -> str:
    """
    Unifica todos los archivos markdown en un solo archivo, eliminando la sección "Wiki Pages".
    Excluye las páginas listadas en pags_descarte.txt.
    
    Args:
        markdown_dir: Directorio donde están los archivos markdown
        output_file: Archivo de salida donde guardar el markdown unificado
        excluded_pages_file: Archivo con la lista de páginas a excluir
    
    Returns:
        Ruta del archivo generado
    """
    # Leer la lista de páginas a excluir
    excluded_pages = set()
    if os.path.exists(excluded_pages_file):
        try:
            with open(excluded_pages_file, 'r', encoding='utf-8') as f:
                for line in f:
                    page_name = line.strip()
                    if page_name:  # Ignorar líneas vacías
                        excluded_pages.add(page_name)
        except Exception as e:
            print(f"[WARN] Advertencia: No se pudo leer {excluded_pages_file}: {e}")
    
    # Obtener todos los archivos markdown
    if not os.path.exists(markdown_dir):
        print(f"Error: No se encontró el directorio {markdown_dir}")
        return ""
    
    all_md_files = [f for f in os.listdir(markdown_dir) if f.endswith('.md')]
    
    # Filtrar archivos excluidos
    md_files = []
    excluded_count = 0
    for md_file in all_md_files:
        page_name = md_file.replace('.md', '')
        if page_name not in excluded_pages:
            md_files.append(md_file)
        else:
            excluded_count += 1
    
    if not md_files:
        print(f"No se encontraron archivos markdown para unificar en {markdown_dir}")
        return ""
    
    print(f"Unificando {len(md_files)} archivos markdown desde {markdown_dir}...")
    if excluded_count > 0:
        print(f"  (Excluyendo {excluded_count} archivos según {excluded_pages_file})")
    
    unified_content = []
    processed_count = 0
    
    for md_file in sorted(md_files):
        md_path = os.path.join(markdown_dir, md_file)
        page_name = md_file.replace('.md', '')
        
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar la línea que contiene "Quick reference")" (fin de la sección Wiki Pages)
            lines = content.split('\n')
            start_idx = None
            
            # Encontrar el final de la sección Wiki Pages (línea con "Quick reference")")
            for i, line in enumerate(lines):
                if '"Quick reference")' in line or '"Quick reference"' in line:
                    start_idx = i + 1  # Empezar desde la línea siguiente
                    break
            
            if start_idx is None:
                # Si no se encuentra "Quick reference")", buscar "The g" como fallback
                for i, line in enumerate(lines):
                    if 'The g' in line:
                        start_idx = i
                        break
                
                if start_idx is None:
                    # Si no se encuentra nada, mantener todo el contenido
                    content_cleaned = content
                else:
                    # Tomar solo desde "The g" en adelante
                    content_cleaned = '\n'.join(lines[start_idx:])
            else:
                # Tomar solo desde después de "Quick reference")" en adelante
                content_cleaned = '\n'.join(lines[start_idx:])
            
            # Eliminar todo lo que esté después de "##" (sección Wiki Pages u otras secciones no deseadas)
            # Buscar la primera línea que empiece con "##" y eliminar desde ahí
            cleaned_lines = []
            for line in content_cleaned.split('\n'):
                # Si encontramos una línea que empiece con "##", detener
                if line.strip().startswith('##'):
                    break  # Detener aquí, no incluir esta línea ni las siguientes
                cleaned_lines.append(line)
            
            content_cleaned = '\n'.join(cleaned_lines)
            
            # Convertir tablas HTML a formato markdown
            content_cleaned = convert_html_tables_to_markdown(content_cleaned)
            
            # Limpiar líneas vacías excesivas al inicio y final
            content_cleaned = content_cleaned.strip()
            
            # Añadir separador entre páginas
            if unified_content:
                unified_content.append('\n\n---\n\n')
            
            # Añadir el contenido de esta página
            unified_content.append(content_cleaned)
            
            processed_count += 1
            print(f"  [OK] Procesado: {page_name}")
            
        except Exception as e:
            print(f"  [FAIL] Error al procesar {md_file}: {e}")
            continue
    
    # Unificar todo el contenido
    final_content = '\n'.join(unified_content)
    
    # Limpiar saltos de línea dobles: si hay 2 o más seguidos, dejar solo 1
    final_content = re.sub(r'\n{2,}', '\n', final_content)
    
    # Limpiar líneas vacías al inicio y final
    final_content = final_content.strip()
    
    # Guardar el archivo unificado
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    file_size = os.path.getsize(output_file)
    
    print(f"\nUnificación completada:")
    print(f"  - Archivos procesados: {processed_count}")
    print(f"  - Archivo generado: {output_file}")
    print(f"  - Tamaño: {file_size:,} bytes")
    
    return output_file

