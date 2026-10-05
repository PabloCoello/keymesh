# Bucle de trabajo del layout del Voyager.
#
#   make check    verifica keymap.c sin tocar nada mas
#   make          check + regenera ledmap.h y chuleta.html
#   make chuleta  lo anterior y abre la chuleta en el navegador
#   make compile  lo anterior + compila el firmware
#   make flash    lo anterior + flashea el teclado
#
# Si tu copia de qmk_firmware esta en otro sitio:
#   make flash QMK=/ruta/qmk_firmware

QMK      ?= $(HOME)/qmk_firmware
KB       ?= zsa/voyager
KM       ?= keymesh
PY       ?= python3
CC       ?= cc
DEST      = $(QMK)/keyboards/$(KB)/keymaps/$(KM)
SOURCES   = keymap.c config.h rules.mk i18n.h ledmap.h

# Se usa el prebuilt oficial de Arm con la version fija, para que el binario no
# dependa de lo que haya en el disco de cada maquina. Ademas trae newlib, que es
# justo lo que le falta al arm-none-eabi-gcc de Homebrew: sin ella no encuentra
# stdint.h y la compilacion muere en el primer fichero de ChibiOS. Si esta donde
# lo deja la instalacion descrita en el README, se antepone al PATH; si no, se
# usa lo que haya. El nombre del directorio lleva el host, asi que se compone.
ARM_VERSION ?= 13.3.rel1
UNAME_S     := $(shell uname -s)
UNAME_M     := $(shell uname -m)
ifeq ($(UNAME_S),Darwin)
ARM_HOST ?= darwin-$(UNAME_M)
else
ARM_HOST ?= $(UNAME_M)
endif
ARM_TOOLCHAIN ?= $(HOME)/toolchains/arm-gnu-toolchain-$(ARM_VERSION)-$(ARM_HOST)-arm-none-eabi/bin
ifneq ($(wildcard $(ARM_TOOLCHAIN)),)
export PATH := $(ARM_TOOLCHAIN):$(PATH)
endif

.PHONY: all check syntax gen chuleta install compile flash clean

all: gen

# ledmap.h se regenera primero porque check.py y la chuleta lo leen.
check:
	@$(PY) tools/gen_ledmap.py > /dev/null
	@$(PY) tools/check.py
	@$(MAKE) --no-print-directory syntax

# Compila keymap.c contra stubs de la API de QMK. Caza erratas y keycodes
# inexistentes en segundos, sin necesitar el toolchain de ARM.
syntax:
	@rm -rf .synt && mkdir -p .synt
	@cp ledmap.h i18n.h tools/stub/qmk_stub.h .synt/
	@printf '#pragma once\n#include "qmk_stub.h"\n' > .synt/version.h
	@printf '#pragma once\n#include "qmk_stub.h"\n' > .synt/os_detection.h
	@sed 's|#include QMK_KEYBOARD_H|#include "qmk_stub.h"|' keymap.c > .synt/keymap.c
	@$(CC) -fsyntax-only -Wall -Wextra -Wno-unused-parameter -I.synt .synt/keymap.c
	@rm -rf .synt
	@echo "syntax: keymap.c compila sin avisos"

gen: check
	@$(PY) tools/gen_ledmap.py
	@$(PY) tools/gen_cheatsheet.py

chuleta: gen
	@command -v open >/dev/null 2>&1 && open chuleta.html && exit 0; \
	 command -v xdg-open >/dev/null 2>&1 && xdg-open chuleta.html && exit 0; \
	 echo "abre chuleta.html a mano"

install: gen
	@test -d "$(QMK)" || { echo "No encuentro qmk_firmware en $(QMK)."; \
	  echo "Usa: make $(MAKECMDGOALS) QMK=/ruta/a/qmk_firmware"; exit 1; }
	@mkdir -p $(DEST)
	@cp $(SOURCES) $(DEST)/
	@echo "install: copiado a $(DEST)"

compile: install
	@cd $(QMK) && qmk compile -kb $(KB) -km $(KM)

flash: install
	@echo "Cuando lo pida, pulsa el boton de reset del borde superior."
	@cd $(QMK) && qmk flash -kb $(KB) -km $(KM)

clean:
	@rm -rf .synt
