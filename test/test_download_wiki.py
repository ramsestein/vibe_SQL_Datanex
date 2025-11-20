"""
Paso 1 del pipeline: Descarga de páginas de la wiki.
Ejecuta la función download_wiki_pages con los archivos reales.
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import download_wiki_pages


def test_download_wiki_pages():
    """Paso 1: Descarga todas las páginas de la wiki."""
    print("="*60)
    print("PASO 1: Descarga de páginas de la wiki")
    print("="*60)
    
    # URL real de la wiki
    wiki_url = "https://gitlab.com/dsc-clinic/datascope/-/wikis/Overview"
    # Directorio real donde se guardan los archivos
    output_dir = "data/wiki_html"
    
    try:
        print(f"\nDescargando desde: {wiki_url}")
        print(f"Directorio de salida: {output_dir}")
        
        # Ejecutar la función
        pages = download_wiki_pages(wiki_url, output_dir)
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        # Verificar que se descargaron páginas
        if len(pages) > 0:
            print(f"✓ Se descargaron {len(pages)} páginas")
        else:
            print("⚠ No se descargaron páginas")
        
        # Verificar que el directorio existe
        if os.path.exists(output_dir):
            html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
            print(f"✓ Directorio {output_dir} existe con {len(html_files)} archivos HTML")
            
            # Mostrar páginas descargadas
            print("\n" + "-"*60)
            print("PÁGINAS DESCARGADAS:")
            print("-"*60)
            for page_name in sorted(pages.keys()):
                file_path = os.path.join(output_dir, f"{page_name}.html")
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"  - {page_name} ({file_size:,} bytes)")
        else:
            print(f"⚠ El directorio {output_dir} no existe")
        
        print("\n" + "="*60)
        print("✓ PASO 1 COMPLETADO")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_download_wiki_pages()
    sys.exit(0 if success else 1)

