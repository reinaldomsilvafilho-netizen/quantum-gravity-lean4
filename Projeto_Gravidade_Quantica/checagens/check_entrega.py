"""Confere uma entrega no ARQUIVO REAL antes de qualquer relato de sucesso.

Nasceu da falha de 2026-10-17: um agente editou só a cópia temporária e relatou sucesso.
Toda afirmação "editei X" de um agente passa por aqui (skill gtqg-tarefa-publicacao e
gtqg-tarefa-latex). Reprova se:
  E1  o caminho é cópia temporária (TEMP, scratchpad, tmp*) e não o arquivo do projeto;
  E2  o arquivo não existe;
  E3  o arquivo não mudou: hash igual ao --hash-antes, ou modificação mais antiga que --minutos;
  E4  falta um texto que a entrega diz ter posto (--contem), ou sobrou um que diz ter tirado (--nao-contem);
  E5  com --compilar (.tex): a compilação independente, numa cópia da pasta, não fecha
      0 erros / 0 avisos / 0 overfull / 0 indefinidas (mesma contagem do build_pdfs_safe.py).

Uso:
  python checagens/check_entrega.py ARQ --hash         # imprime o hash (rodar ANTES de lançar o agente)
  python checagens/check_entrega.py ARQ --hash-antes H --contem "texto novo" --nao-contem "texto velho" --compilar
Saída 0 = entrega conferida; 1 = reprovada (cada falha diz o que fazer).
"""
import argparse
import hashlib
import os
import pathlib
import shutil
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TEMP_MARCAS = ("\\appdata\\local\\temp", "/tmp/", "\\scratchpad", "/scratchpad")


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def conferir(arq, hash_antes=None, minutos=None, contem=(), nao_contem=(), compilar=False):
    falhas = []
    real = arq.resolve()
    baixo = str(real).lower().replace("/", "\\") + "\\"
    if any(m.replace("/", "\\") in baixo for m in TEMP_MARCAS) or real.name.startswith("tmp"):
        falhas.append(("E1", f"{real} é cópia temporária; edite o arquivo do projeto e confira de novo"))
    if not real.exists():
        falhas.append(("E2", f"{real} não existe"))
        return falhas, None
    h = sha256(real)
    if hash_antes and h == hash_antes:
        falhas.append(("E3", "o hash não mudou: a edição não chegou ao arquivo real"))
    if minutos is not None and time.time() - real.stat().st_mtime > 60 * minutos:
        falhas.append(("E3", f"última modificação há mais de {minutos} min"))
    texto = real.read_text(encoding="utf-8", errors="replace")
    for s in contem:
        if s not in texto:
            falhas.append(("E4", f"falta no arquivo real: «{s}»"))
    for s in nao_contem:
        if s in texto:
            falhas.append(("E4", f"ainda está no arquivo real: «{s}»"))
    if compilar and real.suffix == ".tex":
        import build_pdfs_safe as b
        with tempfile.TemporaryDirectory() as tmp:
            b.snapshot(str(real.parent), tmp)
            e, w, o, u, _ = b.compile_in(tmp, real.name)
        if (e, w, o, u) != (0, 0, 0, 0):
            falhas.append(("E5", f"compilação independente: erros={e} avisos={w} overfull={o} indefinidas={u}"))
    return falhas, h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--hash", action="store_true", help="só imprime o hash atual")
    ap.add_argument("--hash-antes")
    ap.add_argument("--minutos", type=float)
    ap.add_argument("--contem", action="append", default=[])
    ap.add_argument("--nao-contem", action="append", default=[])
    ap.add_argument("--compilar", action="store_true")
    a = ap.parse_args()
    arq = pathlib.Path(a.arquivo)
    if a.hash:
        print(sha256(arq.resolve()))
        return
    falhas, h = conferir(arq, a.hash_antes, a.minutos, a.contem, a.nao_contem, a.compilar)
    for cod, msg in falhas:
        print(f"REPROVA {cod}: {msg}")
    print(f"check_entrega: {arq.resolve()} sha256={h} -> {'REPROVADA' if falhas else 'CONFERIDA'}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
