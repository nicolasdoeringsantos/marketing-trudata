@echo off
title Painel Executivo - TruData ERP
echo ===================================================
echo   Iniciando Cockpit Executivo - TruData ERP
echo ===================================================
echo.

:: 1. Verificar se o servidor ja esta ativo na porta 8080
netstat -ano | findstr :8080 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo [1/2] Iniciando servidor multi-thread na porta 8080...
    start /B python "%~dp0servidor_painel.py"
    timeout /t 1 /nobreak >nul
) else (
    echo [1/2] Servidor local ativo e pronto na porta 8080.
)

echo [2/2] Abrindo Cockpit no seu navegador...
start http://localhost:8080/
exit
