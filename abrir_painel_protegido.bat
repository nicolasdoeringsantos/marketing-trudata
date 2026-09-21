@echo off
title TruData Hub - Painel com Login Seguro
echo ===================================================
echo   Iniciando Cockpit TruData ERP (Acesso Protegido)
echo ===================================================
echo.

:: 1. Iniciar Servidor Original na porta 8080 (se ainda nao estiver ativo)
netstat -ano | findstr :8080 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo [1/3] Iniciando servidor do projeto na porta 8080...
    start /B python "%~dp0painel_aprovacao\servidor_painel.py"
    timeout /t 1 /nobreak >nul
) else (
    echo [1/3] Servidor do projeto ja esta ativo na porta 8080.
)

:: 2. Iniciar Proxy de Seguranca com Login na porta 8081 (se ainda nao estiver ativo)
netstat -ano | findstr :8081 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo [2/3] Iniciando camada de login e senha na porta 8081...
    start /B python "%~dp0seguranca_login.py"
    timeout /t 1 /nobreak >nul
) else (
    echo [2/3] Camada de login ja esta ativa na porta 8081.
)

:: 3. Abrir o navegador na porta protegida
echo [3/3] Abrindo tela de login no seu navegador...
start http://localhost:8081/
exit
