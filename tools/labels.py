"""Etiquetas y chords del layout. Compartido por el generador de la
chuleta y por check.py, para que no haya dos copias.
"""

LAYER_TITLES = {
    "L_BASE": ("Base", "Letras, dígitos y los dos modificadores"),
    "L_NAV": ("Nav", "Pulgar izquierdo interior"),
    "L_SYM": ("Sym", "Pulgar derecho interior"),
    "L_META": ("Meta", "Toca Nav y luego Sym, o mantén los dos"),
}

LABELS = {
    "KC_TRANSPARENT": "", "KC_NO": "", "KC_ESCAPE": "Esc", "KC_TAB": "Tab",
    "KC_ENTER": "Enter", "KC_BSPC": "Retr", "KC_SPACE": "Espacio",
    "KC_DELETE": "Supr", "KC_COMMA": ",", "KC_DOT": ".",
    "KC_LEFT_SHIFT": "Shift", "KC_RIGHT_SHIFT": "Shift",
    "KC_LEFT_CTRL": "Ctrl", "KC_RIGHT_CTRL": "Ctrl",
    "KC_LEFT_GUI": "Gui", "KC_LEFT_ALT": "Alt", "KC_RIGHT_ALT": "AltGr",
    "KC_PAGE_UP": "PgUp", "KC_PGDN": "PgDn",
    "KC_UP": "↑", "KC_DOWN": "↓", "KC_LEFT": "←", "KC_RIGHT": "→",
    "KC_AUDIO_VOL_DOWN": "Vol−", "KC_AUDIO_VOL_UP": "Vol+",
    "KC_AUDIO_MUTE": "Mute", "KC_MEDIA_PLAY_PAUSE": "Play",
    "KC_MEDIA_PREV_TRACK": "Ant", "KC_MEDIA_NEXT_TRACK": "Sig",
    "LCTL(KC_TAB)": "Pest →", "LCTL(LSFT(KC_TAB))": "Pest ←",
    "ES_NTIL": "ñ", "ES_ACUT": "´", "ES_MINS": "-", "ES_IEXL": "¡",
    "ES_IQUE": "¿", "ES_QUOT": "'", "ES_QUES": "?", "ES_GRV": "`",
    "ES_PIPE": "|", "ES_AT": "@", "ES_HASH": "#", "ES_TILD": "~",
    "ES_AMPR": "&", "ES_LCBR": "{", "ES_LBRC": "[", "ES_LPRN": "(",
    "ES_LABK": "<", "ES_EQL": "=", "ES_RCBR": "}", "ES_RBRC": "]",
    "ES_RPRN": ")", "ES_RABK": ">", "ES_EURO": "€", "ES_DQUO": '"',
    "ES_PERC": "%", "ES_DLR": "$", "ES_UNDS": "_", "ES_PLUS": "+",
    "ES_SLSH": "/", "ES_ASTR": "*", "ES_MORD": "º", "ES_CIRC": "^",
    "ES_DIAE": "¨", "ES_SCLN": ";", "ES_COLN": ":", "ES_CCED": "ç",
    "U_APP": "App", "U_BSLS": "\\", "U_UNDO": "Undo", "U_REDO": "Redo",
    "U_CUT": "Cortar", "U_COPY": "Copiar", "U_PASTE": "Pegar",
    "U_WLFT": "⇤ pal", "U_WRGT": "pal ⇥", "U_LNST": "Inicio",
    "U_LNEND": "Fin", "U_DWBK": "Borra pal", "U_APPSW": "App ↹",
    "U_WINN": "Ventana", "U_DESKL": "Escr ←", "U_DESKR": "Escr →",
    "U_MSN": "Exposé", "U_DISPL": "Pant ←", "U_DISPR": "Pant →",
    "U_ZIN": "Zoom +", "U_ZOUT": "Zoom −", "U_SHOT": "Captura",
    "U_OSAUTO": "OS auto", "U_OSMAC": "OS mac", "U_OSWIN": "OS win",
    "U_OSLIN": "OS lin", "U_OSDBG": "OS info",
    "RM_TOGG": "LED on", "RM_NEXT": "LED modo", "RM_HUEU": "Tono +",
    "RM_HUED": "Tono −", "RM_VALU": "Brillo +", "RM_VALD": "Brillo −",
    "RGB_SLD": "LED fijo", "TOGGLE_LAYER_COLOR": "LED capa",
    "QK_BOOT": "FLASH", "EE_CLR": "Borra EE",
    "TT(L_NAV)": "Nav", "TT(L_SYM)": "Sym",
}

CHORDS = {
    "U_APP":    ("Cmd", "Ctrl", "Ctrl"),
    "U_UNDO":   ("Cmd Z", "Ctrl Z", "Ctrl Z"),
    "U_REDO":   ("Cmd ⇧ Z", "Ctrl ⇧ Z", "Ctrl ⇧ Z"),
    "U_CUT":    ("Cmd X", "Ctrl X", "Ctrl X"),
    "U_COPY":   ("Cmd C", "Ctrl C", "Ctrl C"),
    "U_PASTE":  ("Cmd V", "Ctrl V", "Ctrl V"),
    "U_WLFT":   ("Opt ←", "Ctrl ←", "Ctrl ←"),
    "U_WRGT":   ("Opt →", "Ctrl →", "Ctrl →"),
    "U_LNST":   ("Cmd ←", "Home", "Home"),
    "U_LNEND":  ("Cmd →", "End", "End"),
    "U_DWBK":   ("Opt Retr", "Ctrl Retr", "Ctrl Retr"),
    "U_WINN":   ("Cmd º", "Alt Tab", "Alt º"),
    "U_DESKL":  ("Ctrl ←", "Win Ctrl ←", "Super PgUp"),
    "U_DESKR":  ("Ctrl →", "Win Ctrl →", "Super PgDn"),
    "U_MSN":    ("Ctrl ↑", "Win Tab", "Super"),
    "U_DISPL":  ("Ctrl Opt Cmd ←", "Win ⇧ ←", "⇧ Super ←"),
    "U_DISPR":  ("Ctrl Opt Cmd →", "Win ⇧ →", "⇧ Super →"),
    "U_ZIN":    ("Cmd +", "Ctrl +", "Ctrl +"),
    "U_ZOUT":   ("Cmd −", "Ctrl −", "Ctrl −"),
    "U_SHOT":   ("Cmd ⇧ 4", "Win ⇧ S", "ImprPant"),
    "U_BSLS":   ("AltGr 6", "AltGr º", "AltGr º"),
    "U_APPSW":  ("Cmd Tab sostenido", "Alt Tab sostenido", "Alt Tab sostenido"),
}

HERDR = {
    "HRD_PFX": ("Prefijo", "Ctrl B"),
    "HRD_LEFT": ("Panel ←", "Ctrl Alt H"),
    "HRD_DOWN": ("Panel ↓", "Ctrl Alt J"),
    "HRD_UP": ("Panel ↑", "Ctrl Alt K"),
    "HRD_RIGHT": ("Panel →", "Ctrl Alt L"),
    "HRD_ZOOM": ("Zoom", "Ctrl Alt Z"),
    "HRD_SPLV": ("Divide │", "Ctrl Alt D"),
    "HRD_SPLH": ("Divide ─", "Ctrl Alt ⇧ D"),
    "HRD_CLOSE": ("Cierra", "Ctrl Alt X"),
    "HRD_NEW": ("Nueva pest.", "Ctrl Alt C"),
    "HRD_TABP": ("Pestaña ←", "Ctrl Alt P"),
    "HRD_TABN": ("Pestaña →", "Ctrl Alt N"),
    "HRD_WS": ("Espacios", "Ctrl Alt W"),
    "HRD_GOTO": ("Ir a…", "Ctrl Alt G"),
    "HRD_DETACH": ("Desacopla", "Ctrl Alt Q"),
}


# Sub-etiquetas fijas, para teclas cuyo comportamiento no se ve en el nombre.
SUBS = {
    "TT(L_NAV)": "toque fija",
    "TT(L_SYM)": "toque fija",
}

# Lo que escribe cada tecla al pulsarla con Shift, para las que producen un
# símbolo distinto y no solo la mayúscula. Es la mitad del layout que no se ve
# en ninguna capa: la fila de números no duplica sus símbolos en Sym, así que
# sin esto la chuleta no dice de dónde salen ! " $ % & / ( ) =.
#
# El resultado de Shift es el mismo en el español ISO de PC y en el de macOS,
# a diferencia de la capa de AltGr. Por eso esta tabla no depende del host.
SHIFTED = {
    "KC_1": "!", "KC_2": '"', "KC_3": "·", "KC_4": "$", "KC_5": "%",
    "KC_6": "&", "KC_7": "/", "KC_8": "(", "KC_9": ")", "KC_0": "=",
    "ES_MINS": "_", "KC_COMMA": ";", "KC_DOT": ":", "ES_ACUT": "¨",
    "ES_QUOT": "?", "ES_IEXL": "¿", "ES_GRV": "^", "ES_MORD": "ª",
    "ES_PLUS": "*", "ES_LABK": ">",
}
