#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define PROGMEM
#define pgm_read_byte(p) (*(const uint8_t *)(p))
#define MATRIX_ROWS 1
#define MATRIX_COLS 52
#define RGB_MATRIX_LED_COUNT 52
#define LAYOUT_voyager(...) {{__VA_ARGS__}}
#define SEND_STRING(s) do { (void)(s); } while (0)
#define LED_LEVEL 0

typedef uint16_t layer_state_t;
typedef struct { bool pressed; } keyevent_t;
typedef struct { keyevent_t event; } keyrecord_t;
typedef struct { uint8_t h, s, v; } HSV;
typedef struct { uint8_t r, g, b; } RGB;
typedef struct { HSV hsv; } rgb_config_t;
typedef struct { bool rgb_control; } rawhid_state_t;
typedef struct { bool disable_layer_led; } keyboard_config_t;
extern rawhid_state_t rawhid_state;
extern keyboard_config_t keyboard_config;

/* keycodes: rango suficiente para que los casos del switch sean distintos */
enum {
  KC_NO = 0x0000, KC_TRANSPARENT = 0x0001,
  KC_A = 0x0004, KC_B, KC_C, KC_D, KC_E, KC_F, KC_G, KC_H, KC_I, KC_J, KC_K,
  KC_L, KC_M, KC_N, KC_O, KC_P, KC_Q, KC_R, KC_S, KC_T, KC_U, KC_V, KC_W,
  KC_X, KC_Y, KC_Z,
  KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0,
  KC_ENTER, KC_ESCAPE, KC_BSPC, KC_TAB, KC_SPACE,
  KC_MINS, KC_EQL, KC_LBRC, KC_RBRC, KC_BSLS, KC_NUHS, KC_SCLN, KC_QUOT,
  KC_GRV, KC_COMM, KC_COMMA = KC_COMM, KC_DOT, KC_SLSH, KC_CAPS,
  KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, KC_F12,
  KC_PSCR, KC_HOME, KC_PAGE_UP, KC_DELETE, KC_END, KC_PGDN, KC_PGUP = KC_PAGE_UP,
  KC_RIGHT, KC_LEFT, KC_DOWN, KC_UP, KC_NUBS,
  KC_LEFT_CTRL, KC_LEFT_SHIFT, KC_LEFT_ALT, KC_LEFT_GUI,
  KC_RIGHT_CTRL, KC_RIGHT_SHIFT, KC_RIGHT_ALT, KC_RIGHT_GUI,
  KC_LCTL = KC_LEFT_CTRL, KC_LSFT = KC_LEFT_SHIFT, KC_LALT = KC_LEFT_ALT,
  KC_LGUI = KC_LEFT_GUI, KC_RCTL = KC_RIGHT_CTRL,
  KC_AUDIO_VOL_DOWN, KC_AUDIO_VOL_UP, KC_AUDIO_MUTE,
  KC_MEDIA_PLAY_PAUSE, KC_MEDIA_PREV_TRACK, KC_MEDIA_NEXT_TRACK,
  RM_TOGG = 0x7800, RM_NEXT, RM_HUEU, RM_HUED, RM_VALU, RM_VALD,
  QK_BOOT = 0x7C00, EE_CLR, TOGGLE_LAYER_COLOR,
  SAFE_RANGE = 0x7E00
};

#define QK_MODS       0x0100
#define QK_MODS_MAX   0x1FFF
#define MOD_LCTL 0x01
#define MOD_LSFT 0x02
#define MOD_LALT 0x04
#define MOD_LGUI 0x08
#define MOD_BIT(kc) (1u << ((kc) & 3))
#define QK_MODS_GET_BASIC_KEYCODE(kc) ((kc) & 0xFF)
#define QK_MODS_GET_MODS(kc) (((kc) >> 8) & 0x1F)
#define IS_CONSUMER_KEYCODE(kc) ((kc) >= KC_AUDIO_VOL_DOWN && (kc) <= KC_MEDIA_NEXT_TRACK)

#define LCTL(kc) (0x0100 | (kc))
#define LSFT(kc) (0x0200 | (kc))
#define LALT(kc) (0x0400 | (kc))
#define LGUI(kc) (0x0800 | (kc))
#define S(kc)    LSFT(kc)
#define ALGR(kc) (0x1400 | (kc))
#define MO(n)    (0x5220 | (n))

typedef enum { OS_UNSURE, OS_LINUX, OS_WINDOWS, OS_MACOS, OS_IOS } os_variant_t;
os_variant_t detected_host_os(void);

void     register_mods(uint8_t m);
void     unregister_mods(uint8_t m);
void     add_mods(uint8_t m);
void     del_mods(uint8_t m);
void     send_keyboard_report(void);
void     wait_ms(uint16_t ms);
void     register_code(uint8_t kc);
void     register_code16(uint16_t kc);
void     unregister_code16(uint16_t kc);
void     tap_code(uint8_t kc);
uint16_t timer_read(void);
uint16_t timer_elapsed(uint16_t t);
void     rgblight_mode(uint8_t m);
void     rgb_matrix_enable(void);
void     rgb_matrix_set_color(int i, uint8_t r, uint8_t g, uint8_t b);
void     rgb_matrix_set_color_all(uint8_t r, uint8_t g, uint8_t b);
uint8_t  rgb_matrix_get_flags(void);
#define LED_FLAG_NONE 0
RGB      hsv_to_rgb(HSV hsv);
uint8_t  biton32(uint32_t v);
extern uint32_t layer_state;
layer_state_t update_tri_layer_state(layer_state_t s, uint8_t a, uint8_t b, uint8_t c);
