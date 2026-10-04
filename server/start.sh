#!/usr/bin/env bash
# start.sh — Truebound Fabric server (MC 26.2 / loader 0.19.3)
# Requer Java 25+ (mods pedem >=25). Instale: sudo pacman -S jdk25-openjdk
set -euo pipefail
cd "$(dirname "$0")"
JAVA_BIN="${JAVA_BIN:-}"
if [ -z "$JAVA_BIN" ]; then
  for c in /usr/lib/jvm/java-25-openjdk/bin/java /usr/lib/jvm/java-27-openjdk/bin/java java; do
    if command -v "${c%% *}" >/dev/null 2>&1 || [ -x "$c" ]; then JAVA_BIN="$c"; break; fi
  done
fi
echo "Java: $JAVA_BIN"
"$JAVA_BIN" -version 2>&1 | head -n 2
if [ ! -f eula.txt ] || ! grep -q "^eula=true" eula.txt; then
  echo "ERRO: aceite a EULA em eula.txt (eula=true). Leia https://aka.ms/MinecraftEULA"
  exit 1
fi
XMS="${XMS:-4G}"; XMX="${XMX:-6G}"
exec "$JAVA_BIN" -Xms"$XMS" -Xmx"$XMX" -jar fabric-server-launch.jar nogui "$@"
