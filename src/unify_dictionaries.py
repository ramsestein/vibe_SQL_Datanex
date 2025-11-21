"""
Módulo para unificar diccionarios CSV en un markdown.
"""

import os
import csv
import glob
from pathlib import Path
from collections import defaultdict
import re


def _clean_lab_description(text):
    """
    Limpia la descripción del diccionario de lab eliminando:
    - Conjunciones (y, o, e, ni, pero, etc.)
    - Determinantes (el, la, los, las, un, una, unos, unas, etc.)
    - Comas
    
    Args:
        text: Texto a limpiar
    
    Returns:
        Texto limpio
    """
    # Lista de palabras a eliminar (conjunciones y determinantes)
    words_to_remove = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'y', 'o', 'e', 'ni', 'pero', 'mas', 'sino', 'que', 'de', 'del', 'al',
        'a', 'en', 'por', 'para', 'con', 'sin', 'sobre', 'bajo', 'entre'
    }
    
    # Dividir en palabras
    words = text.split()
    
    # Filtrar palabras y eliminar comas
    cleaned_words = []
    for word in words:
        # Eliminar comas y otros signos de puntuación al inicio/final
        word_clean = word.strip(',.;:()[]{}')
        # Convertir a minúsculas para comparar
        word_lower = word_clean.lower()
        
        # Si no es una palabra a eliminar y no está vacía, agregarla
        if word_lower not in words_to_remove and word_clean:
            cleaned_words.append(word_clean)
    
    # Unir palabras con espacios
    return ' '.join(cleaned_words)


def _find_common_prefix(texts):
    """
    Encuentra el prefijo común más largo entre una lista de textos.
    
    Args:
        texts: Lista de textos
    
    Returns:
        Prefijo común (puede ser vacío)
    """
    if not texts:
        return ""
    
    # Encontrar el prefijo común
    common = texts[0]
    for text in texts[1:]:
        # Encontrar hasta dónde coinciden
        min_len = min(len(common), len(text))
        i = 0
        while i < min_len and common[i].lower() == text[i].lower():
            i += 1
        common = common[:i]
        if not common:
            return ""
    
    # Asegurar que terminamos en un espacio o palabra completa
    # Buscar el último espacio antes del final del prefijo común
    last_space = common.rfind(' ')
    if last_space > len(common) * 0.3:  # Si el espacio está en una posición razonable
        common = common[:last_space].strip()
    
    return common.strip()


def _compact_tree_structure(tuples):
    """
    Compacta tuplas eliminando prefijos comunes del sistema de árbol.
    
    Agrupa códigos que comparten prefijos comunes y extrae texto común de las descripciones.
    Por ejemplo: 
    - 6000029: Aborto espontaneo con alteracion metabolica incompleto
    - 6000030: Aborto espontaneo con complicacion neom completo
    -> 60000:Aborto espontaneo|29:con alteracion metabolica incompleto|30:con complicacion neom completo
    
    Args:
        tuples: Lista de tuplas (ref, descr)
    
    Returns:
        Lista de entradas compactadas (pueden ser tuplas individuales o strings agrupados)
    """
    if not tuples:
        return []
    
    # Analizar prefijos comunes
    # Agrupar por diferentes longitudes de prefijo (de más largo a más corto)
    max_ref_len = max(len(str(ref)) for ref, _ in tuples)
    
    # Probar diferentes longitudes de prefijo, empezando por prefijos más largos
    for prefix_len in range(max_ref_len - 1, 2, -1):  # Desde prefijos largos a cortos
        prefix_groups = defaultdict(list)
        
        for ref, descr in tuples:
            ref_str = str(ref)
            if len(ref_str) >= prefix_len:
                prefix = ref_str[:prefix_len]
                suffix = ref_str[prefix_len:]
                prefix_groups[prefix].append((suffix, descr))
        
        # Si encontramos grupos con al menos 3 entradas, compactar
        compacted = []
        used_refs = set()
        
        for prefix, group in prefix_groups.items():
            if len(group) >= 3:  # Solo compactar si hay al menos 3 entradas con el mismo prefijo
                # Encontrar texto común en las descripciones
                descriptions = [descr for _, descr in group]
                common_text = _find_common_prefix(descriptions)
                
                # Limpiar y procesar descripciones
                group_entries = []
                for suffix, descr in group:
                    # Extraer solo la parte diferente
                    if common_text and descr.lower().startswith(common_text.lower()):
                        diff_text = descr[len(common_text):].strip()
                        # Si la diferencia empieza con " con", " de", etc., mantenerlo
                        if diff_text and not diff_text.startswith((' con', ' de', ' y', ' o', ' a', ' en')):
                            diff_text = ' ' + diff_text
                    else:
                        diff_text = descr
                    
                    # Limpiar caracteres problemáticos
                    diff_text = diff_text.replace('|', ' ').replace('\n', ' ').replace('\r', ' ').replace(':', ';').strip()
                    # Nota: La limpieza de lab (conjunciones, determinantes, comas) ya se aplicó antes
                    if len(diff_text) > 80:
                        diff_text = diff_text[:77] + "..."
                    
                    group_entries.append(f"{suffix}:{diff_text}")
                    used_refs.add(f"{prefix}{suffix}")
                
                # Crear entrada compactada: prefix:common_text|suffix1:diff1|suffix2:diff2|...
                if common_text:
                    compacted.append(f"{prefix}:{common_text}|{'|'.join(group_entries)}")
                else:
                    # Si no hay texto común, usar formato anterior
                    compacted.append(f"{prefix}|{'|'.join(group_entries)}")
            else:
                # No compactar este grupo, agregar individualmente
                for suffix, descr in group:
                    full_ref = f"{prefix}{suffix}"
                    if full_ref not in used_refs:
                        compacted.append((full_ref, descr))
                        used_refs.add(full_ref)
        
        # Si compactamos algo, retornar el resultado
        if any('|' in str(e) and not isinstance(e, tuple) for e in compacted):
            # Agregar entradas que no fueron agrupadas
            for ref, descr in tuples:
                if str(ref) not in used_refs:
                    compacted.append((str(ref), descr))
            return compacted
    
    # Si no se pudo compactar, retornar original
    return tuples


def unify_dictionaries(dicc_dir: str, output_file: str) -> str:
    """
    Convierte todos los CSV de diccionarios en la carpeta dicc a un markdown unificado.
    
    Para cada CSV, extrae las columnas que terminan en '_ref' y '_descr' y crea
    tuplas de estos valores.
    
    Args:
        dicc_dir: Directorio que contiene los archivos CSV de diccionarios
        output_file: Ruta del archivo markdown de salida
    
    Returns:
        Ruta del archivo markdown creado, o None si hay error
    """
    # Crear directorio de salida si no existe
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Buscar todos los archivos CSV en el directorio
    csv_files = glob.glob(os.path.join(dicc_dir, "*.csv"))
    
    if not csv_files:
        print(f"⚠ No se encontraron archivos CSV en {dicc_dir}")
        return None
    
    print(f"Encontrados {len(csv_files)} archivos CSV:")
    for csv_file in csv_files:
        print(f"  - {os.path.basename(csv_file)}")
    
    unified_content = []
    
    # Procesar cada archivo CSV
    for csv_file in sorted(csv_files):
        file_name = os.path.basename(csv_file)
        print(f"\nProcesando {file_name}...")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Detectar delimitador
                sample = f.read(1024)
                f.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(f, delimiter=delimiter)
                
                # Encontrar columnas ref y descr
                ref_col = None
                descr_col = None
                
                for col in reader.fieldnames:
                    if col.endswith('_ref'):
                        ref_col = col
                    elif col.endswith('_descr'):
                        descr_col = col
                
                if not ref_col or not descr_col:
                    print(f"  ⚠ No se encontraron columnas *_ref y *_descr en {file_name}")
                    continue
                
                print(f"  ✓ Columnas encontradas: {ref_col} -> {descr_col}")
                
                # Agregar título del diccionario (formato compacto)
                dict_name = file_name.replace('.csv', '').replace('dic_', '').replace('_', ' ').title()
                unified_content.append(f"## {dict_name}\n")
                
                # Leer y procesar filas
                tuples = []
                is_lab_dict = 'lab' in file_name.lower()
                
                for row in reader:
                    ref_value = row.get(ref_col, '').strip()
                    descr_value = row.get(descr_col, '').strip()
                    
                    if ref_value and descr_value:
                        # Limpiar descripción para dic_lab: quitar conjunciones, determinantes y comas
                        if is_lab_dict:
                            descr_value = _clean_lab_description(descr_value)
                        tuples.append((ref_value, descr_value))
                
                # Compactar eliminando prefijos comunes (sistema de árbol)
                # Agrupar por prefijos comunes para reducir redundancia
                compacted_tuples = _compact_tree_structure(tuples)
                
                # Agregar tuplas al contenido en formato compacto
                for entry in compacted_tuples:
                    if isinstance(entry, tuple):
                        # Entrada individual: ref:descr
                        ref, descr = entry
                        # La limpieza de lab ya se aplicó antes, solo limpiar caracteres problemáticos
                        descr_clean = descr.replace('|', ' ').replace('\n', ' ').replace('\r', ' ').replace(':', ';').strip()
                        if len(descr_clean) > 100:
                            descr_clean = descr_clean[:97] + "..."
                        unified_content.append(f"{ref}:{descr_clean}")
                    else:
                        # Entrada agrupada: prefix|suffix1:descr1|suffix2:descr2|...
                        unified_content.append(entry)
                
                unified_content.append("")  # Línea en blanco entre diccionarios
                
                print(f"  ✓ {len(tuples)} tuplas procesadas")
        
        except Exception as e:
            print(f"  ✗ Error procesando {file_name}: {e}")
            continue
    
    # Escribir archivo unificado
    if unified_content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unified_content))
        
        print(f"\n✓ Archivo unificado creado: {output_file}")
        return output_file
    else:
        print("\n⚠ No se pudo crear el archivo unificado (sin contenido)")
        return None

