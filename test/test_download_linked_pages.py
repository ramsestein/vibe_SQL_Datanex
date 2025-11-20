"""
Paso 4 del pipeline: Descarga de páginas referenciadas en markdown.
Ejecuta la función download_linked_pages con los archivos reales.
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import download_linked_pages


def test_download_linked_pages():
    """Paso 4: Descarga las páginas referenciadas en los archivos markdown."""
    print("="*60)
    print("PASO 4: Descarga de páginas referenciadas en markdown")
    print("="*60)
    
    # Directorios reales del pipeline
    markdown_dir = "data/wiki_markdown"
    output_dir = "data/wiki_html"
    base_url = "https://gitlab.com/dsc-clinic/datascope/-/wikis"
    
    # Verificar que existe el directorio de markdown
    if not os.path.exists(markdown_dir):
        print(f"\n✗ ERROR: No se encontró {markdown_dir}")
        print("   Necesitas ejecutar primero el paso 3 (test_extract_text.py)")
        return False
    
    try:
        print(f"\nLeyendo markdown desde: {markdown_dir}")
        print(f"Descargando HTML en: {output_dir}")
        print(f"URL base: {base_url}")
        
        # Ejecutar la función
        downloaded_pages = download_linked_pages(
            markdown_dir=markdown_dir,
            output_dir=output_dir,
            base_url=base_url
        )
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        # Verificar que el directorio de salida existe
        if os.path.exists(output_dir):
            html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
            print(f"✓ Directorio {output_dir} existe con {len(html_files)} archivos HTML")
            
            # Mostrar páginas descargadas
            if downloaded_pages:
                print("\n" + "-"*60)
                print("PÁGINAS DESCARGADAS:")
                print("-"*60)
                for page_name in sorted(downloaded_pages.keys()):
                    file_path = os.path.join(output_dir, f"{page_name}.html")
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f"  - {page_name} ({file_size:,} bytes)")
        else:
            print(f"⚠ El directorio {output_dir} no existe")
        
        print("\n" + "="*60)
        print("✓ PASO 4 COMPLETADO")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_download_linked_pages()
    sys.exit(0 if success else 1)

