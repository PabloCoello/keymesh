# Layout del ZSA Voyager de Pablo

Firmware QMK para un ZSA Voyager que se usa en tres sistemas a través de un
conmutador KVM ATEN. El firmware detecta el anfitrión y resuelve cada atajo en
tiempo de ejecución, para que la misma tecla haga lo mismo en Windows, Ubuntu y
macOS aunque el chord que envía sea distinto.

## Contexto de hardware y entorno

- Teclado: ZSA Voyager, 52 teclas, split. Layout de Oryx `mXGVj/6aMO7E`.
- Tres equipos conmutados con un ATEN: macOS, Ubuntu (GNOME) y Windows.
- Los tres anfitriones usan el layout de teclado **español ISO**.
- Monitores: un LG DualUp más un segundo monitor. Mover ventanas entre
  pantallas es un caso de uso real, no teórico.
- Multiplexor de terminal: Herdr (herdr.dev), versión 0.8.2 al escribir esto.
- Pablo está aprendiendo mecanografía. Sus errores se concentran en las teclas
  de índice (b, y, f, j). Esto condiciona decisiones de diseño: ver invariantes.

## Cómo se trabaja en este repo

    make check      verifica keymap.c sin tocar el teclado
    make            check + regenera ledmap.h y chuleta.html
    make chuleta    lo anterior y abre la chuleta en el navegador
    make compile    lo anterior + compila el firmware
    make flash      lo anterior + flashea

`make check` corre siempre antes de compilar. Comprueba cuatro cosas:

1. Cada capa tiene exactamente 52 teclas. Una coma perdida en el array la
   acepta el compilador de QMK y deja el teclado con las teclas corridas.
2. Ningún keycode propio queda declarado sin tratar ni usado sin declarar.
3. Toda tecla colocada en una capa tiene etiqueta en `tools/labels.py`.
4. `keymap.c` compila con `-Wall -Wextra` contra stubs de la API de QMK.

### Entorno de compilación

`make compile` y `make flash` necesitan dos cosas fuera de lo obvio, ambas ya
resueltas en esta máquina y documentadas en la sección 6 del README:

- **El CLI de QMK tiene que correr sobre Python 3.11.** Los scripts de build de
  `firmware24` usan `ast.Num`, eliminado en Python 3.12. El síntoma es
  `Platform not defined` precedido de un `AttributeError` sobre `ast`, que no
  apunta a la causa.
- **El `arm-none-eabi-gcc` de Homebrew no sirve**: es el compilador sin newlib,
  así que no encuentra `stdint.h`. Se usa el prebuilt oficial de Arm en
  `~/toolchains/`, y el `Makefile` lo antepone al PATH mediante
  `ARM_TOOLCHAIN`.

Los avisos de `qmk doctor` sobre `avr-gcc`, `avrdude`, `dfu-programmer` y
`dfu-util` no aplican: el Voyager es ARM.

## Ficheros generados: no editar a mano

- `ledmap.h` lo genera `tools/gen_ledmap.py` desde las capas de `keymap.c`.
- `chuleta.html` lo genera `tools/gen_cheatsheet.py` desde `keymap.c`,
  `ledmap.h` y `tools/labels.py`.

Ambos se versionan a propósito, para poder consultar la chuleta desde una
máquina sin Python. Si editas `keymap.c`, ejecuta `make` antes de commitear.

## Invariantes: no romper sin hablarlo

**El swap de Cmd y Ctrl de macOS tiene que estar desactivado en Ajustes del
Sistema.** El firmware asume que recibe keycodes honestos. macOS aplica ese
remapeo por dispositivo a nivel HID, así que afecta a todo lo que manda el
teclado, incluido el prefijo `ctrl+b` de Herdr y las cadenas `ctrl+alt`. Fue el
origen del bug que motivó esta reescritura.

**`os_chord()` en `keymap.c` es la única fuente de verdad de las diferencias
entre sistemas.** Si un atajo difiere entre anfitriones, se añade un keycode
propio y se resuelve ahí. No metas condicionales de sistema en otros sitios.

**`CHORDS` y `HERDR` en `tools/labels.py` duplican lo que dice `os_chord()`.**
Es duplicación consciente: la chuleta necesita el texto legible. `make check`
falla si aparece un keycode sin etiqueta, pero **no** puede detectar que el
texto de la etiqueta miente. Si cambias un chord en `os_chord()`, cambia
también su entrada en `labels.py`.

**Rama `firmware24` del fork de ZSA.** `os_detection` está ahí. En esa rama los
keycodes `RGB_TOG`, `RGB_MOD`, `RGB_HUI`, `RGB_VAI`, `RGB_HUD` y `RGB_VAD` **ya
no existen**: QMK los renombró a `RM_TOGG`, `RM_NEXT`, `RM_HUEU`, `RM_VALU`,
`RM_HUED` y `RM_VALD`, sin alias. Si copias fragmentos de layouts antiguos, ese
es el primer error de compilación que verás.

**`i18n.h` describe solo el layout español de PC.** Los símbolos que difieren en
macOS no van ahí: se resuelven en `os_chord()`. Ahora mismo el único conocido es
el backslash (`U_BSLS`). Si aparecen más, siguen el mismo patrón.

**No usar el bloque EEPROM de usuario.** El firmware de ZSA guarda su propia
configuración ahí y no se ha verificado que no colisione. El override manual de
sistema vive en RAM y se pierde al conmutar de máquina, que es justo cuando la
detección automática vuelve a ejecutarse.

**Nada de home-row mods, y mod-taps solo con motivo.** Pablo está aprendiendo
mecanografía y sus fallos están en las teclas de índice. Añadir modificadores a
la fila de inicio empeoraría eso, y los mod-taps producen fallos difíciles de
diagnosticar mientras la pulsación aún no es regular. El cluster de
modificadores de la capa NAV cubre el caso sin tocar la base.

**Oryx es unidireccional.** Exporta código fuente, no lo importa, y no tiene
casilla para escribir un keycode arbitrario. `keymap.c` es la fuente de verdad;
el layout de Oryx queda congelado como copia de seguridad. Consecuencia
práctica: Keymapp y typ.ing muestran el layout viejo, porque lo descargan de
Oryx usando el ID que va en el firmware. Para eso está la chuleta.

## Estilo

Español neutro o de España. Nada de español rioplatense: sin voseo ni modismos
argentinos.

Comentarios en el código en español, y solo donde expliquen un *por qué* que no
se deduzca del código. Los chords de `os_chord()` llevan comentario cuando el
atajo no es obvio (por ejemplo que en GNOME el cambio de espacio de trabajo es
Super+PgUp y no Ctrl+Alt+flechas).
