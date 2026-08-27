// Códigos del layout español (ISO).
// Basado en quantum/keymap_extras/keymap_spanish.h de QMK.
//
// IMPORTANTE: estos defines describen el layout ESPAÑOL DE PC (Windows/Linux).
// Los símbolos que difieren en macOS NO se definen aquí: se resuelven en
// tiempo de ejecución en keymap.c (ver U_BSLS y os_chord()).
#pragma once

// Letras y dígitos (idénticos al US)
#define ES_MORD KC_GRV        // º
#define ES_FORD S(KC_GRV)     // ª
#define ES_NTIL KC_SCLN       // ñ
#define ES_CCED KC_NUHS       // ç
#define ES_ACUT KC_QUOT       // ´ (muerta)
#define ES_DIAE S(KC_QUOT)    // ¨ (muerta)
#define ES_GRV  KC_LBRC       // ` (muerta)
#define ES_CIRC S(KC_LBRC)    // ^ (muerta)
#define ES_PLUS KC_RBRC       // +
#define ES_ASTR S(KC_RBRC)    // *
#define ES_QUOT KC_MINS       // '
#define ES_QUES S(KC_MINS)    // ?
#define ES_IEXL KC_EQL        // ¡
#define ES_IQUE S(KC_EQL)     // ¿
#define ES_LABK KC_NUBS       // <
#define ES_RABK S(KC_NUBS)    // >
#define ES_MINS KC_SLSH       // -
#define ES_UNDS S(KC_SLSH)    // _
#define ES_SCLN S(KC_COMM)    // ;
#define ES_COLN S(KC_DOT)     // :

// Fila numérica con Shift
#define ES_EXLM S(KC_1)       // !
#define ES_DQUO S(KC_2)       // "
#define ES_BULT S(KC_3)       // ·
#define ES_DLR  S(KC_4)       // $
#define ES_PERC S(KC_5)       // %
#define ES_AMPR S(KC_6)       // &
#define ES_SLSH S(KC_7)       // /
#define ES_LPRN S(KC_8)       // (
#define ES_RPRN S(KC_9)       // )
#define ES_EQL  S(KC_0)       // =

// AltGr
#define ES_PIPE ALGR(KC_1)    // |
#define ES_AT   ALGR(KC_2)    // @
#define ES_HASH ALGR(KC_3)    // #
#define ES_TILD ALGR(KC_4)    // ~
#define ES_EURO ALGR(KC_5)    // €
#define ES_NOT  ALGR(KC_6)    // ¬   <-- ojo: esto es lo que escribía tu antigua tecla de "\"
#define ES_LBRC ALGR(KC_LBRC) // [
#define ES_RBRC ALGR(KC_RBRC) // ]
#define ES_LCBR ALGR(KC_QUOT) // {
#define ES_RCBR ALGR(KC_NUHS) // }

// Backslash: difiere entre PC y macOS.
//   PC (Win/Linux): AltGr + º
//   macOS:          AltGr(Option) + 6
// No usar directamente en el keymap: usar el keycode U_BSLS, que elige según el host.
#define ES_BSLS_PC  ALGR(KC_GRV)
#define ES_BSLS_MAC ALGR(KC_6)
