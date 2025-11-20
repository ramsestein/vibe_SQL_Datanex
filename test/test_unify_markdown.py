"""
Paso 5 del pipeline: Unificación de markdowns.
Ejecuta la función unify_markdowns con los archivos reales.
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import unify_markdowns


def test_unify_markdown():
    """Paso 5: Unifica todos los markdowns en un solo archivo."""
    print("="*60)
    print("PASO 5: Unificación de markdowns")
    print("="*60)
    
    # Directorios reales del pipeline
    markdown_dir = "data/wiki_markdown"
    output_file = "data/wiki_unified.md"
    
    # Verificar que existe el directorio de markdown
    if not os.path.exists(markdown_dir):
        print(f"\n✗ ERROR: No se encontró {markdown_dir}")
        print("   Necesitas ejecutar primero el paso 3 (test_extract_text.py)")
        return False
    
    try:
        print(f"\nUnificando markdown desde: {markdown_dir}")
        print(f"Archivo de salida: {output_file}")
        
        # Ejecutar la función
        result_file = unify_markdowns(
            markdown_dir=markdown_dir,
            output_file=output_file
        )
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        if result_file and os.path.exists(result_file):
            file_size = os.path.getsize(result_file)
            print(f"✓ Archivo unificado creado: {result_file}")
            print(f"✓ Tamaño: {file_size:,} bytes")
            
            # Verificar que no contiene "## Wiki Pages"
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '## Wiki Pages' in content or '## Wiki pages' in content:
                    print("⚠ ADVERTENCIA: El archivo aún contiene la sección 'Wiki Pages'")
                else:
                    print("✓ Sección 'Wiki Pages' eliminada correctamente")
        else:
            print(f"⚠ El archivo {output_file} no se creó")
        
        print("\n" + "="*60)
        print("✓ PASO 5 COMPLETADO")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_unify_markdown()
    sys.exit(0 if success else 1)

