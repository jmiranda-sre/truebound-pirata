#!/usr/bin/env bash
# start-tudo.sh — sobe playit (túnel) + servidor Minecraft juntos.
# Evita o "connection timed out" causado por túnel sem agente.
# Uso: ./start-tudo.sh   (servidor fica em foreground; Ctrl+C derruba tudo)
# Secret: export PLAYIT_SECRET=... ou grave em server/.playit-secret (NÃO vai pro git)
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"
command -v playit >/dev/null || { echo "ERRO: binario playit nao achado em ~/.local/bin (veja README)"; exit 1; }
if [ -z "${PLAYIT_SECRET:-}" ]; then
  if [ -f .playit-secret ]; then PLAYIT_SECRET="$(cat .playit-secret)"
  else echo "ERRO: defina PLAYIT_SECRET ou crie server/.playit-secret"; exit 1
  fi
fi
SOCK="${PLAYIT_SOCK:-/tmp/playit.sock}"
# limpa daemon velho (se houver)
pkill -f "[p]layit --socket-path $SOCK" 2>/dev/null || true
sleep 1
rm -f "$SOCK"
nohup playit --secret "$PLAYIT_SECRET" --socket-path "$SOCK" > playit.log 2>&1 &
echo "playit subindo..."
for i in $(seq 1 30); do
  if playit-cli --socket-path "$SOCK" status 2>/dev/null | grep -q "Phase: running"; then
    echo "playit online (tentativa $i)"
    break
  fi
  sleep 2
  [ "$i" = 30 ] && { echo "ERRO: playit nao ficou online, veja playit.log"; exit 1; }
done
cleanup() { pkill -f "[p]layit --socket-path $SOCK" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
echo "subindo servidor..."
exec ./start.sh
