#!/bin/bash
# Script interactivo para ejecutar el pipeline de Datanex
# Permite gestionar la lista de páginas a excluir antes de ejecutar

# Colores para mejor UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PAGS_FILE="pags_descarte.txt"

# Función para verificar e instalar dependencias
verificar_dependencias() {
    echo ""
    echo "Verificando dependencias..."
    echo ""
    
    # Verificar si existe requirements.txt
    if [ ! -f "requirements.txt" ]; then
        echo -e "${YELLOW}ADVERTENCIA: No se encontró requirements.txt${NC}"
        echo "Las dependencias no se instalarán automáticamente."
        return 0
    fi
    
    # Actualizar pip primero
    echo "Actualizando pip..."
    python3 -m pip install --upgrade pip --quiet 2>/dev/null || python3 -m pip install --upgrade pip
    
    # Verificar si las dependencias están instaladas
    echo "Verificando dependencias instaladas..."
    python3 -m pip check >/dev/null 2>&1
    
    # Instalar o actualizar dependencias desde requirements.txt
    echo "Instalando/actualizando dependencias desde requirements.txt..."
    if ! python3 -m pip install -r requirements.txt --quiet --upgrade 2>/dev/null; then
        echo ""
        echo -e "${YELLOW}ERROR al instalar dependencias. Intentando sin modo silencioso...${NC}"
        if ! python3 -m pip install -r requirements.txt --upgrade; then
            echo -e "${RED}ERROR: No se pudieron instalar las dependencias.${NC}"
            return 1
        fi
    fi
    
    echo ""
    echo -e "${GREEN}Dependencias verificadas e instaladas correctamente.${NC}"
    return 0
}

# Función para ver páginas
ver_paginas() {
    echo ""
    echo "========================================"
    echo "PÁGINAS EN LA LISTA DE EXCLUSIÓN"
    echo "========================================"
    echo ""
    if [ -f "$PAGS_FILE" ]; then
        echo "Contenido de $PAGS_FILE:"
        echo "----------------------------------------"
        cat "$PAGS_FILE"
        echo "----------------------------------------"
    else
        echo "El archivo $PAGS_FILE no existe."
        echo "(Se procesarán todas las páginas disponibles)"
    fi
    echo ""
    read -p "Presione Enter para continuar..."
}

# Función para agregar página
agregar_pagina() {
    echo ""
    echo "========================================"
    echo "AGREGAR PÁGINA A LA LISTA DE EXCLUSIÓN"
    echo "========================================"
    echo ""
    read -p "Ingrese el nombre de la página a excluir (sin extensión): " nueva_pagina
    
    if [ -z "$nueva_pagina" ]; then
        echo "Nombre de página vacío. Operación cancelada."
        read -p "Presione Enter para continuar..."
        return
    fi
    
    # Verificar si ya existe
    if [ -f "$PAGS_FILE" ]; then
        if grep -Fxq "$nueva_pagina" "$PAGS_FILE"; then
            echo ""
            echo "La página \"$nueva_pagina\" ya está en la lista de exclusión."
            read -p "Presione Enter para continuar..."
            return
        fi
    fi
    
    # Agregar la página al archivo
    echo "$nueva_pagina" >> "$PAGS_FILE"
    echo ""
    echo -e "${GREEN}Página \"$nueva_pagina\" agregada a la lista de exclusión.${NC}"
    echo ""
    read -p "Presione Enter para continuar..."
}

# Función para quitar página
quitar_pagina() {
    echo ""
    echo "========================================"
    echo "QUITAR PÁGINA DE LA LISTA DE EXCLUSIÓN"
    echo "========================================"
    echo ""
    
    if [ ! -f "$PAGS_FILE" ]; then
        echo "El archivo $PAGS_FILE no existe. No hay páginas para quitar."
        read -p "Presione Enter para continuar..."
        return
    fi
    
    echo "Páginas actuales en la lista:"
    echo "----------------------------------------"
    cat "$PAGS_FILE"
    echo "----------------------------------------"
    echo ""
    
    read -p "Ingrese el nombre de la página a quitar (sin extensión): " pagina_quitar
    
    if [ -z "$pagina_quitar" ]; then
        echo "Nombre de página vacío. Operación cancelada."
        read -p "Presione Enter para continuar..."
        return
    fi
    
    # Verificar si existe
    if ! grep -Fxq "$pagina_quitar" "$PAGS_FILE"; then
        echo ""
        echo "La página \"$pagina_quitar\" no está en la lista de exclusión."
        read -p "Presione Enter para continuar..."
        return
    fi
    
    # Crear archivo temporal sin la página a quitar
    grep -vFx "$pagina_quitar" "$PAGS_FILE" > "${PAGS_FILE}.tmp" 2>/dev/null
    
    # Reemplazar el archivo original
    if [ -f "${PAGS_FILE}.tmp" ]; then
        mv "${PAGS_FILE}.tmp" "$PAGS_FILE"
        # Si el archivo quedó vacío, eliminarlo
        if [ ! -s "$PAGS_FILE" ]; then
            rm "$PAGS_FILE"
        fi
    else
        # Si no se pudo crear el temporal, eliminar el archivo original
        rm "$PAGS_FILE" 2>/dev/null
    fi
    
    echo ""
    echo -e "${GREEN}Página \"$pagina_quitar\" eliminada de la lista de exclusión.${NC}"
    echo ""
    read -p "Presione Enter para continuar..."
}

# Función para subir archivo al repositorio remoto
subir_archivo_remoto() {
    echo ""
    echo "========================================"
    echo "SUBIENDO ARCHIVO AL REPOSITORIO REMOTO"
    echo "========================================"
    echo ""
    
    # Verificar que git esté instalado
    if ! command -v git &> /dev/null; then
        echo -e "${RED}ERROR: Git no está instalado o no está en el PATH.${NC}"
        echo "No se puede subir el archivo al repositorio remoto."
        return 1
    fi
    
    # Verificar que el archivo existe
    if [ ! -f "vibe_SQL_copilot.txt" ]; then
        echo -e "${RED}ERROR: El archivo vibe_SQL_copilot.txt no existe.${NC}"
        echo "No se puede subir al repositorio remoto."
        return 1
    fi
    
    # Configurar el remote si no existe
    local remote_name="vibe_query"
    local remote_url="https://github.com/ramsestein/vibe_query_DataNex.git"
    
    if ! git remote get-url "$remote_name" &> /dev/null; then
        echo "Configurando remote \"$remote_name\"..."
        git remote add "$remote_name" "$remote_url"
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: No se pudo agregar el remote.${NC}"
            return 1
        fi
    else
        # Verificar que apunta al URL correcto
        git remote set-url "$remote_name" "$remote_url"
    fi
    
    echo ""
    echo "Agregando archivo vibe_SQL_copilot.txt al staging..."
    git add vibe_SQL_copilot.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo agregar el archivo al staging.${NC}"
        return 1
    fi
    
    # Verificar si hay cambios para commitear
    if ! git diff --cached --quiet vibe_SQL_copilot.txt; then
        echo "Haciendo commit del archivo..."
        git commit -m "Actualizar vibe_SQL_copilot.txt desde pipeline" --no-verify
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: No se pudo hacer commit del archivo.${NC}"
            return 1
        fi
        
        echo "Subiendo archivo al repositorio remoto..."
        git push "$remote_name" main
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: No se pudo hacer push al repositorio remoto.${NC}"
            echo "Verifique que tiene permisos y que el repositorio existe."
            return 1
        fi
        
        echo ""
        echo -e "${GREEN}Archivo vibe_SQL_copilot.txt subido exitosamente a:${NC}"
        echo "$remote_url"
    else
        echo "No hay cambios en el archivo. No se necesita actualizar."
    fi
    
    return 0
}

# Función para ejecutar pipeline
ejecutar_pipeline() {
    echo ""
    echo "========================================"
    echo "EJECUTANDO PIPELINE"
    echo "========================================"
    echo ""
    
    # Verificar que el entorno virtual esté activado
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Reactivando entorno virtual..."
        source .venv/bin/activate 2>/dev/null || {
            echo -e "${RED}ERROR: No se pudo activar el entorno virtual.${NC}"
            read -p "Presione Enter para continuar..."
            return
        }
        verificar_dependencias
    fi
    
    if [ -f "$PAGS_FILE" ]; then
        echo "Lista de páginas a excluir:"
        cat "$PAGS_FILE"
        echo ""
    else
        echo "No hay lista de exclusión. Se procesarán todas las páginas."
        echo ""
    fi
    read -p "Presione Enter para continuar..."
    echo ""
    echo "Ejecutando pipeline..."
    echo ""
    python3 main.py
    echo ""
    echo "========================================"
    echo "Pipeline completado."
    echo "========================================"
    
    # Subir archivo al repositorio remoto
    subir_archivo_remoto
    
    read -p "Presione Enter para continuar..."
}

# Función del menú principal
menu() {
    while true; do
        clear
        echo "========================================"
        echo "MENÚ PRINCIPAL"
        echo "========================================"
        echo ""
        echo "1. Ver páginas actuales a excluir"
        echo "2. Agregar página a la lista de exclusión"
        echo "3. Quitar página de la lista de exclusión"
        echo "4. Ejecutar pipeline"
        echo "5. Salir"
        echo ""
        read -p "Seleccione una opción (1-5): " opcion
        
        case $opcion in
            1)
                ver_paginas
                ;;
            2)
                agregar_pagina
                ;;
            3)
                quitar_pagina
                ;;
            4)
                ejecutar_pipeline
                ;;
            5)
                echo ""
                echo "Saliendo..."
                exit 0
                ;;
            *)
                echo -e "${RED}Opción inválida. Por favor seleccione 1-5.${NC}"
                sleep 1
                ;;
        esac
    done
}

# Inicio del script
clear
echo "========================================"
echo "Pipeline Datanex - Gestor Interactivo"
echo "========================================"
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 no está instalado o no está en el PATH.${NC}"
    echo "Por favor instale Python 3.8 o superior."
    exit 1
fi

# Verificar que pip esté disponible
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}ERROR: pip no está disponible.${NC}"
    echo "Por favor instale pip o reinstale Python."
    exit 1
fi

# Verificar si existe el entorno virtual, si no, crearlo
if [ ! -f ".venv/bin/activate" ]; then
    echo ""
    echo "El entorno virtual no existe. Creándolo..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo crear el entorno virtual.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Entorno virtual creado.${NC}"
fi

# Activar el entorno virtual
echo ""
echo "Activando entorno virtual..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo activar el entorno virtual.${NC}"
    exit 1
fi

# Verificar e instalar dependencias
verificar_dependencias
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudieron instalar las dependencias.${NC}"
    exit 1
fi

# Ir al menú
menu

