#define USB_SUSPEND_WAKEUP_DELAY 0
#define SERIAL_NUMBER "mXGVj/6aMO7E"
#define LAYER_STATE_8BIT

#define RGB_MATRIX_STARTUP_SPD 60

// TT() con el umbral en 1: mantener la tecla da capa momentánea, y un toque
// suelto la fija hasta que la vuelvas a tocar. Por defecto QMK usa cinco
// toques para fijar, que en la práctica nunca se alcanzan.
//
// Efecto secundario útil: como NAV y SYM se pueden dejar fijadas, tocar una y
// luego la otra deja los dos bits de capa activos, y el tri-layer enciende
// META. No hace falta mantener los dos pulgares.
//
// Riesgo: un roce involuntario del pulgar fija la capa y las letras dejan de
// escribir. El color de los LEDs avisa. Si molesta, pon 2 aquí: entonces hace
// falta doble toque para fijar y un roce suelto no hace nada.
#define TAPPING_TOGGLE 1

// --- Detección del host ---
// La detección se estabiliza antes de aplicarse. 250 ms da margen a la
// reenumeración USB del KVM sin que se note al conmutar.
#define OS_DETECTION_DEBOUNCE 250

// Reinicia el teclado cuando el USB vuelve al estado inicial, es decir al
// conmutar el ATEN, para que la detección se repita en el host nuevo. QMK solo
// actúa si la detección ya fue estable al menos una vez, precisamente para no
// entrar en bucle con algunos KVM.
#define OS_DETECTION_KEYBOARD_RESET

// Propaga el host detectado a la mitad derecha. Sin esto, los LEDs de la mitad
// derecha no reflejarían el color del sistema activo.
#define SPLIT_DETECTED_OS_ENABLE
