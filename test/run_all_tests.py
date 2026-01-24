"""
Script para ejecutar todos los pasos del pipeline.
Ejecuta los cinco pasos en secuencia: descarga, filtrado, extracción, unificación y creación del archivo final.
Versión 2.1: Pipeline simplificado sin diccionarios.
"""

import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test_download_wiki import test_download_wiki_pages
from test_filter_useful_pages import test_filter_useful_pages
from test_extract_text import test_extract_text
from test_download_linked_pages import test_download_linked_pages
from test_unify_markdown import test_unify_markdown
from test_create_final_output import test_create_final_output


def main():
    """Ejecuta todos los pasos del pipeline en secuencia."""
    print("\n" + "="*60)
    print("EJECUTANDO PIPELINE COMPLETO (v2.1 - Sin diccionarios)")
    print("="*60 + "\n")
    
    steps = [
        ("Paso 1: Descarga de wiki", test_download_wiki_pages),
        ("Paso 2: Filtrado de páginas útiles", test_filter_useful_pages),
        ("Paso 3: Extracción a Markdown", test_extract_text),
        ("Paso 4: Descarga de páginas referenciadas", test_download_linked_pages),
        ("Paso 5: Unificación de markdowns", test_unify_markdown),
        ("Paso 6: Creación del archivo final", test_create_final_output),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            success = step_func()
            results.append((step_name, success))
            
            # Si un paso falla, no continuar con los siguientes
            if not success:
                print(f"\n⚠ El {step_name} falló. Deteniendo el pipeline.")
                break
                
        except Exception as e:
            print(f"\n✗ ERROR al ejecutar {step_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((step_name, False))
            break
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DEL PIPELINE")
    print("="*60)
    
    completed = sum(1 for _, success in results if success)
    total = len(results)
    
    for step_name, success in results:
        status = "✓ COMPLETADO" if success else "✗ FALLIDO"
        print(f"  {status}: {step_name}")
    
    print(f"\nPasos completados: {completed}/{total}")
    
    if completed == total:
        print("\n✓ PIPELINE COMPLETADO EXITOSAMENTE")
        return 0
    else:
        print(f"\n✗ PIPELINE DETENIDO: {total - completed} paso(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())

