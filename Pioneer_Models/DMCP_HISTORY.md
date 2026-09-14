# DMCP System Firmware History

> Please remember it is always wise to make FAT disk backup before any update.

## DMCP v3.31 — 2026-05-06

- Fixed disk write buffer overrun (based on several crash reports)
- Stability improvements of Flash/QSPI writes

## DMCP v3.30 — 2025-12-02

- Updated System menu confirmation message

## DMCP v3.29 — 2025-11-13

- Extended search for keymap filename to pattern 'keymap_\*.bin'
- RESET+F4 activates bootloader (USB DFU)

## DMCP v3.28 — 2025-10-20

- Added QR code functions to interface
- KBD test update (Fixed order of keys for DM41X)

## DMCP v3.27 — 2025-09-19

- Fixed: character spacing glitch when switching to SwissKeys ("bold") font
- Fixed: Allow to load QSPI file from FAT with CRC specified by currently loaded program

## DMCP v3.26 — 2025-04-25

- corrected diagnostic exit key sequence
- Added several new font characters for libfree42 compatibility

## DMCP v3.25 — 2024-06-27

- Help browser allows to jump to \<p> tags
- run_help_file() with empty filename opens help-file selection dialog
- Improved key-press handling while previous key isn't released yet
- Louder screenshot sound

## DMCP v3.24 — 2022-09-22

- SM logo (after RESET) update
- Fixes in help browser

## DMCP v3.23 — 2022-01-28

- Maintenance release - no functional changes

## DMCP v3.22 — 2021-08-20

- Font updates and fixes

## DMCP v3.21 — 2021-03-23

- Maintenance release - no functional changes
- Stabilization fixes to prevent issues arising from DM42 3.18

## DMCP v3.20 — 2020-10-09

- Help system: Support for links between files
- Help system: Numpad like navigation keys
- DMCP ifc doc updated to version 3.15

## DMCP v3.19 — 2020-05-12

- Fixed problem with bad key state after wake-up
- USB disk reports unique disk ID now

## DMCP v3.18 — 2020-03-30

- Fixed labels for date format change in 'Set Date' screen to match 'Set Time' time format change.
- Fixed file filtering problem in file list screens.

## DMCP v3.17 — 2020-02-11

- Maintenance revision, no functional changes

## DMCP v3.16 — 2020-01-17

- File list: Fix sporadic repeat of first chars in some filenames
- File list: Fix displaying zeroes and eventual hang at some point while displaying directories with 100+ files.

## DMCP v3.15 — 2019-07-24

- Improve response to simultaneous key presses

## DMCP v3.14 — 2019-07-08

- LCD handling enhancement
- Stability enhancement
- Keyboard handling enhancement

## DMCP v3.13 — 2019-03-15

- File listing enhancements - supports more files in directory listings, directory browsing and two column display
- Clear history buffer when help file changed
- Fix of hangs on some boards in various places (before or after flashing from FAT, after USB plug-in)

## DMCP v3.12 — 2019-01-22

- Firmware update from FAT, doesn't wait for key press after successful flashing
- RESET+[+] jumps directly to MSC mode (checks for fw and keymap file and installs them without confirmation)
- Support for reset.bmp (loaded from /reset.bmp)
- Clarify DMY/MDY switching in date setting screen by removing [-1m] and adding [DMY]/[MDY].
- (Devel) System keymap support (loaded from /keymap.bin)
- (Testing) "System->Power OFF mode" menu item

## DMCP v3.11 — 2018-10-11

- Fix for "Bug when connecting to USB cable"

## DMCP v3.10 — 2018-10-01

- Upgrade system interface for bitmap handling to support print to file from DM42PGM

## DMCP v3.9a (minor) — 2018-08-10

- Menu lines aligned after line number

## DMCP v3.9 — 2018-08-01

- Small number of boards exhibited excessive power-off current - fixed

## DMCP v3.8 — 2018-07-03

- Fixed jump out of system menu to sleep
- Added program/system interface comparison to program info screen
- Extended DMCP interface to version 3.8 (added run_help_file() function)
