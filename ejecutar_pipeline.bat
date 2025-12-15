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

REM Verificar que git este instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no esta instalado o no esta en el PATH.
    echo No se puede subir el archivo al repositorio remoto.
    goto :eof
)

REM Verificar que los archivos existen
if not exist "vibe_SQL_copilot.txt" (
    echo ERROR: El archivo vibe_SQL_copilot.txt no existe.
    echo No se puede subir al repositorio remoto.
    goto :eof
)

if not exist "README_vibe_query.md" (
    echo ERROR: El archivo README_vibe_query.md no existe.
    echo No se puede subir al repositorio remoto.
    goto :eof
)

set remote_url=https://github.com/ramsestein/vibe_query_DataNex.git
set temp_repo=.temp_vibe_query

REM Limpiar directorio temporal si existe
if exist "%temp_repo%" (
    echo Limpiando directorio temporal anterior...
    rmdir /s /q "%temp_repo%"
)

REM Clonar el repositorio destino (shallow clone para ser rapido)
echo Clonando repositorio destino...
git clone --depth 1 "%remote_url%" "%temp_repo%" >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudo clonar el repositorio destino.
    echo Verifique la URL y sus permisos.
    goto :cleanup
)

REM Copiar los archivos al repositorio clonado
echo Copiando archivos al repositorio destino...
copy /y "vibe_SQL_copilot.txt" "%temp_repo%\vibe_SQL_copilot.txt" >nul
if errorlevel 1 (
    echo ERROR: No se pudo copiar vibe_SQL_copilot.txt.
    goto :cleanup
)

copy /y "README_vibe_query.md" "%temp_repo%\README.md" >nul
if errorlevel 1 (
    echo ERROR: No se pudo copiar README_vibe_query.md.
    goto :cleanup
)

REM Cambiar al directorio del repo clonado
cd "%temp_repo%"

REM Verificar si hay cambios
git diff --quiet 2>nul
if errorlevel 1 (
    echo Haciendo commit de los archivos...
    git add vibe_SQL_copilot.txt README.md
    git commit -m "Actualizar vibe_SQL_copilot.txt y README desde pipeline" --no-verify
    if errorlevel 1 (
        echo ERROR: No se pudo hacer commit.
        cd ..
        goto :cleanup
    )
    
    echo Subiendo archivo al repositorio remoto...
    git push origin main --force
    if errorlevel 1 (
        echo ERROR: No se pudo hacer push al repositorio remoto.
        cd ..
        goto :cleanup
    )
    
    echo.
    echo [OK] Archivos subidos exitosamente a:
    echo %remote_url%
    echo   - vibe_SQL_copilot.txt
    echo   - README.md
) else (
    echo No hay cambios en los archivos. No se necesita actualizar.
)

REM Volver al directorio original
cd ..

:cleanup
REM Limpiar directorio temporal
if exist "%temp_repo%" (
    echo Limpiando directorio temporal...
    rmdir /s /q "%temp_repo%"
)

goto :eof
