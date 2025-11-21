"""
Script para crear el archivo final combinando prompt.txt y wiki_unified.md.
"""

import os


def create_final_output(
    prompt_file: str = "prompt.txt",
    wiki_unified_file: str = "data/wiki_unified.md",
    dictionaries_file: str = "dicc/dictionaries_unified.md",
    output_file: str = "vibe_SQL_copilot.txt"
) -> str:
    """
    Crea el archivo final combinando el prompt, el contenido unificado de la wiki
    y los diccionarios unificados.
    
    Args:
        prompt_file: Archivo con el prompt inicial
        wiki_unified_file: Archivo markdown unificado de la wiki
        dictionaries_file: Archivo markdown unificado de diccionarios
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
    
    if not os.path.exists(dictionaries_file):
        print(f"Error: No se encontró el archivo {dictionaries_file}")
        return ""
    
    print(f"Creando archivo final combinando:")
    print(f"  - {prompt_file}")
    print(f"  - {wiki_unified_file}")
    print(f"  - {dictionaries_file}")
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
            wiki_content = f.read().strip()
    except Exception as e:
        print(f"Error al leer {wiki_unified_file}: {e}")
        return ""
    
    # Leer el contenido de los diccionarios unificados
    try:
        with open(dictionaries_file, 'r', encoding='utf-8') as f:
            dictionaries_content = f.read().strip()
    except Exception as e:
        print(f"Error al leer {dictionaries_file}: {e}")
        return ""
    
    # Insertar el contenido en las secciones correspondientes
    # Primero insertar el contenido de wiki después de "### CONTEXTO ###"
    if "### CONTEXTO ###" in prompt_content:
        prompt_content = prompt_content.replace(
            "### CONTEXTO ###",
            "### CONTEXTO ###\n\n" + wiki_content
        )
    else:
        # Si no existe la sección, agregarla al final del prompt
        prompt_content = prompt_content.strip() + "\n\n### CONTEXTO ###\n\n" + wiki_content
    
    # Luego insertar el contenido de diccionarios después de "### DICCIONARIOS ###"
    if "### DICCIONARIOS ###" in prompt_content:
        prompt_content = prompt_content.replace(
            "### DICCIONARIOS ###",
            "### DICCIONARIOS ###\n\n" + dictionaries_content
        )
    else:
        # Si no existe la sección, agregarla al final
        prompt_content = prompt_content.strip() + "\n\n### DICCIONARIOS ###\n\n" + dictionaries_content
    
    final_content = prompt_content
    
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

