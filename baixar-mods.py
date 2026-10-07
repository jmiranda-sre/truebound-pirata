import zipfile, json, os, urllib.request
base=os.path.dirname(os.path.abspath(__file__))
z=zipfile.ZipFile(os.path.join(base,'Truebound.mrpack'))
idx=json.loads(z.read('modrinth.index.json'))
UA={"User-Agent":"SKLauncher-Setup/1.0"}
MANUAL=[
 ("mods/dynamiccrosshair-9.14+26.2-fabric.jar",536169,
  "https://cdn.modrinth.com/data/ZcR9weSm/versions/JGy4NTx0/dynamiccrosshair-9.14%2B26.2-fabric.jar"),
 ("mods/veinminer-fabric-2.12.1.jar",523832,
  "https://cdn.modrinth.com/data/OhduvhIc/versions/InpIvPQ1/veinminer-fabric-2.12.1.jar"),
 ("mods/FallingTree-26.2-25.jar",493214,
  "https://cdn.modrinth.com/data/Fb4jn8m6/versions/sOoH5kkd/FallingTree-26.2-25.jar"),
 ("mods/ultimate-daycounter-1.0.jar",25712,
  "https://cdn.modrinth.com/data/veX8VVuB/versions/PNUOtxTt/ultimate-daycounter-1.0.jar"),
 ("mods/SereneSeasons-fabric-26.2-26.1.2.0.6.jar",412279,
  "https://cdn.modrinth.com/data/e0bNACJD/versions/q5mzi8wy/SereneSeasons-fabric-26.2-26.1.2.0.6.jar"),
 ("mods/GlitchCore-fabric-26.2-26.2.0.0.0.jar",334860,
  "https://cdn.modrinth.com/data/s3dmwKy5/versions/SDUCBYRU/GlitchCore-fabric-26.2-26.2.0.0.0.jar"),
 ("mods/zoomify-2.16.3+26.2.jar",563034,
  "https://cdn.modrinth.com/data/w7ThoJFB/versions/2Qr8jSFc/zoomify-2.16.3%2B26.2.jar"),
 ("mods/biolith-fabric-3.7.0-beta.1.jar",237369,
  "https://cdn.modrinth.com/data/iGEl6Crx/versions/qSLRk6dS/biolith-fabric-3.7.0-beta.1.jar"),
 ("mods/ClimateRivers-v26.2.1-mc26.2.x-Fabric.jar",41129,
  "https://cdn.modrinth.com/data/DzZWws4q/versions/7OZbCRHr/ClimateRivers-v26.2.1-mc26.2.x-Fabric.jar"),
 ("mods/fabric-api-0.161.0+26.2.jar",2566123,
  "https://cdn.modrinth.com/data/P7dR8mSH/versions/ewUK83HI/fabric-api-0.161.0%2B26.2.jar"),
 ("mods/PuzzlesLib-v26.2.4-mc26.2.x-Fabric.jar",1153533,
  "https://cdn.modrinth.com/data/QAGBst4M/versions/aNOJuoCM/PuzzlesLib-v26.2.4-mc26.2.x-Fabric.jar"),
]
# Do mrpack, substituidos por versao manual (ex: biolith quebra com TerraBlender novo)
REPLACE={"mods/biolith-fabric-3.6.0-alpha.9.jar","mods/ClimateRivers-v26.2.0-mc26.2.x-Fabric.jar","mods/fabric-api-0.154.2+26.2.jar","mods/PuzzlesLib-v26.2.0-mc26.2.x-Fabric.jar"}
def fetch(url,dest,size=-1):
    if os.path.exists(dest) and size>0 and os.path.getsize(dest)==size:
        return True
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=120) as r, open(dest,'wb') as o:
        o.write(r.read())
    return True
ok,fail=0,0
for f in idx['files']:
    if f['path'] in REPLACE:
        old=os.path.join(base,'instance',f['path'])
        if os.path.exists(old): os.remove(old); print(f'REMOVIDO {f["path"]} (substituido)',flush=True)
        ok+=1; continue
    dest=os.path.join(base,'instance',f['path'])
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest)==f.get('fileSize',-1):
        ok+=1; continue
    try:
        fetch(f['downloads'][0],dest,f.get('fileSize',-1))
        ok+=1; print(f'OK {f["path"]}',flush=True)
    except Exception as e:
        fail+=1; print(f'FALHA {f["path"]}: {e}',flush=True)
for rel,size,url in MANUAL:
    dest=os.path.join(base,'instance',rel)
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    try:
        fetch(url,dest,size)
        ok+=1; print(f'OK {rel} (manual)',flush=True)
    except Exception as e:
        fail+=1; print(f'FALHA {rel}: {e}',flush=True)
print(f'PRONTO: {ok} ok, {fail} falhas')
