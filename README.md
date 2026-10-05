# Truebound 1.2.0 — Cliente + Servidor (MC 26.2 / Fabric 0.19.3)

Fonte: https://modrinth.com/modpack/truebound (MIT) + 3 mods manuais:
Dynamic Crosshair 9.14 (client), VeinMiner 2.12.1 + FallingTree 26.2.0.3 (client+server).

## Pastas
- `instance/` — cliente isolado SKLauncher (70 mods: 68 ativos + 2 .disabled)
- `server/` — Fabric espelhado (39 mods server-side, mundo novo `truebound-new`)
- `Truebound.mrpack` — pack original 1.2.0 (2.6MB)

## Cliente (SKLauncher pirata/offline)
1. SKLauncher 4.0 > Importar `Truebound.mrpack` **ou** aponte o diretório do jogo para `instance/`
2. Copie os 3 `.jar` manuais para `instance/mods/` (já estão aqui):
   `dynamiccrosshair-9.14+26.2-fabric.jar`, `veinminer-fabric-2.12.1.jar`, `FallingTree-26.2-25.jar`
3. Java 25+ obrigatório: `sudo pacman -S jdk25-openjdk` (SKLauncher 4 baixa sozinho)
4. Server IP: `localhost:25565` (ou IP do host). online-mode=false aceita nick offline.

## Servidor
```
cd server
# 1. mods (sem commitar .jar): 
python3 baixar-mods-server.py
# 2. instale o Fabric (gera server.jar + libraries):
java -jar fabric-installer.jar server -mcversion 26.2 -loader 0.19.3 -downloadMinecraft
# 3. aceite a EULA (leia https://aka.ms/MinecraftEULA) e ligue:
#    eula.txt -> eula=true
chmod +x start.sh
./start.sh        # Linux — XMS=4G XMX=6G, Java 25+
# start.bat no Windows
```
- `server.properties` já vem com `online-mode=false` (pirata), mundo `truebound-new`, 10 players.
- **Segurança offline:** qualquer nick entra. Recomendado: `whitelist=true`, `/whitelist add <nick>`, `/op` só confiável.
- EULA: servidor só liga com `eula=true` após você concordar.

## Subir tudo junto (servidor + playit)
```bash
cd server
./start-tudo.sh   # sobe o túnel, espera ficar online e liga o servidor
```
Precisa do secret do agente: `export PLAYIT_SECRET=...` ou arquivo `server/.playit-secret`
(esse arquivo **não** vai pro git — cada host usa o seu). Sem o playit no ar, o endereço
público recusa conexão (timeout), mesmo com o servidor rodando.

## Expor com playit.gg (amigo fora da sua rede, sem port forward)
Agente já testado no Linux (v1.0.10 em `~/.local/bin/playit` — não vai pro repo).
1. Crie conta em https://playit.gg/login/create
2. Rode `playit` no terminal, abra o link de claim que ele imprime e vincule o agente
3. No painel: Add Tunnel > **Minecraft Java (TCP)** > local `127.0.0.1:25565`
4. Com o **servidor + playit rodando**, passe o endereço público (ex: `xxx.playit.gg:12345`) pro amigo
5. Amigo: mesmo cliente deste repo > Multiplayer > endereço playit (região São Paulo = menor ping)

## GitHub (repo leve, sem binários)
`.gitignore` exclui `server.jar`, `libraries/`, `mods/*.jar`, `world/`, `logs/`.
Commita: configs, scripts, `*.json`, `*.md`, `*.txt`, `*.properties`, `start.sh/bat`.
Amigos clonam e rodam os 2 scripts (`baixar-mods.py` no root p/ cliente, `baixar-mods-server.py` p/ server).
