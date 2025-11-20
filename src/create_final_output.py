"""
Script para crear el archivo final combinando prompt.txt y wiki_unified.md.
"""

import os


def create_final_output(
    prompt_file: str = "prompt.txt",
    wiki_unified_file: str = "data/wiki_unified.md",
    output_file: str = "vibe_SQL_copilot.txt"
) -> str:
    """
    Crea el archivo final combinando el prompt y el contenido unificado de la wiki.
    
    Args:
        prompt_file: Archivo con el prompt inicial
        wiki_unified_file: Archivo markdown unificado de la wiki
        output_file: Archivo de salida final
    
    Returns:
        Ruta del archivo generado
    """
    # Verificar que existen los archivos de entrada
    if not os.path.exists(prompt_file):
        print(f"Error: No se encontró el archivo {prompt_file}")
        return ""
    
    if not os.path.exists(wiki_unified_file):
        print(f"Error: No se encontró el archivo {wiki_unified_file}")
        return ""
    
    print(f"Creando archivo final combinando:")
    print(f"  - {prompt_file}")
    print(f"  - {wiki_unified_file}")
    print(f"  -> {output_file}")
    
    # Leer el contenido del prompt
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
    except Exception as e:
        print(f"Error al leer {prompt_file}: {e}")
        return ""
    
    # Leer el contenido del markdown unificado
    try:
        with open(wiki_unified_file, 'r', encoding='utf-8') as f:
            wiki_content = f.read()
    except Exception as e:
        print(f"Error al leer {wiki_unified_file}: {e}")
        return ""
    
    # Combinar ambos contenidos
    final_content = prompt_content.strip() + '\n\n' + wiki_content.strip()
    
    # Guardar el archivo final
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        file_size = os.path.getsize(output_file)
        
        print(f"\nArchivo final creado:")
        print(f"  - Archivo: {output_file}")
        print(f"  - Tamaño: {file_size:,} bytes")
        
        return output_file
        
    except Exception as e:
        print(f"Error al escribir {output_file}: {e}")
        return ""

