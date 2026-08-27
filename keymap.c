#include QMK_KEYBOARD_H
#include "version.h"
#include "i18n.h"
#include "os_detection.h"

#define MOON_LED_LEVEL LED_LEVEL
#ifndef ZSA_SAFE_RANGE
#define ZSA_SAFE_RANGE SAFE_RANGE
#endif

// ---------------------------------------------------------------------------
// Capas
// ---------------------------------------------------------------------------
enum layers {
    L_BASE = 0,
    L_NAV  = 1,
    L_SYM  = 2,
    L_META = 3,  // se activa manteniendo los dos pulgares interiores (tri-layer)
};

enum custom_keycodes {
    RGB_SLD = ZSA_SAFE_RANGE,

    // Modificador "de aplicación": Cmd en macOS, Ctrl en Windows/Linux.
    U_APP,

    // Edición
    U_UNDO, U_REDO, U_CUT, U_COPY, U_PASTE,

    // Movimiento de texto
    U_WLFT, U_WRGT,    // palabra izquierda / derecha
    U_LNST, U_LNEND,   // inicio / fin de línea
    U_DWBK,            // borrar palabra hacia atrás

    // Ventanas, escritorios, aplicaciones
    U_APPSW,           // conmutador de aplicaciones con modificador sostenido
    U_WINN,            // siguiente ventana de la misma aplicación
    U_DESKL, U_DESKR,  // escritorio / Space anterior y siguiente
    U_DISPL, U_DISPR,  // mover la ventana a la pantalla anterior / siguiente
    U_MSN,             // Mission Control / Task View / Activities

    // Varios dependientes del host
    U_ZIN, U_ZOUT,     // zoom
    U_SHOT,            // captura de región
    U_BSLS,            // backslash

    // Control manual del host detectado
    U_OSAUTO, U_OSMAC, U_OSWIN, U_OSLIN, U_OSDBG,

    // Herdr (chords ctrl+alt, idénticos en los tres sistemas)
    HRD_PFX,                                   // prefijo ctrl+b
    HRD_LEFT, HRD_DOWN, HRD_UP, HRD_RIGHT,     // foco de panel
    HRD_ZOOM, HRD_SPLV, HRD_SPLH, HRD_CLOSE,   // paneles
    HRD_NEW, HRD_TABP, HRD_TABN,               // pestañas
    HRD_WS, HRD_GOTO, HRD_DETACH,              // sesión
};

// ---------------------------------------------------------------------------
// Resolución del host
// ---------------------------------------------------------------------------
typedef enum { OSX_AUTO, OSX_MAC, OSX_WIN, OSX_LIN } os_override_t;

// Solo en RAM, a propósito: no toco el bloque EEPROM de usuario porque el
// firmware de ZSA guarda su propia configuración ahí. Al cambiar de host el
// teclado se reinicia (OS_DETECTION_KEYBOARD_RESET) y vuelve a AUTO.
static os_override_t os_override = OSX_AUTO;

static os_variant_t host_os(void) {
    switch (os_override) {
        case OSX_MAC: return OS_MACOS;
        case OSX_WIN: return OS_WINDOWS;
        case OSX_LIN: return OS_LINUX;
        default:      return detected_host_os();
    }
}

static bool host_is_mac(void) {
    os_variant_t os = host_os();
    return os == OS_MACOS || os == OS_IOS;
}

static bool host_is_win(void) {
    return host_os() == OS_WINDOWS;
}

// Devuelve el chord real para un keycode semántico, o KC_NO si no aplica.
static uint16_t os_chord(uint16_t keycode) {
    const bool mac = host_is_mac();
    const bool win = host_is_win();

    switch (keycode) {
        // --- Edición ---
        case U_UNDO:  return mac ? LGUI(KC_Z)        : LCTL(KC_Z);
        case U_REDO:  return mac ? LGUI(LSFT(KC_Z))  : LCTL(LSFT(KC_Z));
        case U_CUT:   return mac ? LGUI(KC_X)        : LCTL(KC_X);
        case U_COPY:  return mac ? LGUI(KC_C)        : LCTL(KC_C);
        case U_PASTE: return mac ? LGUI(KC_V)        : LCTL(KC_V);

        // --- Movimiento de texto ---
        // En macOS el salto de palabra es Option, en PC es Ctrl.
        case U_WLFT:  return mac ? LALT(KC_LEFT)     : LCTL(KC_LEFT);
        case U_WRGT:  return mac ? LALT(KC_RIGHT)    : LCTL(KC_RIGHT);
        // En macOS, Home/End van al inicio/fin del documento, no de la línea.
        case U_LNST:  return mac ? LGUI(KC_LEFT)     : KC_HOME;
        case U_LNEND: return mac ? LGUI(KC_RIGHT)    : KC_END;
        case U_DWBK:  return mac ? LALT(KC_BSPC)     : LCTL(KC_BSPC);

        // --- Ventanas y escritorios ---
        case U_WINN:
            if (mac) return LGUI(ES_MORD);      // Cmd+` (tecla a la izquierda del 1)
            if (win) return LALT(KC_TAB);       // Windows no tiene equivalente por app
            return LALT(ES_MORD);               // GNOME: "cambiar ventanas de una aplicación"
        case U_DESKL:
            if (mac) return LCTL(KC_LEFT);
            if (win) return LGUI(LCTL(KC_LEFT));
            return LGUI(KC_PGUP);               // GNOME: Super+Page_Up
        case U_DESKR:
            if (mac) return LCTL(KC_RIGHT);
            if (win) return LGUI(LCTL(KC_RIGHT));
            return LGUI(KC_PGDN);               // GNOME: Super+Page_Down
        case U_DISPL:
            // macOS no tiene atajo nativo para esto: son los valores por
            // defecto de Rectangle ("Move to previous/next display").
            if (mac) return LCTL(LALT(LGUI(KC_LEFT)));
            if (win) return LGUI(LSFT(KC_LEFT));
            return LGUI(LSFT(KC_LEFT));         // GNOME: Shift+Super+izquierda
        case U_DISPR:
            if (mac) return LCTL(LALT(LGUI(KC_RIGHT)));
            if (win) return LGUI(LSFT(KC_RIGHT));
            return LGUI(LSFT(KC_RIGHT));        // GNOME: Shift+Super+derecha
        case U_MSN:
            if (mac) return LCTL(KC_UP);        // Mission Control
            if (win) return LGUI(KC_TAB);       // Task View
            return KC_LGUI;                     // GNOME: Actividades

        // --- Varios ---
        case U_ZIN:   return mac ? LGUI(ES_PLUS)     : LCTL(ES_PLUS);
        case U_ZOUT:  return mac ? LGUI(ES_MINS)     : LCTL(ES_MINS);
        case U_SHOT:
            if (mac) return LGUI(LSFT(KC_4));
            if (win) return LGUI(LSFT(KC_S));
            return LSFT(KC_PSCR);
        case U_BSLS:  return mac ? ES_BSLS_MAC       : ES_BSLS_PC;

        // --- Herdr: ctrl+alt, idéntico en los tres sistemas ---
        case HRD_PFX:    return LCTL(KC_B);
        case HRD_LEFT:   return LCTL(LALT(KC_H));
        case HRD_DOWN:   return LCTL(LALT(KC_J));
        case HRD_UP:     return LCTL(LALT(KC_K));
        case HRD_RIGHT:  return LCTL(LALT(KC_L));
        case HRD_ZOOM:   return LCTL(LALT(KC_Z));
        case HRD_SPLV:   return LCTL(LALT(KC_D));
        case HRD_SPLH:   return LCTL(LALT(LSFT(KC_D)));
        case HRD_CLOSE:  return LCTL(LALT(KC_X));
        case HRD_NEW:    return LCTL(LALT(KC_C));
        case HRD_TABP:   return LCTL(LALT(KC_P));
        case HRD_TABN:   return LCTL(LALT(KC_N));
        case HRD_WS:     return LCTL(LALT(KC_W));
        case HRD_GOTO:   return LCTL(LALT(KC_G));
        case HRD_DETACH: return LCTL(LALT(KC_Q));
    }
    return KC_NO;
}

// ---------------------------------------------------------------------------
// Keymap
// ---------------------------------------------------------------------------
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

  // BASE. Cambios respecto a tu layout: la tecla de Bloq Mayús pasa de
  // KC_LEFT_CTRL a U_APP (Cmd en mac, Ctrl en PC) y KC_DELETE (arriba a la
  // derecha) pasa a KC_RIGHT_CTRL, que es Ctrl de verdad en los tres sistemas.
  // Delete sigue disponible en la capa NAV.
  [L_BASE] = LAYOUT_voyager(
    KC_ESCAPE,      KC_1,           KC_2,           KC_3,           KC_4,           KC_5,                                           KC_6,           KC_7,           KC_8,           KC_9,           KC_0,           KC_RIGHT_CTRL,
    KC_TAB,         KC_Q,           KC_W,           KC_E,           KC_R,           KC_T,                                           KC_Y,           KC_U,           KC_I,           KC_O,           KC_P,           KC_ENTER,
    U_APP,          KC_A,           KC_S,           KC_D,           KC_F,           KC_G,                                           KC_H,           KC_J,           KC_K,           KC_L,           ES_NTIL,        ES_ACUT,
    KC_LEFT_SHIFT,  KC_Z,           KC_X,           KC_C,           KC_V,           KC_B,                                           KC_N,           KC_M,           KC_COMMA,       KC_DOT,         ES_MINS,        KC_RIGHT_SHIFT,
                                                    KC_BSPC,        TT(L_NAV),                                      TT(L_SYM),      KC_SPACE
  ),

  // NAV. Mano izquierda: acciones sobre el documento y la aplicación.
  // Mano derecha: movimiento. Filas 2-3 dentro del texto, fila 4 entre
  // contenedores (aplicaciones, ventanas, escritorios).
  [L_NAV] = LAYOUT_voyager(
    KC_ESCAPE,      KC_F1,          KC_F2,          KC_F3,          KC_F4,          KC_F5,                                          KC_F6,          KC_F7,          KC_F8,          KC_F9,          KC_F10,         KC_F11,
    KC_TAB,         LCTL(LSFT(KC_TAB)),LCTL(KC_TAB),U_ZOUT,         U_ZIN,          U_SHOT,                                         U_LNST,         KC_PAGE_UP,     KC_UP,          KC_PGDN,        U_LNEND,        KC_ENTER,
    KC_TRANSPARENT, KC_LEFT_GUI,    KC_LEFT_ALT,    KC_LEFT_CTRL,   KC_LEFT_SHIFT,  KC_RIGHT_ALT,                                   U_WLFT,         KC_LEFT,        KC_DOWN,        KC_RIGHT,       U_WRGT,         KC_DELETE,
    KC_TRANSPARENT, U_UNDO,         U_CUT,          U_COPY,         U_PASTE,        U_REDO,                                         U_APPSW,        U_WINN,         U_DESKL,        U_DESKR,        U_MSN,          KC_TRANSPARENT,
                                                    U_DWBK,         KC_TRANSPARENT,                                 KC_TRANSPARENT, KC_SPACE
  ),

  // SYM. Mano izquierda intacta respecto a tu layout salvo el backslash.
  // Mano derecha: se eliminaron el ! y el ? duplicados y se rellenó la fila 4.
  [L_SYM] = LAYOUT_voyager(
    KC_TRANSPARENT, ES_IEXL,        ES_IQUE,        ES_QUOT,        ES_QUES,        ES_GRV,                                         ES_EURO,        ES_DQUO,        ES_PERC,        ES_DLR,         ES_UNDS,        KC_TRANSPARENT,
    KC_TRANSPARENT, ES_PIPE,        ES_AT,          ES_HASH,        ES_TILD,        ES_AMPR,                                        ES_PLUS,        ES_MINS,        ES_SLSH,        ES_ASTR,        ES_MORD,        KC_ENTER,
    KC_TRANSPARENT, ES_LCBR,        ES_LBRC,        ES_LPRN,        ES_LABK,        ES_EQL,                                         KC_AUDIO_VOL_DOWN,KC_AUDIO_VOL_UP,KC_AUDIO_MUTE, KC_MEDIA_PLAY_PAUSE,KC_MEDIA_PREV_TRACK,KC_MEDIA_NEXT_TRACK,
    KC_TRANSPARENT, ES_RCBR,        ES_RBRC,        ES_RPRN,        ES_RABK,        U_BSLS,                                         ES_CIRC,        ES_DIAE,        ES_SCLN,        ES_COLN,        ES_CCED,        KC_TRANSPARENT,
                                                    KC_BSPC,        KC_TRANSPARENT,                                 KC_TRANSPARENT, KC_SPACE
  ),

  // META. Mantén los dos pulgares interiores a la vez.
  // Izquierda: sistema, host, LEDs. Derecha: Herdr sobre h/j/k/l reales.
  [L_META] = LAYOUT_voyager(
    QK_BOOT,        KC_NO,          KC_NO,          KC_NO,          U_DISPL,        U_DISPR,                                        KC_NO,          KC_NO,          KC_NO,          KC_NO,          KC_NO,          KC_NO,
    KC_NO,          U_OSAUTO,       U_OSMAC,        U_OSWIN,        U_OSLIN,        U_OSDBG,                                        HRD_SPLH,       HRD_SPLV,       HRD_NEW,        HRD_TABP,       HRD_TABN,       KC_ENTER,
    KC_NO,          RM_TOGG,        RM_NEXT,        RM_HUEU,        RM_VALU,        TOGGLE_LAYER_COLOR,                             HRD_LEFT,       HRD_DOWN,       HRD_UP,         HRD_RIGHT,      HRD_ZOOM,       KC_NO,
    KC_NO,          EE_CLR,         RGB_SLD,        RM_HUED,        RM_VALD,        KC_NO,                                          HRD_PFX,        HRD_CLOSE,      HRD_DETACH,     HRD_WS,         HRD_GOTO,       KC_NO,
                                                    KC_NO,          KC_TRANSPARENT,                                 KC_TRANSPARENT, KC_NO
  ),
};

// META se alcanza manteniendo NAV y SYM a la vez. No gasta ninguna tecla.
layer_state_t layer_state_set_user(layer_state_t state) {
    return update_tri_layer_state(state, L_NAV, L_SYM, L_META);
}

// ---------------------------------------------------------------------------
// Conmutador de aplicaciones con modificador sostenido
// ---------------------------------------------------------------------------
// Cmd+Tab (mac) o Alt+Tab (PC) solo sirven si el modificador se mantiene entre
// pulsaciones. Aquí se mantiene durante APPSW_TIMEOUT ms tras el último toque,
// para poder recorrer la lista con toques repetidos.
#define APPSW_TIMEOUT 900

static bool     appsw_active = false;
static uint16_t appsw_timer  = 0;
static uint8_t  appsw_mod    = 0;

static void appsw_tap(void) {
    if (!appsw_active) {
        appsw_mod = host_is_mac() ? MOD_BIT(KC_LGUI) : MOD_BIT(KC_LALT);
        register_mods(appsw_mod);
        appsw_active = true;
    }
    appsw_timer = timer_read();
    tap_code(KC_TAB);
}

static void appsw_task(void) {
    if (appsw_active && timer_elapsed(appsw_timer) > APPSW_TIMEOUT) {
        unregister_mods(appsw_mod);
        appsw_active = false;
    }
}

// ---------------------------------------------------------------------------
// process_record_user
// ---------------------------------------------------------------------------
static uint8_t u_app_mod = 0;

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
    case QK_MODS ... QK_MODS_MAX:
        // Las teclas de consumo (volumen, media) con modificadores se
        // comportan de forma distinta en cada sistema; esto asegura que el
        // modificador se aplique a la tecla pulsada.
        if (IS_CONSUMER_KEYCODE(QK_MODS_GET_BASIC_KEYCODE(keycode))) {
            if (record->event.pressed) {
                add_mods(QK_MODS_GET_MODS(keycode));
                send_keyboard_report();
                wait_ms(2);
                register_code(QK_MODS_GET_BASIC_KEYCODE(keycode));
                return false;
            } else {
                wait_ms(2);
                del_mods(QK_MODS_GET_MODS(keycode));
            }
        }
        break;

    case RGB_SLD:
        if (record->event.pressed) {
            rgblight_mode(1);
        }
        return false;

    // Modificador de aplicación. Se recuerda qué modificador se registró en la
    // pulsación para liberar el mismo al soltar, aunque el host cambie.
    case U_APP:
        if (record->event.pressed) {
            u_app_mod = host_is_mac() ? MOD_BIT(KC_LGUI) : MOD_BIT(KC_LCTL);
            register_mods(u_app_mod);
        } else {
            unregister_mods(u_app_mod);
            u_app_mod = 0;
        }
        return false;

    case U_APPSW:
        if (record->event.pressed) {
            appsw_tap();
        }
        return false;

    // Control manual del host, por si la detección falla detrás del KVM.
    case U_OSAUTO: if (record->event.pressed) os_override = OSX_AUTO; return false;
    case U_OSMAC:  if (record->event.pressed) os_override = OSX_MAC;  return false;
    case U_OSWIN:  if (record->event.pressed) os_override = OSX_WIN;  return false;
    case U_OSLIN:  if (record->event.pressed) os_override = OSX_LIN;  return false;

    case U_OSDBG:
        if (record->event.pressed) {
            switch (detected_host_os()) {
                case OS_MACOS:   SEND_STRING("detectado: macOS"); break;
                case OS_IOS:     SEND_STRING("detectado: iOS"); break;
                case OS_WINDOWS: SEND_STRING("detectado: Windows"); break;
                case OS_LINUX:   SEND_STRING("detectado: Linux"); break;
                default:         SEND_STRING("detectado: sin determinar"); break;
            }
            switch (os_override) {
                case OSX_MAC: SEND_STRING(" / forzado: macOS"); break;
                case OSX_WIN: SEND_STRING(" / forzado: Windows"); break;
                case OSX_LIN: SEND_STRING(" / forzado: Linux"); break;
                default:      SEND_STRING(" / forzado: no"); break;
            }
        }
        return false;

    default: {
        // Todos los keycodes semánticos pasan por aquí. Se usa
        // register/unregister en lugar de tap para que mantener la tecla
        // repita (flechas de palabra, cambio de escritorio, etc.).
        uint16_t chord = os_chord(keycode);
        if (chord != KC_NO) {
            if (record->event.pressed) {
                register_code16(chord);
            } else {
                unregister_code16(chord);
            }
            return false;
        }
        break;
    }
    }
    return true;
}

void matrix_scan_user(void) {
    appsw_task();
}

// ---------------------------------------------------------------------------
// LEDs
// ---------------------------------------------------------------------------
extern rgb_config_t rgb_matrix_config;

RGB hsv_to_rgb_with_value(HSV hsv) {
    RGB   rgb = hsv_to_rgb(hsv);
    float f   = (float)rgb_matrix_config.hsv.v / UINT8_MAX;
    return (RGB){f * rgb.r, f * rgb.g, f * rgb.b};
}

void keyboard_post_init_user(void) {
    rgb_matrix_enable();
}

// El color de la capa BASE indica el host detectado, para que sepas de un
// vistazo qué semántica de modificadores está activa tras conmutar el KVM.
//   macOS   -> cian      Windows -> azul
//   Linux   -> naranja   sin determinar -> rojo tenue
static uint8_t base_hue(void) {
    switch (host_os()) {
        case OS_MACOS:
        case OS_IOS:     return 128;
        case OS_WINDOWS: return 160;
        case OS_LINUX:   return 20;
        default:         return 0;
    }
}

#include "ledmap.h"

void set_layer_color(int layer) {
    for (int i = 0; i < RGB_MATRIX_LED_COUNT; i++) {
        HSV hsv;
        if (layer == L_BASE) {
            uint8_t l = pgm_read_byte(&ledmap[L_BASE][i][2]);
            if (!l) {
                rgb_matrix_set_color(i, 0, 0, 0);
                continue;
            }
            // Las dos teclas modificadoras cambian de significado según el
            // host, así que se marcan con un tono desplazado.
            uint8_t h = pgm_read_byte(&ledmap[L_BASE][i][0]);
            hsv = (HSV){.h = (uint8_t)(base_hue() + h), .s = pgm_read_byte(&ledmap[L_BASE][i][1]), .v = l};
        } else {
            hsv = (HSV){
                .h = pgm_read_byte(&ledmap[layer][i][0]),
                .s = pgm_read_byte(&ledmap[layer][i][1]),
                .v = pgm_read_byte(&ledmap[layer][i][2]),
            };
        }
        if (!hsv.h && !hsv.s && !hsv.v) {
            rgb_matrix_set_color(i, 0, 0, 0);
        } else {
            RGB rgb = hsv_to_rgb_with_value(hsv);
            rgb_matrix_set_color(i, rgb.r, rgb.g, rgb.b);
        }
    }
}

bool rgb_matrix_indicators_user(void) {
    if (rawhid_state.rgb_control) {
        return false;
    }
    if (!keyboard_config.disable_layer_led) {
        switch (biton32(layer_state)) {
            case L_BASE: set_layer_color(L_BASE); break;
            case L_NAV:  set_layer_color(L_NAV);  break;
            case L_SYM:  set_layer_color(L_SYM);  break;
            case L_META: set_layer_color(L_META); break;
            default:
                if (rgb_matrix_get_flags() == LED_FLAG_NONE) {
                    rgb_matrix_set_color_all(0, 0, 0);
                }
        }
    } else {
        if (rgb_matrix_get_flags() == LED_FLAG_NONE) {
            rgb_matrix_set_color_all(0, 0, 0);
        }
    }
    return true;
}
