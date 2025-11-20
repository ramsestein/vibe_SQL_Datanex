"""
Paso 3 del pipeline: Extracción de texto a Markdown.
Ejecuta la función extract_text con los archivos reales.
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.extract_text import extract_text


def test_extract_text():
    """Paso 3: Extrae texto y convierte HTML a Markdown."""
    print("="*60)
    print("PASO 3: Extracción de texto a Markdown")
    print("="*60)
    
    # Directorios reales del pipeline
    source_dir = "data/wiki_work_html"
    output_dir = "data/wiki_markdown"
    
    # Verificar que existe el directorio fuente
    if not os.path.exists(source_dir):
        print(f"\n✗ ERROR: No se encontró {source_dir}")
        print("   Necesitas ejecutar primero el paso 2 (test_filter_useful_pages.py)")
        return False
    
    try:
        print(f"\nExtrayendo texto desde: {source_dir}")
        print(f"Directorio de salida: {output_dir}")
        
        # Ejecutar la función
        markdown_pages = extract_text(
            source_dir=source_dir,
            output_dir=output_dir
        )
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        # Verificar que el directorio de salida existe
        if os.path.exists(output_dir):
            md_files = [f for f in os.listdir(output_dir) if f.endswith('.md')]
            print(f"✓ Directorio {output_dir} existe con {len(md_files)} archivos Markdown")
            
            # Mostrar páginas convertidas
            print("\n" + "-"*60)
            print("PÁGINAS CONVERTIDAS A MARKDOWN:")
            print("-"*60)
            for page_name in sorted(markdown_pages.keys()):
                file_path = os.path.join(output_dir, f"{page_name}.md")
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    content_preview = markdown_pages[page_name][:100].replace('\n', ' ')
                    print(f"  - {page_name} ({file_size:,} bytes)")
                    print(f"    Preview: {content_preview}...")
        else:
            print(f"⚠ El directorio {output_dir} no existe")
        
        print("\n" + "="*60)
        print("✓ PASO 3 COMPLETADO")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_extract_text()
    sys.exit(0 if success else 1)

