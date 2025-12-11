"""
Paso 4 del pipeline: Filtrado de páginas útiles.
Ejecuta la función filter_useful_pages con los archivos reales.
Nota: pags_descarte.txt contiene las páginas a EXCLUIR (descartar).
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import filter_useful_pages


def test_filter_useful_pages():
    """Paso 4: Filtra las páginas excluyendo las listadas en pags_descarte.txt."""
    print("="*60)
    print("PASO 4: Filtrado de páginas útiles")
    print("="*60)
    
    # Directorios reales del pipeline
    source_dir = "data/wiki_html"
    output_dir = "data/wiki_work_html"
    useful_pages_file = "pags_descarte.txt"
    
    # Verificar que existe el archivo de páginas a excluir (es opcional, pero recomendado)
    if not os.path.exists(useful_pages_file):
        print(f"\n⚠ ADVERTENCIA: No se encontró {useful_pages_file}")
        print("   Se procesarán todas las páginas disponibles.")
    
    # Verificar que existe el directorio fuente
    if not os.path.exists(source_dir):
        print(f"\n✗ ERROR: No se encontró {source_dir}")
        print("   Necesitas ejecutar primero el paso 1 (test_download_wiki.py)")
        return False
    
    try:
        print(f"\nFiltrando desde: {source_dir}")
        print(f"Archivo de páginas a excluir: {useful_pages_file}")
        print(f"Directorio de salida: {output_dir}")
        print("(Nota: Se incluirán TODAS las páginas excepto las listadas en el archivo)")
        
        # Ejecutar la función
        filtered_pages = filter_useful_pages(
            useful_pages_file=useful_pages_file,
            source_dir=source_dir,
            output_dir=output_dir
        )
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        # Verificar que el directorio de salida existe
        if os.path.exists(output_dir):
            html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
            print(f"✓ Directorio {output_dir} existe con {len(html_files)} archivos HTML")
            
            # Mostrar páginas filtradas
            print("\n" + "-"*60)
            print("PÁGINAS FILTRADAS:")
            print("-"*60)
            for page_name in sorted(filtered_pages.keys()):
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
    success = test_filter_useful_pages()
    sys.exit(0 if success else 1)

