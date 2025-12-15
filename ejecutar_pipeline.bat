@echo off
setlocal enabledelayedexpansion
REM Script para ejecutar el pipeline de Datanex y subir el resultado automáticamente

echo ========================================
echo Pipeline Datanex - Ejecutando...
echo ========================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor instale Python 3.8 o superior.
    exit /b 1
)

REM Verificar que pip esté disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no esta disponible.
    echo Por favor instale pip o reinstale Python.
    exit /b 1
)

REM Verificar si existe el entorno virtual, si no, crearlo
if not exist ".venv\Scripts\activate.bat" (
    echo El entorno virtual no existe. Creandolo...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        exit /b 1
    )
    echo Entorno virtual creado.
)

REM Activar el entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual.
    exit /b 1
)

REM Verificar e instalar dependencias
call :verificar_dependencias
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    exit /b 1
)

REM Ejecutar pipeline
echo.
echo Ejecutando pipeline...
echo.
python main.py
if errorlevel 1 (
    echo ERROR: El pipeline fallo.
    exit /b 1
)

echo.
echo ========================================
echo Pipeline completado.
echo ========================================
echo.

REM Subir archivo al repositorio remoto
call :subir_archivo_remoto

exit /b 0

:verificar_dependencias
echo.
echo Verificando dependencias...
echo.

REM Verificar si existe requirements.txt
if not exist "requirements.txt" (
    echo ADVERTENCIA: No se encontro requirements.txt
    echo Las dependencias no se instalaran automaticamente.
    goto :eof
)

REM Actualizar pip primero
echo Actualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar o actualizar dependencias desde requirements.txt
echo Instalando/actualizando dependencias desde requirements.txt...
python -m pip install -r requirements.txt --quiet --upgrade
if errorlevel 1 (
    echo ERROR al instalar dependencias. Intentando sin modo silencioso...
    python -m pip install -r requirements.txt --upgrade
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias.
        exit /b 1
    )
)

echo Dependencias verificadas e instaladas correctamente.
goto :eof

:subir_archivo_remoto
echo ========================================
echo SUBIENDO ARCHIVO AL REPOSITORIO REMOTO
echo ========================================
echo.

REM Verificar que git esté instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no esta instalado o no esta en el PATH.
    echo No se puede subir el archivo al repositorio remoto.
    goto :eof
)

REM Verificar que el archivo existe
if not exist "vibe_SQL_copilot.txt" (
    echo ERROR: El archivo vibe_SQL_copilot.txt no existe.
    echo No se puede subir al repositorio remoto.
    goto :eof
)

REM Configurar el remote si no existe
set "remote_name=vibe_query"
set "remote_url=https://github.com/ramsestein/vibe_query_DataNex.git"

git remote get-url "%remote_name%" >nul 2>&1
if errorlevel 1 (
    echo Configurando remote "%remote_name%"...
    git remote add "%remote_name%" "%remote_url%"
    if errorlevel 1 (
        echo ERROR: No se pudo agregar el remote.
        goto :eof
    )
) else (
    REM Verificar que apunta al URL correcto
    git remote set-url "%remote_name%" "%remote_url%"
)

echo Agregando archivo vibe_SQL_copilot.txt al staging...
git add vibe_SQL_copilot.txt
if errorlevel 1 (
    echo ERROR: No se pudo agregar el archivo al staging.
    goto :eof
)

REM Verificar si hay cambios para commitear
git diff --cached --quiet vibe_SQL_copilot.txt
if errorlevel 1 (
    echo Haciendo commit del archivo...
    git commit -m "Actualizar vibe_SQL_copilot.txt desde pipeline" --no-verify
    if errorlevel 1 (
        echo ERROR: No se pudo hacer commit del archivo.
        goto :eof
    )
    
    echo Subiendo archivo al repositorio remoto...
    git push "%remote_name%" main
    if errorlevel 1 (
        echo ERROR: No se pudo hacer push al repositorio remoto.
        echo Verifique que tiene permisos y que el repositorio existe.
        goto :eof
    )
    
    echo.
    echo Archivo vibe_SQL_copilot.txt subido exitosamente a:
    echo %remote_url%
) else (
    echo No hay cambios en el archivo. No se necesita actualizar.
)

goto :eof
