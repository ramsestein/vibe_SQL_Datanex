@echo off
setlocal enabledelayedexpansion
REM Script interactivo para ejecutar el pipeline de Datanex
REM Permite gestionar la lista de páginas a excluir antes de ejecutar

echo ========================================
echo Pipeline Datanex - Gestor Interactivo
echo ========================================
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor instale Python 3.8 o superior.
    pause
    exit /b 1
)

REM Verificar que pip esté disponible
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no esta disponible.
    echo Por favor instale pip o reinstale Python.
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual, si no, crearlo
if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo El entorno virtual no existe. Creandolo...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Entorno virtual creado.
)

REM Activar el entorno virtual
echo.
echo Activando entorno virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

REM Verificar e instalar dependencias
call :verificar_dependencias
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

set "pags_file=pags_descarte.txt"
goto menu

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

REM Verificar si las dependencias están instaladas
echo Verificando dependencias instaladas...
python -m pip check >nul 2>&1

REM Instalar o actualizar dependencias desde requirements.txt
echo Instalando/actualizando dependencias desde requirements.txt...
python -m pip install -r requirements.txt --quiet --upgrade
if errorlevel 1 (
    echo.
    echo ERROR al instalar dependencias. Intentando sin modo silencioso...
    python -m pip install -r requirements.txt --upgrade
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias.
        exit /b 1
    )
)

echo.
echo Dependencias verificadas e instaladas correctamente.
goto :eof

:menu
echo ========================================
echo MENU PRINCIPAL
echo ========================================
echo.
echo 1. Ver paginas actuales a excluir
echo 2. Agregar pagina a la lista de exclusion
echo 3. Quitar pagina de la lista de exclusion
echo 4. Ejecutar pipeline
echo 5. Salir
echo.
set /p opcion="Seleccione una opcion (1-5): "

if "%opcion%"=="1" goto ver_paginas
if "%opcion%"=="2" goto agregar_pagina
if "%opcion%"=="3" goto quitar_pagina
if "%opcion%"=="4" goto ejecutar_pipeline
if "%opcion%"=="5" goto salir
echo Opcion invalida. Por favor seleccione 1-5.
echo.
goto menu

:ver_paginas
echo.
echo ========================================
echo PAGINAS EN LA LISTA DE EXCLUSION
echo ========================================
echo.
if exist "%pags_file%" (
    echo Contenido de %pags_file%:
    echo ----------------------------------------
    type "%pags_file%"
    echo ----------------------------------------
) else (
    echo El archivo %pags_file% no existe.
    echo (Se procesaran todas las paginas disponibles)
)
echo.
pause
goto menu

:agregar_pagina
echo.
echo ========================================
echo AGREGAR PAGINA A LA LISTA DE EXCLUSION
echo ========================================
echo.
set /p nueva_pagina="Ingrese el nombre de la pagina a excluir (sin extension): "

if "!nueva_pagina!"=="" (
    echo Nombre de pagina vacio. Operacion cancelada.
    pause
    goto menu
)

REM Verificar si ya existe
if exist "%pags_file%" (
    findstr /C:"!nueva_pagina!" "%pags_file%" >nul 2>&1
    if !errorlevel! equ 0 (
        echo.
        echo La pagina "!nueva_pagina!" ya esta en la lista de exclusion.
        pause
        goto menu
    )
)

REM Agregar la pagina al archivo
echo !nueva_pagina!>> "%pags_file%"
echo.
echo Pagina "!nueva_pagina!" agregada a la lista de exclusion.
echo.
pause
goto menu

:quitar_pagina
echo.
echo ========================================
echo QUITAR PAGINA DE LA LISTA DE EXCLUSION
echo ========================================
echo.

if not exist "%pags_file%" (
    echo El archivo %pags_file% no existe. No hay paginas para quitar.
    pause
    goto menu
)

echo Paginas actuales en la lista:
echo ----------------------------------------
type "%pags_file%"
echo ----------------------------------------
echo.

set /p pagina_quitar="Ingrese el nombre de la pagina a quitar (sin extension): "

if "!pagina_quitar!"=="" (
    echo Nombre de pagina vacio. Operacion cancelada.
    pause
    goto menu
)

REM Verificar si existe
findstr /C:"!pagina_quitar!" "%pags_file%" >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo La pagina "!pagina_quitar!" no esta en la lista de exclusion.
    pause
    goto menu
)

REM Crear archivo temporal sin la pagina a quitar usando findstr para excluir la linea
set "temp_file=%pags_file%.tmp"
findstr /V /C:"!pagina_quitar!" "%pags_file%" > "%temp_file%"

REM Verificar que el archivo temporal no esté vacío (si solo había una línea, el archivo quedará vacío)
if exist "%temp_file%" (
    REM Reemplazar el archivo original
    move /Y "%temp_file%" "%pags_file%" >nul
) else (
    REM Si el archivo temporal no existe o está vacío, eliminar el archivo original
    del "%pags_file%" >nul 2>&1
    if exist "%temp_file%" del "%temp_file%" >nul 2>&1
)
echo.
echo Pagina "!pagina_quitar!" eliminada de la lista de exclusion.
echo.
pause
goto menu

:ejecutar_pipeline
echo.
echo ========================================
echo EJECUTANDO PIPELINE
echo ========================================
echo.

REM Verificar que el entorno virtual esté activado
if "%VIRTUAL_ENV%"=="" (
    echo Reactivando entorno virtual...
    call .venv\Scripts\activate.bat
    call :verificar_dependencias
)

if exist "%pags_file%" (
    echo Lista de paginas a excluir:
    type "%pags_file%"
    echo.
) else (
    echo No hay lista de exclusion. Se procesaran todas las paginas.
    echo.
)
pause
echo.
echo Ejecutando pipeline...
echo.
python main.py
echo.
echo ========================================
echo Pipeline completado.
echo ========================================
pause
goto menu

:salir
echo.
echo Saliendo...
exit /b 0
