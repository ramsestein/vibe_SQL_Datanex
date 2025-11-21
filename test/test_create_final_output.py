"""
Paso 8 del pipeline: Creación del archivo final.
Ejecuta la función create_final_output con los archivos reales.
"""

import os
import sys

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import create_final_output


def test_create_final_output():
    """Paso 8: Crea el archivo final combinando prompt.txt, wiki_unified.md y dictionaries_unified.md."""
    print("="*60)
    print("PASO 8: Creación del archivo final")
    print("="*60)
    
    # Archivos reales del pipeline
    prompt_file = "prompt.txt"
    wiki_unified_file = "data/wiki_unified.md"
    dictionaries_file = "dicc/dictionaries_unified.md"
    output_file = "vibe_SQL_copilot.txt"
    
    # Verificar que existen los archivos de entrada
    if not os.path.exists(prompt_file):
        print(f"\n✗ ERROR: No se encontró {prompt_file}")
        return False
    
    if not os.path.exists(wiki_unified_file):
        print(f"\n✗ ERROR: No se encontró {wiki_unified_file}")
        print("   Necesitas ejecutar primero el paso 5 (test_unify_markdown.py)")
        return False
    
    if not os.path.exists(dictionaries_file):
        print(f"\n✗ ERROR: No se encontró {dictionaries_file}")
        print("   Necesitas ejecutar primero el paso 6 (test_unify_dictionaries.py)")
        return False
    
    try:
        print(f"\nCombinando archivos:")
        print(f"  - {prompt_file}")
        print(f"  - {wiki_unified_file}")
        print(f"  - {dictionaries_file}")
        print(f"  -> {output_file}")
        
        # Ejecutar la función
        result_file = create_final_output(
            prompt_file=prompt_file,
            wiki_unified_file=wiki_unified_file,
            dictionaries_file=dictionaries_file,
            output_file=output_file
        )
        
        # Verificaciones
        print("\n" + "-"*60)
        print("RESUMEN:")
        print("-"*60)
        
        if result_file and os.path.exists(result_file):
            file_size = os.path.getsize(result_file)
            print(f"✓ Archivo final creado: {result_file}")
            print(f"✓ Tamaño: {file_size:,} bytes")
            
            # Verificar que contiene contenido de ambos archivos
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if prompt_file and os.path.exists(prompt_file):
                    with open(prompt_file, 'r', encoding='utf-8') as pf:
                        prompt_text = pf.read().strip()
                        if prompt_text in content:
                            print("✓ Contiene el contenido de prompt.txt")
                        else:
                            print("⚠ No se encontró el contenido de prompt.txt")
        else:
            print(f"⚠ El archivo {output_file} no se creó")
        
        print("\n" + "="*60)
        print("✓ PASO 8 COMPLETADO")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_create_final_output()
    sys.exit(0 if success else 1)

