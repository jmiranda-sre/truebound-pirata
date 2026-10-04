@echo off
REM start.bat — Truebound Fabric server no Windows (MC 26.2 / loader 0.19.3)
REM Requer Java 25+ (Adoptium/Temurin 25). Ajuste JAVA_BIN se preciso.
set JAVA_BIN=java
%JAVA_BIN% -version
findstr /R "^eula=true" eula.txt >nul
if errorlevel 1 (
  echo ERRO: aceite a EULA em eula.txt (eula=true). Leia https://aka.ms/MinecraftEULA
  pause
  exit /b 1
)
if "%XMS%"=="" set XMS=4G
if "%XMX%"=="" set XMX=6G
%JAVA_BIN% -Xms%XMS% -Xmx%XMX% -jar fabric-server-launch.jar nogui %*
pause
