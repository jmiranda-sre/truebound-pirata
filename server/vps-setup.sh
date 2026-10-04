#!/usr/bin/env bash
# vps-setup.sh — sobe o Truebound Fabric (MC 26.2 / loader 0.19.3) numa VPS Ubuntu 24.04 x86_64
# Uso: rode como root ou com sudo numa VPS zerada com 4GB+ RAM.
# O que faz: Java 25 (Temurin), clone do repo, mods do servidor, Fabric, systemd + firewall.
set -euo pipefail
REPO="${REPO:-https://github.com/jmiranda-sre/truebound-pirata.git}"
DEST="${DEST:-/opt/truebound}"
MC_USER="${MC_USER:-minecraft}"
if [ "$(id -u)" -ne 0 ]; then echo "rode como root (sudo ./vps-setup.sh)"; exit 1; fi
apt-get update -y
apt-get install -y git python3 curl unzip ufw
# Java 25 Temurin (servidor e mods exigem >=25)
if [ ! -x /opt/java25/bin/java ]; then
  mkdir -p /opt/java25
  curl -L -o /tmp/java25.tar.gz \
    "https://api.adoptium.net/v3/binary/latest/25/ga/linux/x64/jdk/hotspot/normal/eclipse"
  tar xzf /tmp/java25.tar.gz -C /opt/java25 --strip-components=1
  rm /tmp/java25.tar.gz
fi
/opt/java25/bin/java -version 2>&1 | head -n 1
id "$MC_USER" &>/dev/null || useradd -r -m -d "$DEST" -s /bin/bash "$MC_USER"
if [ ! -d "$DEST/.git" ]; then
  git clone "$REPO" "$DEST"
  chown -R "$MC_USER:$MC_USER" "$DEST"
fi
cd "$DEST/server"
sudo -u "$MC_USER" python3 baixar-mods-server.py | tail -n 2
if [ ! -f fabric-server-launch.jar ] || [ ! -f server.jar ]; then
  sudo -u "$MC_USER" /opt/java25/bin/java -jar fabric-installer.jar server \
    -mcversion 26.2 -loader 0.19.3 -downloadMinecraft
fi
# EULA: o operador precisa aceitar. Libere descomentando ou edite server/eula.txt
if grep -q "^eula=false" eula.txt; then
  echo "AVISO: aceite a Mojang EULA em $DEST/server/eula.txt (eula=true) e rode: systemctl start minecraft"
fi
sed "s|/opt/truebound|$DEST|g; s|/opt/java25|/opt/java25|g" minecraft.service > /etc/systemd/system/minecraft.service
systemctl daemon-reload
systemctl enable minecraft
ufw allow 25565/tcp || true
ufw --force enable || true
echo "PRONTO. Edite eula.txt se preciso e suba com: systemctl start minecraft && journalctl -u minecraft -f"
