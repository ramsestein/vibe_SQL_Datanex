"""
Script principal para descargar y procesar la wiki de Datanex.
"""

from src import download_wiki_pages, filter_useful_pages, extract_text, download_linked_pages, unify_markdowns, unify_dictionaries, create_final_output


def main():
    """Función principal que orquesta la descarga de la wiki."""
    wiki_url = "https://gitlab.com/dsc-clinic/datascope/-/wikis/home"
    output_directory = "data/wiki_html"
    useful_pages_file = "pags_descarte.txt"
    work_output_directory = "data/wiki_work_html"
    
    # Paso 1: Descargar desde home (que tiene el menú lateral con todas las páginas)
    print("="*60)
    print("PASO 1: Descarga desde home (menú lateral)")
    print("="*60)
    print("Iniciando descarga desde la página home de Datanex...")
    print("(Scraping responsable: rate limit 2s, reintentos automáticos, validación de integridad)")
    pages = download_wiki_pages(
        base_url=wiki_url,
        output_dir=output_directory,
        rate_limit=2.0,           # 2 segundos entre requests (conservador)
        max_retries=3,            # 3 intentos por página
        respect_existing=True     # No re-descargar sin cambios
    )
    
    print(f"\nPáginas descargadas exitosamente:")
    for page_name in sorted(pages.keys()):
        print(f"  - {page_name}")
    
    # Paso 2: Filtrar páginas (excluyendo las listadas en pags_descarte.txt)
    print("\n" + "="*60)
    print("PASO 2: Filtrado de páginas útiles")
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
    
    # Paso 3: Crear markdowns solo de las páginas útiles
    print("\n" + "="*60)
    print("PASO 3: Extracción a Markdown de páginas útiles")
    print("="*60)
    
    markdown_pages = extract_text(
        source_dir=work_output_directory,
        output_dir="data/wiki_markdown"
    )
    
    print(f"\nMarkdowns guardados en data/wiki_markdown:")
    for page_name in sorted(markdown_pages.keys()):
        print(f"  - {page_name}.md")
    
    # Paso 4: Unificar todos los markdowns
    print("\n" + "="*60)
    print("PASO 4: Unificación de todos los markdowns")
    print("="*60)
    
    unified_file = unify_markdowns(
        markdown_dir="data/wiki_markdown",
        output_file="data/wiki_unified.md",
        excluded_pages_file=useful_pages_file
    )
    
    if unified_file:
        print(f"\n✓ Archivo unificado creado: {unified_file}")
    else:
        print("\n⚠ No se pudo crear el archivo unificado")
    
    # Paso 5: Unificar diccionarios CSV
    print("\n" + "="*60)
    print("PASO 5: Unificación de diccionarios CSV")
    print("="*60)
    
    dictionaries_file = unify_dictionaries(
        dicc_dir="dicc",
        output_file="dicc/dictionaries_unified.md"
    )
    
    if dictionaries_file:
        print(f"\n✓ Archivo de diccionarios unificado creado: {dictionaries_file}")
    else:
        print("\n⚠ No se pudo crear el archivo de diccionarios unificado")
    
    # Paso 6: Crear archivo final
    print("\n" + "="*60)
    print("PASO 6: Creación del archivo final")
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

