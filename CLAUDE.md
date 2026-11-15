# PX30-wallpanel

Vervangt Android op de Smatek ST-PX30-T6E door Debian 13 arm64: kiosk (Cog/WPE
op DRM) met een Home Assistant-dashboard, een agent (MQTT, updates, rescue) en
het on-device flashen van de Zigbee/Thread-radio (TYZS13).

## Mappen
- `agent/` — px30-agent (MQTT discovery), px30-update, sudoers/udev-regels
- `boot/` — scripts voor recovery-image en dtb-varianten
- `bootanim/` — bootanimatie
- `dts/` — device tree + build-dtb.sh
- `initramfs/` — eigen initramfs (A/B, fallback, rescue)
- `kernel/` — patches bovenop mainline
- `kiosk/` — kiosk-extra's (dashboard-backup, kaarten, proximity-wake)
- `rootfs/` — build-rootfs.sh + overlay
- `tools/` — debug- en OTA-hulpmiddelen voor op de PC
- `zigbee/` — recepten voor radiofirmware (NCP, OT-RCP, router, OTBR)
- `tests/` — `python tests/test_update.py` enz. (de pipeline-test gebruikt `../fwpipe` of `FWPIPE_DIR`)
- `docs/` — Engelse documentatie; `docs/archive/` lokaal Nederlands logboek (gitignored)
- `logs/` — seriële/debug-logs en schermafbeeldingen van eerdere sessies

## Harde regels
- Nooit schrijven onder offset 0x4000 van de eMMC, en nooit naar uboot,
  trust of idblock.
- Het account `admin` op het paneel is alleen-lezen, tenzij Ward het bevestigt.
- De seriële poort niet op het LAN zetten zonder Ward's OK.
- Geen wifi-secrets tonen, loggen of committen.
- Het paneel is een live systeem: eerst vragen.
- Geen `Co-Authored-By`-trailer in commits.

## Waar staat wat
- Status en wat werkt: README.md en `docs/`. Houd dit bestand kort.
- Radiofirmware-builds (de vroegere `updater/`) staan in de private repo
  `Warre118/fwpipe`; clone die naast deze repo (`../fwpipe`).
