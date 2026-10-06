#!/usr/bin/env python3
"""Genera chuleta.html leyendo keymap.c y ledmap.h.

Los colores de las teclas son los mismos valores HSV que el firmware manda a
los LEDs, convertidos a hex. Así el papel y el teclado coinciden.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import colorsys
import json
import re

KEYMAP = os.path.join(ROOT, "keymap.c")
LEDMAP = os.path.join(ROOT, "ledmap.h")
DST = os.path.join(ROOT, "chuleta.html")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import LAYER_TITLES, LABELS, CHORDS, HERDR, SUBS, SHIFTED
from led_order import to_key_order

# Tonos base por sistema, replicando base_hue() de keymap.c
BASE_HUE = {"mac": 128, "win": 160, "lin": 20}


# Etiqueta corta de cada tecla

# Chord real por sistema. Espeja os_chord() de keymap.c.


def split_args(body):
    body = re.sub(r"//[^\n]*", "", body)
    out, depth, cur = [], 0, ""
    for ch in body:
        if ch == "(":
            depth += 1
            cur += ch
        elif ch == ")":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return [x for x in out if x]


def brace_body(text, start_paren):
    depth = 0
    for j in range(start_paren, len(text)):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return text[start_paren + 1:j]
    raise ValueError("sin cierre")


src = open(KEYMAP, encoding="utf-8").read()

# --- capas ---
layers = []
for m in re.finditer(r"\[(L_\w+)\]\s*=\s*LAYOUT_voyager\(", src):
    i = src.index("(", m.end() - 1)
    layers.append((m.group(1), split_args(brace_body(src, i))))

for name, keys in layers:
    assert len(keys) == 52, (name, len(keys))

# --- comprobación de deriva: cada keycode con chord debe existir en el enum ---
enum_block = src[src.index("enum custom_keycodes"):src.index("// ---", src.index("enum custom_keycodes"))]
enum_names = set(re.findall(r"\b(U_[A-Z_]+|HRD_[A-Z_]+)\b", enum_block))
unknown = (set(CHORDS) | set(HERDR)) - enum_names
assert not unknown, f"en la tabla pero no en el firmware: {sorted(unknown)}"
used = {k for _, keys in layers for k in keys if k.startswith(("U_", "HRD_"))}
missing = used - set(CHORDS) - set(HERDR) - {
    "U_OSAUTO", "U_OSMAC", "U_OSWIN", "U_OSLIN", "U_OSDBG"}
assert not missing, f"en el firmware pero sin describir: {sorted(missing)}"

# --- ledmap ---
led_src = open(LEDMAP, encoding="utf-8").read()
led = {}
for m in re.finditer(r"\[(L_\w+)\]\s*=\s*\{(.*?)\},\s*\n", led_src, re.S):
    trips = re.findall(r"\{(\d+),(\d+),(\d+)\}", m.group(2))
    trips = [tuple(int(x) for x in t) for t in trips]
    assert len(trips) == 52, m.group(1)
    # ledmap.h esta en orden de LED; la chuleta dibuja en orden de keymap.
    led[m.group(1)] = to_key_order(trips)
for name, _ in layers:
    assert len(led[name]) == 52, name


def hsv_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 255.0, s / 255.0, v / 255.0)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def label(k):
    if k in LABELS:
        return LABELS[k]
    if k in HERDR:
        return HERDR[k][0]
    m = re.match(r"^KC_F(\d+)$", k)
    if m:
        return "F" + m.group(1)
    m = re.match(r"^KC_(\w)$", k)
    if m:
        return m.group(1)
    return k


# --- construye el modelo que consume el HTML ---
model = {"layers": [], "baseHue": BASE_HUE}
for name, keys in layers:
    entry = {"id": name, "title": LAYER_TITLES[name][0],
             "how": LAYER_TITLES[name][1], "keys": []}
    for idx, k in enumerate(keys):
        h, s, v = led[name][idx]
        key = {"label": label(k), "code": k, "off": v == 0}
        if name == "L_BASE" and not key["off"]:
            key["hueOffset"] = h
            key["sat"] = s
            key["val"] = v
        else:
            key["color"] = hsv_hex(h, s, v) if v else None
        if k in CHORDS:
            key["chords"] = list(CHORDS[k])
            key["osdep"] = True
        elif k in HERDR:
            key["sub"] = HERDR[k][1]
        elif k in SUBS:
            key["sub"] = SUBS[k]
        elif k in SHIFTED:
            key["sub"] = "\u21e7 " + SHIFTED[k]
        entry["keys"].append(key)
    model["layers"].append(entry)

data = json.dumps(model, ensure_ascii=False, separators=(",", ":"))

# Escalonado de columnas, en px. col 1 es el meñique, col 6 el índice interior.
STAGGER = [10, 6, 0, 6, 12, 16]

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Voyager — chuleta del layout</title>
<style>
  :root {{
    --ink: #e8e6e1;
    --dim: #6f6b66;
    --line: #26241f;
    --bg: #100f0d;
    --panel: #171613;
  }}
  * {{ box-sizing: border-box; }}
  html {{ background: var(--bg); }}
  body {{
    margin: 0;
    padding: 40px 28px 80px;
    background: var(--bg);
    color: var(--ink);
    font: 400 14px/1.5 ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 1180px; margin: 0 auto; }}

  header {{ border-bottom: 1px solid var(--line); padding-bottom: 22px; margin-bottom: 8px; }}
  h1 {{
    margin: 0 0 6px;
    font-size: 13px; font-weight: 700;
    letter-spacing: 0.34em; text-transform: uppercase;
  }}
  .lede {{ margin: 0; color: var(--dim); font-size: 13px; max-width: 62ch; }}

  /* Selector de sistema: no es decoración, cambia los chords y el color base */
  .hosts {{ display: flex; gap: 0; margin: 26px 0 4px; border: 1px solid var(--line); width: fit-content; }}
  .hosts button {{
    appearance: none; background: transparent; border: 0;
    border-right: 1px solid var(--line);
    color: var(--dim); cursor: pointer;
    font: inherit; font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
    padding: 11px 20px 10px;
  }}
  .hosts button:last-child {{ border-right: 0; }}
  .hosts button[aria-pressed="true"] {{ color: #14120f; }}
  .hosts button:focus-visible {{ outline: 2px solid var(--ink); outline-offset: -2px; }}
  .hostnote {{ color: var(--dim); font-size: 12px; margin: 0 0 34px; }}

  .layer {{ margin: 0 0 46px; }}
  .layer > hgroup {{ display: flex; align-items: baseline; gap: 16px; margin-bottom: 16px; }}
  .layer h2 {{
    margin: 0; font-size: 12px; font-weight: 700;
    letter-spacing: 0.3em; text-transform: uppercase;
  }}
  .layer .how {{ color: var(--dim); font-size: 12px; }}

  .board {{ display: flex; gap: 62px; justify-content: center; }}
  .half {{ display: flex; gap: 5px; }}
  .col {{ display: flex; flex-direction: column; gap: 5px; }}

  .key {{
    width: 74px; height: 52px;
    border: 1px solid var(--line);
    border-radius: 4px;
    background: var(--panel);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 2px; padding: 3px;
    text-align: center;
    overflow: hidden;
  }}
  .key .lb {{ font-size: 12px; line-height: 1.15; }}
  .key .sb {{ font-size: 9px; line-height: 1.1; opacity: 0.72; letter-spacing: 0.02em; }}
  .key.off {{ opacity: 0.2; }}
  .key.trans .lb {{ color: var(--dim); }}
  /* Las teclas cuyo chord depende del sistema llevan una marca en la esquina */
  .key.osdep {{ position: relative; }}
  .key.osdep::after {{
    content: ""; position: absolute; top: 4px; right: 4px;
    width: 4px; height: 4px; border-radius: 50%;
    background: currentColor; opacity: 0.55;
  }}

  .thumbs {{ display: flex; justify-content: center; gap: 62px; margin-top: 7px; }}
  .thumbs .side {{ display: flex; gap: 5px; }}
  .thumbs .side.l {{ margin-left: 210px; }}
  .thumbs .side.r {{ margin-right: 210px; }}

  footer {{ border-top: 1px solid var(--line); padding-top: 20px; color: var(--dim); font-size: 12px; }}
  footer p {{ margin: 0 0 8px; max-width: 74ch; }}
  code {{ color: var(--ink); }}

  @media (max-width: 1080px) {{
    body {{ padding: 24px 14px 60px; }}
    .board {{ gap: 26px; }}
    .key {{ width: 58px; height: 46px; }}
    .key .lb {{ font-size: 11px; }}
    .thumbs {{ gap: 26px; }}
    .thumbs .side.l {{ margin-left: 120px; }}
    .thumbs .side.r {{ margin-right: 120px; }}
  }}
  @media (max-width: 720px) {{
    .board, .thumbs {{ flex-direction: column; align-items: center; gap: 14px; }}
    .thumbs .side.l, .thumbs .side.r {{ margin: 0; }}
  }}
  @media print {{
    body {{ padding: 0; }}
    * {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .hosts, .hostnote {{ display: none; }}
    .layer {{ break-inside: avoid; page-break-inside: avoid; }}
  }}
  @media (prefers-reduced-motion: no-preference) {{
    .key {{ transition: background-color 140ms ease, color 140ms ease; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Voyager · chuleta del layout</h1>
    <p class="lede">Los colores son los mismos valores que el firmware manda a los LEDs, así que
    el papel y el teclado coinciden. Generada desde <code>keymap.c</code>.</p>
  </header>

  <div class="hosts" role="group" aria-label="Sistema anfitrión">
    <button type="button" data-os="mac" aria-pressed="true">macOS</button>
    <button type="button" data-os="win" aria-pressed="false">Windows</button>
    <button type="button" data-os="lin" aria-pressed="false">Ubuntu</button>
  </div>
  <p class="hostnote">El punto en la esquina de una tecla significa que su chord depende del
  sistema. El color de la capa Base es el que verás encendido tras conmutar el KVM.
  Nav y Sym solo están activas mientras las mantienes; Meta, mientras mantienes las dos.</p>

  <main id="layers"></main>

  <footer>
    <p>La línea pequeña con <code>\u21e7</code> es lo que escribe esa tecla con Shift. La fila
    de números no duplica sus símbolos en Sym: <code>! " $ % &amp; ( ) =</code> se sacan con
    Shift, como en cualquier teclado. Shift da lo mismo en el español de PC y en el de
    macOS, así que esa línea no cambia al conmutar de sistema.</p>
    <p>Meta se enciende cuando Nav y Sym están activas a la vez: toca una y luego
    la otra, o mantén los dos pulgares. Para salir del todo hay que apagar las dos.</p>
    <p><code>OS info</code> escribe el sistema detectado. Si no acierta tras conmutar el
    ATEN, fuérzalo con <code>OS mac</code>, <code>OS win</code> u <code>OS lin</code>.</p>
  </footer>
</div>

<script>
const MODEL = {data};
const STAGGER = {json.dumps(STAGGER)};
const OS_INDEX = {{ mac: 0, win: 1, lin: 2 }};
const HOST_LABEL = {{ mac: "macOS", win: "Windows", lin: "Ubuntu" }};
let currentOs = "mac";

function hsvToHex(h, s, v) {{
  h = ((h % 256) + 256) % 256;
  const hh = (h / 255) * 6, i = Math.floor(hh), f = hh - i;
  const sn = s / 255, vn = v / 255;
  const p = vn * (1 - sn), q = vn * (1 - sn * f), t = vn * (1 - sn * (1 - f));
  const c = [[vn,t,p],[q,vn,p],[p,vn,t],[p,q,vn],[t,p,vn],[vn,p,q]][i % 6];
  return "#" + c.map(x => Math.round(x * 255).toString(16).padStart(2, "0")).join("");
}}

function readable(hex) {{
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  return (0.299 * r + 0.587 * g + 0.114 * b) > 140 ? "#14120f" : "#f2f0ec";
}}

function keyEl(k, layerId) {{
  const el = document.createElement("div");
  el.className = "key";
  if (k.off) el.classList.add("off");
  if (k.code === "KC_TRANSPARENT") el.classList.add("trans");
  if (k.osdep) el.classList.add("osdep");

  let bg = null;
  if (layerId === "L_BASE" && !k.off) {{
    bg = hsvToHex(MODEL.baseHue[currentOs] + k.hueOffset, k.sat, k.val);
  }} else if (k.color) {{
    bg = k.color;
  }}
  if (bg) {{
    el.style.background = bg;
    el.style.color = readable(bg);
    el.style.borderColor = "transparent";
  }}

  const lb = document.createElement("div");
  lb.className = "lb";
  lb.textContent = k.code === "KC_TRANSPARENT" ? "·" : k.label;
  el.appendChild(lb);

  const sub = k.chords ? k.chords[OS_INDEX[currentOs]] : k.sub;
  if (sub) {{
    const sb = document.createElement("div");
    sb.className = "sb";
    sb.textContent = sub;
    el.appendChild(sb);
  }}
  return el;
}}

function render() {{
  const root = document.getElementById("layers");
  root.textContent = "";
  for (const layer of MODEL.layers) {{
    const sec = document.createElement("section");
    sec.className = "layer";

    const hg = document.createElement("hgroup");
    const h2 = document.createElement("h2");
    h2.textContent = layer.title;
    const how = document.createElement("span");
    how.className = "how";
    how.textContent = layer.how;
    hg.append(h2, how);
    sec.appendChild(hg);

    const board = document.createElement("div");
    board.className = "board";
    for (const side of [0, 1]) {{
      const half = document.createElement("div");
      half.className = "half";
      for (let c = 0; c < 6; c++) {{
        const col = document.createElement("div");
        col.className = "col";
        const physical = side === 0 ? c : 5 - c;
        col.style.marginTop = STAGGER[physical] + "px";
        for (let r = 0; r < 4; r++) {{
          col.appendChild(keyEl(layer.keys[r * 12 + side * 6 + c], layer.id));
        }}
        half.appendChild(col);
      }}
      board.appendChild(half);
    }}
    sec.appendChild(board);

    const th = document.createElement("div");
    th.className = "thumbs";
    for (const side of [0, 1]) {{
      const s = document.createElement("div");
      s.className = "side " + (side === 0 ? "l" : "r");
      for (const i of side === 0 ? [48, 49] : [50, 51]) {{
        s.appendChild(keyEl(layer.keys[i], layer.id));
      }}
      th.appendChild(s);
    }}
    sec.appendChild(th);
    root.appendChild(sec);
  }}
}}

for (const btn of document.querySelectorAll(".hosts button")) {{
  btn.addEventListener("click", () => {{
    currentOs = btn.dataset.os;
    for (const b of document.querySelectorAll(".hosts button")) {{
      const on = b === btn;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.style.background = on ? hsvToHex(MODEL.baseHue[currentOs], 190, 210) : "transparent";
    }}
    render();
  }});
}}
document.querySelector('.hosts button[data-os="mac"]').style.background =
  hsvToHex(MODEL.baseHue.mac, 190, 210);
render();
</script>
</body>
</html>
"""

open(DST, "w", encoding="utf-8").write(html)
print(f"escrito {DST} ({len(html)} bytes)")
print(f"capas: {[l['id'] for l in model['layers']]}")
print(f"teclas dependientes del sistema: {len(CHORDS)} | teclas de Herdr: {len(HERDR)}")
