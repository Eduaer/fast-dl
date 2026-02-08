# -*- coding: utf-8 -*-
"""
Comprime todos os arquivos do FastDL para .bz2 (ao lado do original).
Caminho: E:\src\fast-dl
Execute: python compress_to_bz2.py
"""

import bz2
import os

FASTDL_ROOT = r"E:\src\fast-dl"
COMPRESS_LEVEL = 9  # 1-9, 9 = menor tamanho

# Extensões que fazem sentido comprimir (arquivos que o cliente baixa)
EXTENSIONS = {".mdl", ".vvd", ".vtx", ".phy", ".ani", ".vmt", ".vtf", ".mp3", ".wav", ".wmv", ".wma"}

# Ou comprimir TUDO exceto já .bz2 (descomente a linha abaixo e comente EXTENSIONS)
COMPRESS_ALL = False  # True = ignora EXTENSIONS e comprime tudo

def should_compress(path):
    if path.lower().endswith(".bz2"):
        return False
    if COMPRESS_ALL:
        return True
    return os.path.splitext(path)[1].lower() in EXTENSIONS

def main():
    total = 0
    skipped = 0
    for root, dirs, files in os.walk(FASTDL_ROOT):
        for name in files:
            path = os.path.join(root, name)
            if not should_compress(path):
                skipped += 1
                continue
            out_path = path + ".bz2"
            if os.path.exists(out_path):
                skipped += 1
                continue
            try:
                with open(path, "rb") as f_in:
                    data = f_in.read()
                with open(out_path, "wb") as f_out:
                    f_out.write(bz2.compress(data, compresslevel=COMPRESS_LEVEL))
                total += 1
                print("OK:", os.path.relpath(out_path, FASTDL_ROOT))
            except Exception as e:
                print("ERRO:", path, "->", e)
    print("\nConcluído. Comprimidos:", total, "| Ignorados/já existentes:", skipped)

if __name__ == "__main__":
    main()
