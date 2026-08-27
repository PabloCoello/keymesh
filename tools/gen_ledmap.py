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

NAV_MOVE  = (140, 255, 200)   # flechas y saltos de texto
NAV_EDIT  = (85, 255, 190)    # deshacer, copiar, pegar
NAV_FN    = (0, 0, 120)       # teclas de función
NAV_WIN   = (20, 255, 220)    # ventanas, escritorios, aplicaciones
NAV_MOD   = (190, 200, 170)   # cluster de modificadores

SYM_LEFT  = (35, 255, 195)    # delimitadores y símbolos de programación
SYM_RIGHT = (10, 220, 195)    # operadores y puntuación
SYM_MEDIA = (215, 220, 185)   # volumen y reproducción

META_SYS  = (0, 255, 200)     # arranque, EEPROM
META_OS   = (128, 255, 210)   # selección de host
META_RGB  = (43, 255, 175)    # LEDs
META_HRD  = (170, 255, 215)   # Herdr
META_WIN  = (20, 255, 220)    # mover ventanas entre pantallas


def is_blank(k):
    return k in ("KC_TRANSPARENT", "KC_NO", "KC_TRNS")


def color_base(k):
    if k in ("U_APP", "KC_RIGHT_CTRL"):
        return MODSHIFT
    return LETTER


def color_nav(k):
    if k.startswith("KC_F") and k[4:].isdigit():
        return NAV_FN
    if k in ("KC_LEFT_GUI", "KC_LEFT_ALT", "KC_LEFT_CTRL", "KC_LEFT_SHIFT", "KC_RIGHT_ALT"):
        return NAV_MOD
    if k in ("U_APPSW", "U_WINN", "U_DESKL", "U_DESKR", "U_MSN"):
        return NAV_WIN
    if k in ("U_UNDO", "U_REDO", "U_CUT", "U_COPY", "U_PASTE", "U_ZIN", "U_ZOUT", "U_SHOT"):
        return NAV_EDIT
    if k.startswith("LCTL("):
        return NAV_EDIT
    return NAV_MOVE


def color_sym(idx, k):
    if k.startswith("KC_AUDIO") or k.startswith("KC_MEDIA"):
        return SYM_MEDIA
    col = idx % 12 if idx < 48 else 0
    return SYM_LEFT if col < 6 else SYM_RIGHT


def color_meta(k):
    if k.startswith("HRD_"):
        return META_HRD
    if k.startswith("U_DISP"):
        return META_WIN
    if k.startswith("U_OS"):
        return META_OS
    if k.startswith("RGB_") or k.startswith("RM_") or k == "TOGGLE_LAYER_COLOR":
        return META_RGB
    if k in ("QK_BOOT", "EE_CLR"):
        return META_SYS
    return (0, 0, 140)


out = []
out.append("// GENERADO por gen_ledmap.py. No editar a mano.")
out.append("// Cada capa ilumina solo las teclas que hace algo. En la capa BASE el")
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
        elif name == "L_NAV":
            c = color_nav(k)
        elif name == "L_SYM":
            c = color_sym(idx, k)
        else:
            c = color_meta(k)
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
