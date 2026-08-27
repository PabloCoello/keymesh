#!/usr/bin/env python3
"""Verifica keymap.c antes de compilar.

Comprueba tres cosas que el compilador no siempre deja claras:
  1. Cada capa tiene exactamente 52 teclas. Si sobra o falta una coma, el
     compilador acepta el fichero y el teclado sale con las teclas corridas.
  2. Ningún keycode personalizado queda declarado sin tratar, ni usado sin
     declarar.
  3. Todos los keycodes de las capas tienen etiqueta en la chuleta.

Devuelve 1 si algo falla.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def layer_keys(src):
    out = []
    for m in re.finditer(r"\[(L_\w+)\]\s*=\s*LAYOUT_voyager\(", src):
        i = src.index("(", m.end() - 1)
        depth = 0
        body = None
        for j in range(i, len(src)):
            if src[j] == "(":
                depth += 1
            elif src[j] == ")":
                depth -= 1
                if depth == 0:
                    body = re.sub(r"//[^\n]*", "", src[i + 1:j])
                    break
        if body is None:
            raise SystemExit(f"{m.group(1)}: falta el paréntesis de cierre")
        keys, depth, cur = [], 0, ""
        for ch in body:
            if ch == "(":
                depth += 1
                cur += ch
            elif ch == ")":
                depth -= 1
                cur += ch
            elif ch == "," and depth == 0:
                keys.append(cur.strip())
                cur = ""
            else:
                cur += ch
        if cur.strip():
            keys.append(cur.strip())
        out.append((m.group(1), [k for k in keys if k]))
    return out


def main():
    src = open(os.path.join(ROOT, "keymap.c"), encoding="utf-8").read()
    problems = []

    layers = layer_keys(src)
    if not layers:
        problems.append("no encuentro ninguna capa LAYOUT_voyager")
    for name, keys in layers:
        if len(keys) != 52:
            problems.append(f"{name}: {len(keys)} teclas, esperadas 52")

    start = src.index("enum custom_keycodes")
    blk = src[start:src.index("// ---", start)]
    declared = set(re.findall(r"\b(U_[A-Z_]+|HRD_[A-Z_]+)\b", blk))
    handled = set(re.findall(r"case (U_[A-Z_]+|HRD_[A-Z_]+):", src))
    if declared - handled:
        problems.append("declarados pero sin tratar: "
                        + ", ".join(sorted(declared - handled)))
    used_anywhere = set(re.findall(r"\b(U_[A-Z_]+|HRD_[A-Z_]+)\b", src))
    if used_anywhere - declared:
        problems.append("usados sin declarar: "
                        + ", ".join(sorted(used_anywhere - declared)))

    # Toda tecla colocada en una capa debe tener etiqueta en la chuleta,
    # para que una tecla nueva no aparezca como su keycode crudo.
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import labels as gc
    placed = {k for _, keys in layers for k in keys}
    unlabelled = sorted(
        k for k in placed
        if k not in gc.LABELS and k not in gc.HERDR
        and not re.match(r"^KC_(F\d+|\w)$", k))
    if unlabelled:
        problems.append("sin etiqueta en la chuleta: " + ", ".join(unlabelled))

    for p in problems:
        print("  FALLO", p)
    if problems:
        return 1
    counts = ", ".join(f"{n[2:]} {len(k)}" for n, k in layers)
    print(f"check: teclas por capa ({counts}); "
          f"{len(declared)} keycodes propios, todos tratados y etiquetados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
