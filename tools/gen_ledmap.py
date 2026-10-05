#!/usr/bin/env python3
"""Genera ledmap.h a partir de las capas definidas en keymap.c.

Las teclas transparentes o vacías quedan apagadas, para que cada capa
ilumine solo lo que realmente hace.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from led_order import to_led_order

SRC = os.path.join(ROOT, "keymap.c")
DST = os.path.join(ROOT, "ledmap.h")

LED_COUNT = 52

text = open(SRC, encoding="utf-8").read()

# Extrae los bloques LAYOUT_voyager(...) en orden de aparición.
blocks = []
for m in re.finditer(r"\[(L_\w+)\]\s*=\s*LAYOUT_voyager\(", text):
    name = m.group(1)
    i = text.index("(", m.end() - 1)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                blocks.append((name, text[i + 1:j]))
                break

layers = []
for name, body in blocks:
    body = re.sub(r"//[^\n]*", "", body)
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
    keys = [k for k in keys if k]
    if len(keys) != LED_COUNT:
        sys.exit(f"{name}: se esperaban {LED_COUNT} teclas, se encontraron {len(keys)}")
    layers.append((name, keys))

OFF = (0, 0, 0)

# Paletas por capa. h, s, v en el rango 0-255 de QMK.
LETTER   = (0, 190, 150)    # h se suma a base_hue() en la capa BASE
MODSHIFT = (96, 255, 230)   # teclas cuyo significado depende del host

# Las capas a las que se llega con los pulgares son planas: un color para toda
# la capa y otro para dos teclas de referencia, una por mano, que sirven para
# situar los dedos sin mirar la chuleta.
NAV_FLAT   = (140, 255, 200)
NAV_MARK   = (12, 255, 230)
SYM_FLAT   = (35, 255, 195)
SYM_MARK   = (163, 255, 230)
META_FLAT  = (170, 255, 200)
META_MARK  = (42, 255, 230)

MARKS = {
    "L_NAV":  (("KC_LEFT_GUI", "KC_DELETE"), NAV_FLAT, NAV_MARK),
    "L_SYM":  (("ES_AT", "ES_SLSH"), SYM_FLAT, SYM_MARK),
    "L_META": (("QK_BOOT", "HRD_CLOSE"), META_FLAT, META_MARK),
}


def is_blank(k):
    return k in ("KC_TRANSPARENT", "KC_NO", "KC_TRNS")


def color_base(k):
    if k in ("U_APP", "KC_RIGHT_CTRL"):
        return MODSHIFT
    return LETTER


def color_flat(name, k):
    marks, flat, mark = MARKS[name]
    return mark if k in marks else flat


def is_left(idx):
    return idx % 12 < 6 if idx < 48 else idx < 50


# Cada capa de MARKS tiene que existir, y cada tecla de referencia (izquierda,
# derecha) aparecer una sola vez y en su mano. Si no, el resalte se perdería o
# se iría de lado sin avisar.
layer_keys = dict(layers)
for name, (marks, _, _) in MARKS.items():
    if name not in layer_keys:
        sys.exit(f"{name}: la capa de MARKS no existe en keymap.c")
    keys = layer_keys[name]
    for k, left in zip(marks, (True, False)):
        n = keys.count(k)
        if n != 1:
            sys.exit(f"{name}: la tecla de referencia {k} aparece {n} veces")
        if is_left(keys.index(k)) != left:
            sys.exit(f"{name}: la tecla de referencia {k} no está en la mano esperada")


out = []
out.append("// GENERADO por gen_ledmap.py. No editar a mano.")
out.append("// Cada capa ilumina solo las teclas que hacen algo. En la capa BASE el")
out.append("// campo de tono se SUMA a base_hue(), que depende del host detectado.")
out.append("//")
out.append("// Las entradas van en orden de INDICE DE LED, que no es el de")
out.append("// LAYOUT_voyager. La permutacion esta en tools/led_order.py.")
out.append("#pragma once")
out.append("")
out.append("const uint8_t PROGMEM ledmap[][RGB_MATRIX_LED_COUNT][3] = {")

for name, keys in layers:
    rows = []
    for idx, k in enumerate(keys):
        if is_blank(k):
            c = OFF
        elif name == "L_BASE":
            c = color_base(k)
        else:
            c = color_flat(name, k)
        rows.append(c)
    # rows va en orden de keymap; el firmware indexa por LED. Ver led_order.py.
    body = ", ".join("{%d,%d,%d}" % c for c in to_led_order(rows))
    out.append(f"    [{name}] = {{ {body} }},")
    out.append("")

out.append("};")
out.append("")

open(DST, "w", encoding="utf-8").write("\n".join(out))
print(f"escrito {DST}: {len(layers)} capas x {LED_COUNT} LEDs")
for name, keys in layers:
    lit = sum(1 for k in keys if not is_blank(k))
    print(f"  {name}: {lit} teclas encendidas, {LED_COUNT - lit} apagadas")
