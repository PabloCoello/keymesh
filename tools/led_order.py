"""Correspondencia entre el orden del keymap y el orden de los LEDs.

`LAYOUT_voyager` enumera las teclas fila por fila alternando mitades: los seis
de la izquierda, los seis de la derecha, la fila siguiente. El indice de LED de
`rgb_matrix` recorre la mitad izquierda entera y luego la derecha. Los dos
ordenes no coinciden, y `set_layer_color()` en keymap.c indexa por LED: sin
esta permutacion el color sale en la tecla equivocada en 44 de las 52.

Derivado de `keyboards/zsa/voyager/keyboard.json` de la rama firmware24:
`layouts.LAYOUT.layout` da el orden del keymap y `rgb_matrix.layout` el de los
LEDs, y ambas entradas traen su posicion de matriz, que es lo que permite
cruzarlas. La tabla se versiona aqui para que `make check` no dependa de tener
qmk_firmware descargado; `verify()` la contrasta con el fichero real cuando si
lo esta, que es lo que evita que se desvie en silencio.
"""

KEY_COUNT = 52

# Primera tecla de cada fila de seis, en indices de keymap.
_LEFT_ROWS = (0, 12, 24, 36)
_RIGHT_ROWS = (6, 18, 30, 42)
_LEFT_THUMBS = (48, 49)
_RIGHT_THUMBS = (50, 51)

# Indice de LED -> indice de keymap.
LED_TO_KEY = tuple(
    [k for r in _LEFT_ROWS for k in range(r, r + 6)]
    + list(_LEFT_THUMBS)
    + [k for r in _RIGHT_ROWS for k in range(r, r + 6)]
    + list(_RIGHT_THUMBS)
)

# Indice de keymap -> indice de LED.
KEY_TO_LED = tuple(LED_TO_KEY.index(k) for k in range(KEY_COUNT))

assert sorted(LED_TO_KEY) == list(range(KEY_COUNT)), "LED_TO_KEY no es una permutacion"


def to_led_order(seq):
    """Reordena una secuencia en orden de keymap al orden de los LEDs."""
    if len(seq) != KEY_COUNT:
        raise ValueError(f"se esperaban {KEY_COUNT} elementos, hay {len(seq)}")
    return [seq[LED_TO_KEY[i]] for i in range(KEY_COUNT)]


def to_key_order(seq):
    """Reordena una secuencia en orden de LED al orden del keymap."""
    if len(seq) != KEY_COUNT:
        raise ValueError(f"se esperaban {KEY_COUNT} elementos, hay {len(seq)}")
    return [seq[KEY_TO_LED[k]] for k in range(KEY_COUNT)]


def verify(qmk_root):
    """Contrasta la tabla con keyboard.json. Devuelve None si cuadra, o el motivo.

    Devuelve None tambien si no encuentra el fichero: es una verificacion
    oportunista, no un requisito para poder generar.
    """
    import json
    import os

    path = os.path.join(qmk_root, "keyboards", "zsa", "voyager", "keyboard.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        keys = [tuple(k["matrix"]) for k in data["layouts"]["LAYOUT"]["layout"]]
        leds = [tuple(l["matrix"]) for l in data["rgb_matrix"]["layout"]]
    except (KeyError, TypeError, ValueError) as exc:
        return f"no se pudo leer {path}: {exc}"

    if len(keys) != KEY_COUNT or len(leds) != KEY_COUNT:
        return f"{path} declara {len(keys)} teclas y {len(leds)} LEDs, se esperaban {KEY_COUNT}"
    if set(keys) != set(leds):
        return f"{path}: el keymap y los LEDs no cubren las mismas posiciones de matriz"

    real = [keys.index(m) for m in leds]
    if real != list(LED_TO_KEY):
        return (f"{path}: la permutacion real no coincide con LED_TO_KEY.\n"
                f"  real: {real}\n"
                f"  aqui: {list(LED_TO_KEY)}")
    return None
