#!/usr/bin/env python3
"""RCON simples p/ console do servidor. Uso: python3 rcon.py "<comando>" [...]
Senha via: arg --pass, env RCON_PASS ou arquivo server/.rcon-pass"""
import socket, struct, sys, os, pathlib
HOST = os.environ.get("RCON_HOST", "127.0.0.1")
PORT = int(os.environ.get("RCON_PORT", "25575"))
def pkt(rid, typ, payload):
    body = struct.pack("<ii", rid, typ) + payload.encode() + b"\x00\x00"
    return struct.pack("<i", len(body)) + body
def read_pkt(s):
    ln = struct.unpack("<i", s.recv(4))[0]
    data = b""
    while len(data) < ln:
        data += s.recv(ln - len(data))
    rid, typ = struct.unpack("<ii", data[:8])
    return rid, typ, data[8:-2].decode(errors="replace")
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--pass")]
    pw = None
    for a in sys.argv[1:]:
        if a.startswith("--pass"):
            pw = a.split("=", 1)[1] if "=" in a else sys.argv[sys.argv.index(a) + 1]
    if not pw:
        pw = os.environ.get("RCON_PASS")
    if not pw:
        cand = pathlib.Path(__file__).parent / ".rcon-pass"
        if cand.exists():
            pw = cand.read_text().strip()
    if not pw:
        sys.exit("sem senha: --pass=PASS, RCON_PASS ou server/.rcon-pass")
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.sendall(pkt(1, 3, pw))
    rid, _, _ = read_pkt(s)
    if rid == -1:
        sys.exit("RCON: senha errada")
    for cmd in args:
        s.sendall(pkt(2, 2, cmd))
        _, _, out = read_pkt(s)
        print(out)
main()
