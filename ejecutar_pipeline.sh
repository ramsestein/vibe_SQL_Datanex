#!/bin/bash
# Script para ejecutar el pipeline de Datanex y subir el resultado automáticamente

# Colores para mejor UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "Pipeline Datanex - Ejecutando..."
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
    echo "El entorno virtual no existe. Creándolo..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo crear el entorno virtual.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Entorno virtual creado.${NC}"
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo activar el entorno virtual.${NC}"
    exit 1
fi

# Verificar e instalar dependencias
echo ""
echo "Verificando dependencias..."
echo ""

if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}ADVERTENCIA: No se encontró requirements.txt${NC}"
    echo "Las dependencias no se instalarán automáticamente."
else
    echo "Actualizando pip..."
    python3 -m pip install --upgrade pip --quiet 2>/dev/null || python3 -m pip install --upgrade pip
    
    echo "Instalando/actualizando dependencias desde requirements.txt..."
    if ! python3 -m pip install -r requirements.txt --quiet --upgrade 2>/dev/null; then
        echo -e "${YELLOW}ERROR al instalar dependencias. Intentando sin modo silencioso...${NC}"
        if ! python3 -m pip install -r requirements.txt --upgrade; then
            echo -e "${RED}ERROR: No se pudieron instalar las dependencias.${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}Dependencias verificadas e instaladas correctamente.${NC}"
fi

# Ejecutar pipeline
echo ""
echo "Ejecutando pipeline..."
echo ""
python3 main.py
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: El pipeline falló.${NC}"
    exit 1
fi

echo ""
echo "========================================"
echo "Pipeline completado."
echo "========================================"
echo ""

# Subir archivo al repositorio remoto
echo "========================================"
echo "SUBIENDO ARCHIVO AL REPOSITORIO REMOTO"
echo "========================================"
echo ""

# Verificar que git esté instalado
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git no está instalado o no está en el PATH.${NC}"
    echo "No se puede subir el archivo al repositorio remoto."
    exit 1
fi

# Verificar que los archivos existen
if [ ! -f "vibe_SQL_copilot.txt" ]; then
    echo -e "${RED}ERROR: El archivo vibe_SQL_copilot.txt no existe.${NC}"
    echo "No se puede subir al repositorio remoto."
    exit 1
fi

if [ ! -f "README_vibe_query.md" ]; then
    echo -e "${RED}ERROR: El archivo README_vibe_query.md no existe.${NC}"
    echo "No se puede subir al repositorio remoto."
    exit 1
fi

remote_url="https://github.com/ramsestein/vibe_query_DataNex.git"
temp_repo=".temp_vibe_query"

# Limpiar directorio temporal si existe
if [ -d "$temp_repo" ]; then
    echo "Limpiando directorio temporal anterior..."
    rm -rf "$temp_repo"
fi

# Clonar el repositorio destino (shallow clone para ser rápido)
echo "Clonando repositorio destino..."
git clone --depth 1 "$remote_url" "$temp_repo" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo clonar el repositorio destino.${NC}"
    echo "Verifique la URL y sus permisos."
    rm -rf "$temp_repo" 2>/dev/null
    exit 1
fi

# Copiar los archivos al repositorio clonado
echo "Copiando archivos al repositorio destino..."
cp "vibe_SQL_copilot.txt" "$temp_repo/vibe_SQL_copilot.txt"
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo copiar vibe_SQL_copilot.txt.${NC}"
    rm -rf "$temp_repo"
    exit 1
fi

cp "README_vibe_query.md" "$temp_repo/README.md"
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: No se pudo copiar README_vibe_query.md.${NC}"
    rm -rf "$temp_repo"
    exit 1
fi

# Cambiar al directorio del repo clonado
cd "$temp_repo"

# Verificar si hay cambios
if ! git diff --quiet 2>/dev/null; then
    echo "Haciendo commit de los archivos..."
    git add vibe_SQL_copilot.txt README.md
    git commit -m "Actualizar vibe_SQL_copilot.txt y README desde pipeline" --no-verify
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo hacer commit.${NC}"
        cd ..
        rm -rf "$temp_repo"
        exit 1
    fi
    
    echo "Subiendo archivo al repositorio remoto..."
    git push origin main --force
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo hacer push al repositorio remoto.${NC}"
        cd ..
        rm -rf "$temp_repo"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}Archivos subidos exitosamente a:${NC}"
    echo "$remote_url"
    echo "  - vibe_SQL_copilot.txt"
    echo "  - README.md"
else
    echo "No hay cambios en los archivos. No se necesita actualizar."
fi

# Volver al directorio original
cd ..

# Limpiar directorio temporal
echo "Limpiando directorio temporal..."
rm -rf "$temp_repo"

exit 0
