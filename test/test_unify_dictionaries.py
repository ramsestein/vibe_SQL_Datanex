"""
Test para la función unify_dictionaries.
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.unify_dictionaries import unify_dictionaries


def test_unify_dictionaries():
    """Test para unificar diccionarios CSV en markdown."""
    print("="*60)
    print("TEST: Unificación de diccionarios CSV")
    print("="*60)
    
    dicc_dir = "dicc"
    output_file = "dicc/dictionaries_unified.md"
    
    # Verificar que existe el directorio de diccionarios
    if not os.path.exists(dicc_dir):
        print(f"⚠ El directorio {dicc_dir} no existe")
        return False
    
    # Ejecutar la función
    result = unify_dictionaries(
        dicc_dir=dicc_dir,
        output_file=output_file
    )
    
    # Verificar resultado
    if result and os.path.exists(result):
        print(f"\n✓ Test exitoso: Archivo creado en {result}")
        
        # Verificar contenido básico
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 0:
                print(f"  - Tamaño del archivo: {len(content):,} caracteres")
                print(f"  - Líneas: {len(content.splitlines())}")
                return True
            else:
                print("  ⚠ El archivo está vacío")
                return False
    else:
        print(f"\n✗ Test fallido: No se pudo crear el archivo")
        return False


if __name__ == "__main__":
    success = test_unify_dictionaries()
    sys.exit(0 if success else 1)

