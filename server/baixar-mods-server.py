"""Baixa só os mods SERVER-SIDE do Truebound (39 de 70) para server/mods/.
Uso: python3 baixar-mods-server.py (roda dentro de server/ ou repo root com server/).
Não commita .jar no GitHub — amigos rodam este script.
"""
import zipfile, json, os, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
# repo root tem Truebound.mrpack; server/ tem ../Truebound.mrpack
CANDIDATES = [HERE / "Truebound.mrpack", HERE / ".." / "Truebound.mrpack",
              HERE / "server" / ".." / "Truebound.mrpack"]
MRPACK = next((p for p in CANDIDATES if p.exists()), None)
if MRPACK is None:
    # fallback: procura na pasta Games/Truebound
    alt = pathlib.Path.home() / "Games" / "Truebound" / "Truebound.mrpack"
    MRPACK = alt if alt.exists() else None
if MRPACK is None:
    raise SystemExit("Truebound.mrpack não encontrado. Coloque ao lado ou em ../")
SERVER_DIR = HERE if (HERE / "fabric-server-launch.jar").exists() else HERE / "server"
MODS = SERVER_DIR / "mods"
MODS.mkdir(parents=True, exist_ok=True)
# client-only: não vão pro servidor (render/UI). DynamicCrosshair é client.
SKIP = {
 "AmbientSounds_FABRIC_v6.3.6_mc26.2.jar","BetterF3-19.0.0-Fabric-26.2.jar",
 "CutThrough-v26.2.0-mc26.2.x-Fabric.jar","Flashback-0.41.1-for-MC26.2.jar",
 "HeldItemTooltips-v26.2.0-mc26.2.x-Fabric.jar","ImmediatelyFast-Fabric-1.16.1+26.2.jar",
 "InvMove-0.9.5+26.2-Fabric.jar","PickUpNotifier-v26.2.0-mc26.2.x-Fabric.jar",
 "PresenceFootsteps-1.13.3+26.2.jar","blur-fabric-6.3.1+26.2.jar",
 "chatanimation-fabric-1.3.0+mc26.2.jar","continuity-3.0.1+26.2.jar",
 "cursors_extended-fabric-4.1.7+26.2.jar","dark-loading-screen-1.6.19.jar",
 "dynamiccrosshair-9.14+26.2-fabric.jar","elytra_physics-fabric-2.6.2_mc26.2.jar",
 "entity_model_features-3.2.6-26.2-fabric.jar","entity_sound_features-0.8.1-26.1-fabric.jar",
 "entity_texture_features-7.1.1-26.2-fabric.jar","explosive-enhancement-1.4.2-26.2.jar",
 "fallingleaves-2.0.7+26.1.jar","fancytoasts-fabric-26.2.x-1.4.7.jar",
 "iris-fabric-1.11.2+mc26.2.jar","lambdynamiclights-4.12.2+26.2.jar",
 "modmenu-20.0.0.jar","punchy-2.6.1-fabric-26.2.jar","smoothgui-fabric-2.0.0+mc26.2.jar",
 "sodium-fabric-0.9.1+mc26.2.jar","visuality-0.7.14+26.2.jar",
}
MANUAL = [
 ("veinminer-fabric-2.12.1.jar", 523832,
  "https://cdn.modrinth.com/data/OhduvhIc/versions/InpIvPQ1/veinminer-fabric-2.12.1.jar"),
 ("FallingTree-26.2-25.jar", 493214,
  "https://cdn.modrinth.com/data/Fb4jn8m6/versions/sOoH5kkd/FallingTree-26.2-25.jar"),
 ("ultimate-daycounter-1.0.jar", 25712,
  "https://cdn.modrinth.com/data/veX8VVuB/versions/PNUOtxTt/ultimate-daycounter-1.0.jar"),
 ("SereneSeasons-fabric-26.2-26.1.2.0.6.jar", 412279,
  "https://cdn.modrinth.com/data/e0bNACJD/versions/q5mzi8wy/SereneSeasons-fabric-26.2-26.1.2.0.6.jar"),
 ("GlitchCore-fabric-26.2-26.2.0.0.0.jar", 334860,
  "https://cdn.modrinth.com/data/s3dmwKy5/versions/SDUCBYRU/GlitchCore-fabric-26.2-26.2.0.0.0.jar"),
]
UA = {"User-Agent": "Truebound-Server-Setup/1.0"}
def get(url, dest, size=-1):
    if dest.exists() and size > 0 and dest.stat().st_size == size:
        return "ok-cache"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as o:
        o.write(r.read())
    return "baixado"
z = zipfile.ZipFile(MRPACK)
idx = json.loads(z.read("modrinth.index.json"))
ok = fail = 0
for f in idx["files"]:
    name = f["path"].split("/")[-1]
    if not f["path"].startswith("mods/") or name in SKIP:
        continue
    dest = MODS / name
    try:
        print(get(f["downloads"][0], dest, f.get("fileSize", -1)), f["path"], flush=True)
        ok += 1
    except Exception as e:
        fail += 1
        print(f"FALHA {f['path']}: {e}", flush=True)
for name, size, url in MANUAL:
    try:
        print(get(url, MODS / name, size), f"mods/{name} (manual)", flush=True)
        ok += 1
    except Exception as e:
        fail += 1
        print(f"FALHA mods/{name}: {e}", flush=True)
print(f"PRONTO servidor: {ok} ok, {fail} falhas -> {MODS}")
