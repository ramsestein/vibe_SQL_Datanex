"""
Script principal para descargar y procesar la wiki de Datanex.
"""

from src import download_wiki_pages, filter_useful_pages, extract_text, download_linked_pages, unify_markdowns, unify_dictionaries, create_final_output


def main():
    """Función principal que orquesta la descarga de la wiki."""
    wiki_url = "https://gitlab.com/dsc-clinic/datascope/-/wikis/Overview"
    output_directory = "data/wiki_html"
    useful_pages_file = "pags_descarte.txt"
    work_output_directory = "data/wiki_work_html"
    
    # Paso 1: Descargar solo Overview
    print("="*60)
    print("PASO 1: Descarga del Overview")
    print("="*60)
    print("Iniciando descarga del Overview de Datanex...")
    pages = download_wiki_pages(wiki_url, output_directory)
    
    print(f"\nPáginas descargadas exitosamente:")
    for page_name in sorted(pages.keys()):
        print(f"  - {page_name}")
    
    # Paso 2: Crear markdown de Overview
    print("\n" + "="*60)
    print("PASO 2: Extracción a Markdown del Overview")
    print("="*60)
    
    overview_markdown = extract_text(
        source_dir=output_directory,
        output_dir="data/wiki_markdown"
    )
    
    print(f"\nMarkdown del Overview guardado en data/wiki_markdown:")
    for page_name in sorted(overview_markdown.keys()):
        print(f"  - {page_name}.md")
    
    # Paso 3: Descargar todas las páginas referenciadas en Overview.md
    print("\n" + "="*60)
    print("PASO 3: Descarga de páginas referenciadas en Overview")
    print("="*60)
    
    linked_pages = download_linked_pages(
        markdown_dir="data/wiki_markdown",
        output_dir=output_directory,
        base_url="https://gitlab.com/dsc-clinic/datascope/-/wikis"
    )
    
    print(f"\nPáginas referenciadas descargadas en {output_directory}:")
    for page_name in sorted(linked_pages.keys()):
        print(f"  - {page_name}.html")
    
    # Paso 4: Filtrar páginas (excluyendo las listadas en pags_descarte.txt)
    print("\n" + "="*60)
    print("PASO 4: Filtrado de páginas útiles")
    print("="*60)
    print("(Excluyendo las páginas listadas en pags_descarte.txt)")
    
    useful_pages = filter_useful_pages(
        useful_pages_file=useful_pages_file,
        source_dir=output_directory,
        output_dir=work_output_directory
    )
    
    print(f"\nPáginas incluidas guardadas en {work_output_directory}:")
    for page_name in sorted(useful_pages.keys()):
        print(f"  - {page_name}")
    
    # Paso 5: Crear markdowns solo de las páginas útiles
    print("\n" + "="*60)
    print("PASO 5: Extracción a Markdown de páginas útiles")
    print("="*60)
    
    markdown_pages = extract_text(
        source_dir=work_output_directory,
        output_dir="data/wiki_markdown"
    )
    
    print(f"\nMarkdowns guardados en data/wiki_markdown:")
    for page_name in sorted(markdown_pages.keys()):
        print(f"  - {page_name}.md")
    
    # Paso 6: Unificar todos los markdowns
    print("\n" + "="*60)
    print("PASO 6: Unificación de todos los markdowns")
    print("="*60)
    
    unified_file = unify_markdowns(
        markdown_dir="data/wiki_markdown",
        output_file="data/wiki_unified.md"
    )
    
    if unified_file:
        print(f"\n✓ Archivo unificado creado: {unified_file}")
    else:
        print("\n⚠ No se pudo crear el archivo unificado")
    
    # Paso 7: Unificar diccionarios CSV
    print("\n" + "="*60)
    print("PASO 7: Unificación de diccionarios CSV")
    print("="*60)
    
    dictionaries_file = unify_dictionaries(
        dicc_dir="dicc",
        output_file="dicc/dictionaries_unified.md"
    )
    
    if dictionaries_file:
        print(f"\n✓ Archivo de diccionarios unificado creado: {dictionaries_file}")
    else:
        print("\n⚠ No se pudo crear el archivo de diccionarios unificado")
    
    # Paso 8: Crear archivo final
    print("\n" + "="*60)
    print("PASO 8: Creación del archivo final")
    print("="*60)
    
    final_file = create_final_output(
        prompt_file="prompt.txt",
        wiki_unified_file="data/wiki_unified.md",
        dictionaries_file="dicc/dictionaries_unified.md",
        output_file="vibe_SQL_copilot.txt"
    )
    
    if final_file:
        print(f"\n✓ Archivo final creado: {final_file}")
    else:
        print("\n⚠ No se pudo crear el archivo final")    

if __name__ == "__main__":
    main()

