@echo off
title TruData Hub - Acesso Remoto Seguro (Internet)
echo ================================================================
echo   Iniciando Cockpit TruData ERP com Conexao para a Internet
echo ================================================================
echo.

:: 1. Iniciar Servidor Original na porta 8080
netstat -ano | findstr :8080 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo [1/3] Iniciando servidor do projeto na porta 8080...
    start /B python "%~dp0painel_aprovacao\servidor_painel.py"
    timeout /t 1 /nobreak >nul
) else (
    echo [1/3] Servidor do projeto ja esta ativo na porta 8080.
)

:: 2. Iniciar Proxy de Login na porta 8081
netstat -ano | findstr :8081 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo [2/3] Iniciando camada de login e senha na porta 8081...
    start /B python "%~dp0seguranca_login.py"
    timeout /t 1 /nobreak >nul
) else (
    echo [2/3] Camada de login ja esta ativa na porta 8081.
)

:: 3. Iniciar Tunel Cloudflare Seguro
echo [3/3] Conectando ao Cloudflare Tunnel (HTTPS Seguro)...
echo.
echo ================================================================
echo  ATENCAO: Copie o link 'https://....trycloudflare.com' que
echo  aparecera abaixo para abrir no seu celular ou em outro computador!
echo ================================================================
echo.
"%~dp0cloudflared.exe" tunnel --edge-ip-version 4 --protocol http2 --url http://localhost:8081
