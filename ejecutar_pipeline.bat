@echo off
REM Script para ejecutar el pipeline de Datanex
REM Este script activa el entorno virtual (si existe) y ejecuta main.py

echo ========================================
echo Pipeline Datanex - Ejecutando...
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo.
)

REM Ejecutar el script principal
echo Ejecutando pipeline...
python main.py

REM Mantener la ventana abierta para ver los resultados
echo.
echo ========================================
echo Pipeline completado.
echo ========================================
pause

