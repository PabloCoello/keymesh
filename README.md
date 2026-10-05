# Voyager: layout multiplataforma (Windows / Ubuntu / macOS)

Reescritura del layout `mXGVj/6aMO7E` para que el mismo firmware se comporte
bien en los tres sistemas que conmutas con el ATEN, con capa dedicada para
Herdr.

---

## 1. Los dos errores que había

**El swap de Cmd y Ctrl en macOS es la causa de tu bug de pestañas.** macOS
aplica el remapeo de modificadores por dispositivo, a nivel HID, así que afecta
a todo lo que envía el Voyager. Tu tecla de siguiente pestaña era
`LCTL(KC_TAB)`; con el swap llega al sistema como Cmd+Tab, que es el conmutador
de aplicaciones. No es que la tecla esté mal: es que el swap la reescribe.

El mismo swap rompe otras cosas, y esto importa más ahora que usas Herdr:

| Lo que quieres pulsar | Lo que llega a macOS con el swap |
|---|---|
| Ctrl+B (prefijo de Herdr) | Cmd+B |
| Ctrl+Alt+H (chord directo de Herdr) | Cmd+Alt+H |
| Ctrl+←/→ (cambiar de Space) | Cmd+←/→ |
| Ctrl+A, Ctrl+C, Ctrl+R en terminal | Cmd+A, Cmd+C, Cmd+R |

**El backslash solo funcionaba en macOS.** Tu tecla de `\` era `ES_BSLS_MAC`,
que Oryx define como AltGr+6. En el layout español de PC, AltGr+6 es `¬`.
Verificado contra `quantum/keymap_extras/keymap_spanish.h` de QMK, que define
`ES_NOT = ALGR(ES_6)` y `ES_BSLS = ALGR(ES_MORD)`. En Windows y Ubuntu esa
tecla te escribía `¬`.

---

## 2. Paso obligatorio antes de flashear

Quita el intercambio de Cmd y Ctrl en macOS:

    Ajustes del Sistema → Teclado → Atajos de teclado → Teclas modificadoras
    → selecciona el Voyager en el desplegable → deja todo en el valor por defecto

Si no lo quitas, este firmware se comportará al revés en macOS. El swap ahora
lo hace el teclado, no el sistema, y solo donde hace falta.

---

## 3. Cómo funciona ahora

El firmware detecta el sistema anfitrión (`OS_DETECTION_ENABLE`, disponible en
la rama `firmware24` del fork de ZSA) y resuelve cada atajo en tiempo de
ejecución. Hay tres piezas:

**Un modificador de aplicación.** La tecla de Bloq Mayús es ahora `U_APP`:
manda Cmd en macOS y Ctrl en Windows y Linux. Es la tecla de copiar, pegar,
guardar, buscar. Su significado es el mismo en los tres sistemas aunque el
código que envía cambie.

**Un Ctrl de verdad.** La tecla de arriba a la derecha es `KC_RIGHT_CTRL`, Ctrl
real en los tres sistemas. Es la que usan el prefijo de Herdr, los chords
`ctrl+alt`, Ctrl+A y Ctrl+C en terminal, y Ctrl+←/→ en macOS. Está en la mano
derecha a propósito: casi todos los atajos de terminal (Ctrl+A, B, C, D, E, R,
W, Z) son letras de la mano izquierda, así que el pulgar y el meñique no
compiten.

**Keycodes semánticos.** Donde el atajo no es "el mismo con otro modificador"
sino un chord distinto, hay un keycode propio que se resuelve por sistema:

| Tecla | macOS | Windows | Ubuntu (GNOME) |
|---|---|---|---|
| Inicio / Fin de línea | Cmd+←/→ | Home / End | Home / End |
| Palabra izq./der. | Opt+←/→ | Ctrl+←/→ | Ctrl+←/→ |
| Borrar palabra atrás | Opt+Retroceso | Ctrl+Retroceso | Ctrl+Retroceso |
| Escritorio ant./sig. | Ctrl+←/→ | Win+Ctrl+←/→ | Super+PgUp/PgDn |
| Siguiente ventana de la app | Cmd+º | Alt+Tab | Alt+º |
| Exposé / Task View | Ctrl+↑ | Win+Tab | Super |
| Mover a la otra pantalla | Ctrl+Opt+Cmd+←/→ | Win+Shift+←/→ | Shift+Super+←/→ |
| Captura de región | Cmd+Shift+4 | Win+Shift+S | ImprPant |
| Backslash | AltGr+6 | AltGr+º | AltGr+º |

El caso de Inicio/Fin es el que más se nota al escribir: en macOS, Home y End
van al principio y al final del documento, no de la línea. Ahora la misma tecla
hace lo mismo en los tres sistemas.

**Conmutador de aplicaciones que funciona.** `App↹` mantiene el modificador
(Cmd en mac, Alt en PC) durante 900 ms tras el último toque, así que puedes
recorrer la lista con toques repetidos en vez de que se cierre al soltar. Es lo
que no puede hacer un simple `LGUI(KC_TAB)`.

**El color de la capa base indica el host.** Al conmutar el ATEN el teclado se
reinicia y vuelve a detectar. El color te dice qué semántica está activa:
cian para macOS, azul para Windows, naranja para Linux, rojo tenue si no ha
podido determinarlo. Las dos teclas modificadoras salen con un tono desplazado.

---

## 4. Las cuatro capas

`★` marca las teclas cuyo comportamiento depende del host.
`·` es transparente (pasa a la capa de abajo). Los huecos están apagados.

### BASE

```
       Esc           1           2           3           4           5   ║            6           7           8           9           0   Ctrl-real
       Tab           Q           W           E           R           T   ║            Y           U           I           O           P       Enter
      App★           A           S           D           F           G   ║            H           J           K           L           ñ           ´
     Shift           Z           X           C           V           B   ║            N           M           ,           .           -       Shift
                                                      Retr        →NAV   ║         →SYM     Espacio
```

### NAV

```
       Esc          F1          F2          F3          F4          F5   ║           F6          F7          F8          F9         F10         F11
       Tab       Pest←       Pest→       Zoom−       Zoom+     Captura   ║       Inicio        PgUp           ↑        PgDn         Fin       Enter
         ·         Gui         Alt        Ctrl       Shift       AltGr   ║         ⇤pal           ←           ↓           →        pal⇥        Supr
         ·        Undo      Cortar      Copiar       Pegar        Redo   ║         App↹    Ventana→       Escr←       Escr→      Exposé           ·
                                                 Borra-pal           ·   ║            ·     Espacio
```

### SYM

```
         ·           ·           ·           ·           ·           `   ║            €           ·           ·           '           ¡           ·
         ·           |           @           #           ~           &   ║            +           -           /           *           º       Enter
         ·           {           [           (           <           =   ║         Vol−        Vol+        Mute        Play         Ant         Sig
         ·           }           ]           )           >           \   ║            ^           ¨           ;           :           ç           ·
                                                      Retr           ·   ║            ·     Espacio
```

### META

```
     FLASH                                           Pant←       Pant→   ║                                                                         
               OS:auto      OS:mac      OS:win      OS:lin     OS:info   ║       H:splh      H:splv       H:new      H:tabp      H:tabn       Enter
                LED on    LED modo       Tono+     Brillo+    LED capa   ║       H:left      H:down        H:up     H:right      H:zoom            
              Borra EE    LED fijo       Tono−     Brillo−               ║        H:pfx     H:close    H:detach        H:ws      H:goto            
                                                                     ·   ║            ·            
```

**META se enciende cuando NAV y SYM están activas a la vez.** No consume
ninguna tecla: es un tri-layer. Con `TAPPING_TOGGLE 1` hay dos formas de
llegar:

- mantener los dos pulgares interiores, y soltar al terminar;
- tocar NAV, tocar SYM, y quedarte ahí.

La segunda deja las tres capas fijadas. Para salir hay que apagar las dos:
tocar NAV la quita y META se apaga con ella, pero SYM sigue activa hasta que
la toques también.

Mano izquierda de META: mover ventanas entre pantallas, forzar el sistema
detectado, LEDs, y `FLASH` para entrar en modo bootloader.
Mano derecha: Herdr, con el foco de panel sobre las teclas h j k l reales.

`OS:info` escribe en pantalla el sistema detectado y si hay override manual.
Úsala cuando algo se comporte raro tras conmutar el KVM.

---

## 5. Qué cambia respecto a tu layout anterior

| Antes | Ahora | Motivo |
|---|---|---|
| Bloq Mayús = `KC_LEFT_CTRL` | `U_APP` | Cmd en mac, Ctrl en PC |
| Arriba dcha. = `KC_DELETE` | `KC_RIGHT_CTRL` | Delete sigue en NAV, y hacía falta un Ctrl real |
| `ES_BSLS_MAC` | `U_BSLS` | escribía `¬` en Windows y Ubuntu |
| Pestañas en NAV fila 4 (M y `,`) | NAV fila 2 (Q y W) | libera la fila 4 para ventanas y escritorios |
| `KC_HOME` / `KC_END` | `U_LNST` / `U_LNEND` | en macOS Home y End van al documento |
| `LCTL(KC_Z/X/C/V)` | `U_UNDO` / `U_CUT` / `U_COPY` / `U_PASTE` | en macOS usan Cmd |
| `LCTL(ES_PLUS/ES_MINS)` | `U_ZIN` / `U_ZOUT` | igual |
| `LALT(LGUI(LCTL(KC_4)))` | `U_SHOT` | enviaba Alt+Cmd+Ctrl+4, que no es la captura por defecto de macOS |
| `" % $ _` en SYM | fuera | son Shift+2, Shift+5, Shift+4 y Shift+`-`: se escriben con Shift desde la base |
| `¡ ¿ ' ?` en la izquierda de SYM | `' ¡` en la derecha; `¿ ?` en la fila 1 izquierda, sin Shift | `?` y `¿` son demasiado frecuentes para Sym + Shift + tecla |
| La chuleta no decía de dónde sale `! " $ % & ( ) =` | línea `⇧` bajo cada tecla | al vaciar SYM tenían que verse en alguna parte |
| Fila 4 derecha de SYM vacía | `^ ¨ ; : ç` | `¨` hace falta para ü |
| `TAPPING_TOGGLE` 5 (por defecto) | 1 | un toque fija la capa, otro la quita; mantener sigue dando momentánea |
| LEDs uniformes por capa | por tecla, y color según el host | las capas se aprenden mirándolas |
| 3 capas | 4, la nueva por tri-layer | Herdr y control del sistema |

Lo que **no** cambia: las tres filas de abajo de la mano izquierda de SYM
(delimitadores y símbolos de programación), la disposición de flechas en NAV, el
cluster de modificadores en la fila de inicio de NAV, y todas las letras y
dígitos de la capa base.

Un detalle: las pestañas siguen siendo `LCTL(KC_TAB)`, sin condicional. Ctrl+Tab
funciona igual en Chrome, Brave y Safari en los tres sistemas. El bug era el
swap, no la tecla.

---

## 6. Compilar y flashear

### Montar el entorno

Tres avisos que cuestan una tarde si los descubres por tu cuenta. Valen para los
tres sistemas; los comandos concretos van después, uno por sistema.

**El CLI de QMK tiene que correr sobre Python 3.11.** `lib/python/qmk/math.py`
usa `ast.Num`, que Python eliminó en la 3.12. Con una versión más nueva la
compilación muere en `Platform not defined` tras un
`AttributeError: module 'ast' has no attribute 'Num'`, que no dice nada útil.

**El toolchain de ARM va con la versión fija.** Se usa el prebuilt oficial de
Arm 13.3.rel1 y no el del gestor de paquetes de cada sistema: un toolchain
distinto produce un binario distinto, y con firmware conviene que eso sea una
decisión y no un efecto de lo que haya en el disco. Además trae newlib, que es
lo que le falta al `arm-none-eabi-gcc` de Homebrew; sin ella no encuentra
`stdint.h` y la compilación muere en el primer fichero de ChibiOS.

El `Makefile` lo antepone al PATH si lo encuentra bajo `~/toolchains`. Compone
el nombre del directorio con `uname`, porque Arm publica un tarball por host:
`darwin-arm64` en el Mac y `x86_64` en Ubuntu. Para usar otra versión,
descomprímela al lado y pásala por variable:

    make compile ARM_TOOLCHAIN=$HOME/toolchains/<otra-version>/bin

Si te quedas con la nueva, cambia `ARM_VERSION` en el `Makefile` y anótala aquí.

**`qmk doctor` se queja de AVR.** Falta `avr-gcc`, `avrdude` y compañía, y lo
marca como problema grave. El Voyager es ARM (STM32F303): no aplica.

#### macOS

    brew install python@3.11 hidapi dfu-util
    pipx install --python /opt/homebrew/opt/python@3.11/bin/python3.11 qmk
    qmk setup -b firmware24 -y zsa/qmk_firmware
    pipx inject qmk -r ~/qmk_firmware/requirements.txt

    mkdir -p ~/toolchains && cd ~/toolchains
    curl -fLO https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi.tar.xz
    tar -xf arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi.tar.xz

Se instala el CLI con `pipx` y no con `brew install qmk/qmk/qmk` porque la
fórmula del tap de QMK arrastra `arm-none-eabi-gcc@8` desde `osx-cross/arm`, un
segundo tap de terceros. `hidapi` lo necesita el módulo `hid` de Python;
`dfu-util` es lo que flashea el Voyager.

#### Ubuntu

Comprobado en Ubuntu 24.04 sobre x86_64.

    sudo apt install dfu-util

    uv python install 3.11
    pipx install --python "$(uv python find 3.11)" qmk

    git clone --recurse-submodules -b firmware24 \
      https://github.com/zsa/qmk_firmware.git ~/qmk_firmware
    qmk config user.qmk_home=$HOME/qmk_firmware
    pipx inject qmk $(grep -vE '^\s*#|^\s*$' ~/qmk_firmware/requirements.txt | tr '\n' ' ')

    mkdir -p ~/toolchains && cd ~/toolchains
    curl -fLO https://developer.arm.com/-/media/Files/downloads/gnu/13.3.rel1/binrel/arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi.tar.xz
    tar -xf arm-gnu-toolchain-13.3.rel1-x86_64-arm-none-eabi.tar.xz

Cuatro diferencias con macOS, todas de empaquetado:

- Ubuntu 24.04 no trae Python 3.11, solo el 3.12 del sistema. Arriba se coge
  con `uv`, que no pide sudo; el PPA `deadsnakes` sirve igual.
- `pipx inject -r` no existe hasta pipx 1.5 y Ubuntu 24.04 empaqueta la 1.4.3,
  que solo acepta la lista de paquetes en línea. De ahí el `grep`.
- `dfu-util` hace falta para compilar, no solo para flashear. El paquete trae
  `dfu-suffix`, y `builddefs/common_rules.mk` lo llama al generar el `.bin`
  porque `keyboards/zsa/voyager/rules.mk` define `DFU_SUFFIX_ARGS`. Sin él el
  firmware enlaza y luego muere con `dfu-suffix: not found`.
- En vez de `qmk setup` basta clonar el fork y apuntar `user.qmk_home`.

Para flashear hacen falta además las reglas de udev de ZSA. Las de QMK
(`util/udev/50-qmk.rules`) no sirven: cubren el DFU genérico de STM32
(`0483:df11`), y el bootloader del Voyager es `3297:0791`, como se ve en el
`DFU_ARGS` de `keyboards/zsa/voyager/rules.mk`. Copia el bloque del
[wiki de ZSA](https://github.com/zsa/wally/wiki/Linux-install) a
`/etc/udev/rules.d/50-zsa.rules` y recarga:

    sudo udevadm control --reload-rules && sudo udevadm trigger

Tienes que estar en el grupo `plugdev`. Compruébalo con `id -nG`; si no
aparece, `sudo usermod -aG plugdev $USER` y vuelve a iniciar sesión.

### El bucle de trabajo

Una vez montado QMK, el bucle de trabajo es un comando:

    make flash          # verifica, regenera, compila y flashea
    make check          # solo verifica, sin tocar el teclado
    make chuleta        # regenera la chuleta y la abre

`make check` comprueba antes de compilar que cada capa tiene 52 teclas, que
ningún keycode propio quedó sin resolver, que todos tienen etiqueta en la
chuleta, y que el fichero compila contra stubs de la API de QMK. Una coma
perdida en el array la acepta el compilador de QMK y te deja el teclado con
las teclas corridas; esto la caza en un segundo.

Si tu `qmk_firmware` no está en `~/qmk_firmware`:

    make flash QMK=/ruta/a/qmk_firmware

A mano, si prefieres:

    cd qmk_firmware
    mkdir -p keyboards/zsa/voyager/keymaps/keymesh
    cp keymap.c config.h rules.mk i18n.h ledmap.h \
       keyboards/zsa/voyager/keymaps/keymesh/
    qmk compile -kb zsa/voyager -km keymesh
    qmk flash -kb zsa/voyager -km keymesh

Sobre el fork: `os_detection` está en la rama `firmware24` del fork de ZSA, así
que compila contra ella. Si usas QMK mainline tendrás que ajustar
`TOGGLE_LAYER_COLOR`, `keyboard_config` y `rawhid_state`, que son de ZSA.

Comprobado: los cuatro `LAYOUT_voyager` tienen 52 teclas, los 42 keycodes
personalizados están declarados y resueltos, y el fichero pasa
`gcc -fsyntax-only -Wall -Wextra` contra stubs de la API de QMK.

El orden de los LEDs está verificado contra `keyboard.json` del Voyager, y no
es el de `LAYOUT_voyager`: el keymap enumera fila por fila alternando mitades y
el índice de LED recorre una mitad entera y luego la otra. `ledmap.h` se emite
ya permutado; la tabla está en `tools/led_order.py` y `make check` la contrasta
con la definición del teclado cuando encuentra `qmk_firmware`.

La compilación real también está hecha, contra la rama `firmware24` del fork de
ZSA con el toolchain de Arm 13.3.rel1: enlaza sin un solo aviso y produce un
binario de 54 478 bytes en la revisión en que se escribió esto. Es decir, todos
los keycodes del keymap existen de verdad en esa rama, no solo en los stubs; el
tamaño se mueve en cuanto tocas el keymap y no es un valor a defender.

Repetida después en Ubuntu 24.04 sobre x86_64, con la misma rama y la misma
versión del toolchain: enlaza igual de limpia y da 54 472 bytes, más los 16 del
sufijo DFU que añade `dfu-suffix`. Lo que sigue sin verificar es el
comportamiento en hardware: para eso está el protocolo de la sección 9.

Aviso: en `firmware24` los keycodes `RGB_TOG`, `RGB_MOD`, `RGB_HUI` y compañía
ya no existen. QMK los renombró a `RM_TOGG`, `RM_NEXT`, `RM_HUEU`, `RM_HUED`,
`RM_VALU`, `RM_VALD`, y en esa rama no quedan alias. El keymap usa los nombres
nuevos. Si copias trozos de layouts antiguos, te dará error de compilación ahí.

---

## 7. Ajustes en cada sistema

**macOS.** Quita el swap de modificadores (sección 2). Para mover ventanas entre
pantallas hace falta un gestor de ventanas: macOS no trae atajo nativo. Los
chords de `Pant←` y `Pant→` son los valores por defecto de Rectangle
(Ctrl+Opt+Cmd+←/→). Si usas otro, ajusta `U_DISPL` y `U_DISPR` en `keymap.c`.

Rectangle tiene dos juegos de atajos por defecto y **hay que quedarse en el
heredado de Spectacle**, que es el que deja las mitades en Cmd+Opt+flechas. El
otro, el que Rectangle llama «recomendado», pone mitades, cuartos y tercios en
Ctrl+Opt+letra, que es la familia de los chords directos de Herdr: registra
atajos globales y se come `ctrl+alt+j`, `k`, `c`, `d` y `g` antes de que Herdr
los vea. Es decir, cinco teclas de la capa META moverían ventanas en vez de
mover el foco de panel. Los dos atajos que este layout usa de verdad
(Ctrl+Opt+Cmd+←/→) son iguales en ambos juegos.

El ajuste vive en `alternateDefaultShortcuts` (`false` = Spectacle, `true` =
recomendado) y lo fija `make macos-rectangle` en dotmesh, junto con el resto de
prefs de Rectangle. `make health` avisa si alguien lo cambia.

**Ubuntu.** Comprueba en Configuración → Teclado → Atajos que Super+Page_Up y
Super+Page_Down siguen siendo cambiar de espacio de trabajo, y que
Shift+Super+←/→ es mover la ventana de monitor. GNOME ha cambiado estos
valores por defecto entre versiones. Herdr documenta que Ctrl+Alt+flechas está
ocupado por el cambio de espacio de trabajo en GNOME y que Ctrl+Alt+T abre un
terminal en Ubuntu: el keymap no usa ninguno de los dos.

Mira también las extensiones de GNOME Shell, no solo los atajos del sistema. La
extensión gTile ata por defecto las cuatro teclas de foco de panel de Herdr:

    action-contract-left    ['<Ctrl><Alt>h']
    action-contract-bottom  ['<Ctrl><Alt>j']
    action-contract-top     ['<Ctrl><Alt>k']
    action-contract-right   ['<Ctrl><Alt>l']

El síntoma es que `H:left` y compañía encogen la ventana del terminal en vez de
mover el foco de panel. Se arregla vaciando esas cuatro:

    d=~/.local/share/gnome-shell/extensions/gTile@vibou/schemas
    for k in left right top bottom; do
      GSETTINGS_SCHEMA_DIR="$d" \
        gsettings set org.gnome.shell.extensions.gtile action-contract-$k "[]"
    done

Cómo buscar estas colisiones, porque cuesta: `gsettings list-recursively` no
lista los esquemas de las extensiones, que viven fuera de la ruta por defecto, y
`dconf dump` solo guarda lo que se aparta del valor por defecto. Una extensión
con su atajo sin tocar es invisible para las dos herramientas. Hay que leer el
`.gschema.xml` de la extensión.

**Windows.** No hay que tocar nada.

---

## 8. Herdr

`herdr-config.toml` tiene el fragmento para `~/.config/herdr/config.toml`
(`%APPDATA%\herdr\config.toml` en Windows). Mantiene todos los atajos de
prefijo por defecto y añade los chords directos que coinciden con la capa META.

La familia `ctrl+alt` no es una elección arbitraria. La documentación de Herdr
0.8.2 explica que mapearon los atajos por defecto de diez terminales (Ghostty,
iTerm2, Terminal.app, kitty, WezTerm, Alacritty, Warp, Windows Terminal, GNOME
Terminal, Konsole) más los atajos globales de GNOME y KDE, y que `ctrl+alt` es
la única familia de modificadores que queda casi libre en todas partes: los
terminales no la tocan, no le afecta la composición de la tecla Option en
macOS, y se transmite incluso en terminales sin protocolo de teclado moderno.

Consecuencia práctica: toda la capa Herdr son los mismos chords en los tres
sistemas, sin una sola condicional en el firmware. Es la única parte del layout
que no necesita detección de OS.

`H:pfx` manda el prefijo `ctrl+b` a secas, para llegar a cualquier acción que no
esté en la capa. `prefix+?` te lista las activas.

Tras editar el TOML: `herdr server reload-config`.

---

## 9. Protocolo de prueba

Hazlo en los tres sistemas. Son quince minutos y cierran el 90 % de los
problemas de portabilidad.

**Símbolos.** Abre un editor de texto plano y teclea desde la capa SYM:

    \ | @ # ~ { } [ ] < > º ç ¡ ¿ ? ` € ^ ¨ ' + - / * = & ; :

Todos deben salir correctos. Los candidatos a fallar son `\`, `{`, `}`, `[`,
`]`, `@`, `#` y `~`, porque dependen de AltGr y el layout español de macOS no
coincide con el de PC en todos ellos. He verificado el backslash contra el
header de QMK; el resto los da Oryx por buenos, pero no he podido confirmar el
layout español de macOS con una fuente fiable, así que compruébalos. Si alguno
falla solo en macOS, dímelo con qué escribe en su lugar y lo convierto en
keycode condicional igual que el backslash.

**Acentos.** `´` + `a` debe dar `á`. `¨` (capa SYM) + `u` debe dar `ü`.

**Modificadores.** Con `U_APP`: copiar, pegar y guardar en cualquier aplicación.
Con `Ctrl-real` en un terminal: Ctrl+A al inicio de línea, Ctrl+C interrumpe.
Si en macOS `U_APP`+C no copia pero `Ctrl-real`+C sí, es que no quitaste el
swap del sistema.

**Detección.** Conmuta el ATEN a cada máquina y pulsa `OS:info` en un campo de
texto. Debe escribir el sistema correcto. Si sale "sin determinar" o el que no
es, fuerza con `OS:mac` / `OS:win` / `OS:lin` y dímelo: hay parámetros que
ajustar (`OS_DETECTION_DEBOUNCE`, ahora en 250 ms).

**Navegación.** Pestaña siguiente y anterior en Brave. Cambio de escritorio.
Conmutador de aplicaciones con toques repetidos sin soltar la capa. Mover una
ventana del LG DualUp al otro monitor.

**Herdr.** Con Herdr abierto: `H:left` a `H:right` mueven el foco de panel,
`H:new` abre pestaña, `H:splv` divide. Si un chord no hace nada, lo consumió el
terminal o el escritorio antes de llegar a Herdr.

---

## 10. Decisiones que quizá quieras cambiar

**`Ctrl-real` está arriba a la derecha, que es un estiramiento del meñique.**
Lo puse ahí porque es una tecla de uso deliberado, no continuo: la capa Herdr
cubre el Ctrl de alta frecuencia. Si te resulta incómoda, la alternativa es
convertir Enter en mod-tap. En `keymap.c`, capa `L_BASE`, cambia `KC_ENTER` por
`RCTL_T(KC_ENTER)` y devuelve `KC_DELETE` a la posición de arriba a la derecha.
No lo hice por defecto porque estás aprendiendo mecanografía y los mod-tap
producen fallos difíciles de diagnosticar mientras la pulsación aún no es
regular.

**No puse home-row mods**, por lo mismo. Tus errores en keybr estaban en las
teclas de índice (b, y, f, j); añadir modificadores a la fila de inicio ahora
empeoraría eso. El cluster de modificadores de la capa NAV cubre el caso sin
tocar la capa base.

**Un roce del pulgar fija la capa.** Es la contrapartida de
`TAPPING_TOGGLE 1`. El color de los LEDs cambia con la capa, así que lo ves,
pero si te pasa a menudo cambia el 1 por un 2 en `config.h`: entonces hace
falta doble toque para fijar y un roce suelto no hace nada.

**No hay teclado numérico.** La mano derecha de SYM podría ser uno, con los
operadores ya colocados al lado. Lo dejé fuera porque implica reaprender la capa
que acabas de memorizar. Si quieres, es un cambio de diez minutos.

**El override manual de OS no se guarda en EEPROM.** El firmware de ZSA usa su
propio bloque de configuración de usuario y no quise arriesgar un conflicto. El
override vive en RAM y se pierde al conmutar de máquina, que es justo cuando la
detección automática vuelve a ejecutarse. Si la detección resulta poco fiable
detrás del ATEN, esto habrá que replantearlo.

**`ctrl+alt+l` está asignado al foco de panel derecho de Herdr.** La
documentación de Herdr lo marca como bloqueo de pantalla en KDE. En GNOME,
Windows y macOS está libre, así que en tu caso no molesta. Queda anotado en el
TOML por si algún día usas KDE.
