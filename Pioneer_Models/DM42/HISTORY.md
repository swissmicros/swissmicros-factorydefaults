# DM42 Program Firmware History

> Please remember it is always wise to make FAT disk backup before any update.

Platform firmware: see [DMCP system firmware history](../DMCP_HISTORY.md)
([upstream](https://technical.swissmicros.com/dmcp/firmware/history.html)).

## DM42 v3.26 (built with DMCP 3.29) — 2025-11-14

- Upgrade Free42 core library to 3.3.10 version
- Fixed div, mul, percent and pi in DM alpha modes (forum https://www.hpmuseum.org/forum/thread-24155.html)
- Fixed: Crash when using CUSTOM Menu (forum https://forum.swissmicros.com/viewtopic.php?p=39015)

### DMCP changes

- Extended search for keymap filename to pattern 'keymap_\*.bin'
- RESET+F4 activates bootloader (USB DFU)

## DM42 v3.25 (built with DMCP 3.27) — 2025-09-22

- Upgrade Free42 core library to 3.3.8c version
- .. with additional free42 fix "88968670 Fixed initial 'locked' state when inserting END"
- .. Not-supported functions N→BS, N→BD, N→DS, N→DD, BS→N, DS→N (no more space for Intel FP library conversion functions)
- Fixed load of statefiles saved by "binary" versions of Free42
- Update help file URL in help-file-not-found dialog

### DMCP changes

- Fixed: character spacing glitch when switching to SwissKeys ("bold") font
- Fixed: Allow to load QSPI file from FAT with CRC specified by currently loaded program

## DM42 v3.24 (built with DMCP 3.26) — 2025-05-14

- Upgrade Free42 core library to 3.2.6 version

### DMCP changes

- Corrected "KBD Test" exit key sequence
- Added several new font characters for libfree42 compatibility

## DM42 v3.23 (built with DMCP 3.25) — 2024-07-25

- Upgrade lib free42 core to 3.1.8 version
- Fixed problem with covering program lines in MLPE during program line edit ([forum report](https://forum.swissmicros.com/viewtopic.php?p=22216#p22216))

## DM42 v3.22 (built with DMCP 3.24) — 2022-10-08

### Free42 changes

- Update Free42 core to version 3.0.15 (+next two commits)
- A...F added as programmable function (in BASE menu)
- Base mode automatically set to decimal upon entering PRGM mode
- Fix: Crash in SHOW ([report](https://forum.swissmicros.com/viewtopic.php?p=24037#p24037))

### DM42 changes

- WIDTH/HEIGHT returns current graphics mode resolution
- Fix: INTEG_ down ([report](https://forum.swissmicros.com/viewtopic.php?f=17&t=3199))
- Fix: Stacklayout XYZTA & NSTK & CLST ([report](https://forum.swissmicros.com/viewtopic.php?f=17&t=3322))
- Added much additional help file content created by Didier Lachieze, adding many function details, an alpha- index, notes on recent Free42 extensions and more.

### DMCP changes

- SM logo (after RESET) update
- Fixes in help browser code

## DM42 v3.21 (built with DMCP 3.23) — 2022-01-28

- Updated Free42 to version 3.0.9
- with additional patch: [e033a384](https://github.com/thomasokken/free42/commit/e033a384c96b62cce62ff8ac8b5e83ab1fa33d1d)

### DMCP changes

- None

## DM42 v3.20 (built with DMCP 3.22) — 2021-08-31

- Updated Free42 to version 3.0.5
- FIX: AGRAPH display corrupted by menu ([forum post](https://forum.swissmicros.com/viewtopic.php?f=17&t=2994))
- FIX: Output of the MEM command not fully displayed in program mode ([forum post](https://forum.swissmicros.com/viewtopic.php?f=17&t=3047))
- Added new font in two sizes (default after clean start)
- Fixes in original fonts

### DMCP changes

- Font updates and fixes

### DM42 User Manual

- Updated Settings menu

### DM42 Help File

- Updated Settings menu
- Updated About section

## DM42 v3.19 (built with DMCP 3.21) — 2021-05-13

- Free42 update to 3.0.3

## DM42 v3.18 (built with DMCP 3.21) — 2021-04-16

- Free42 update to 3.0.2
- PGMMENU [patch](https://github.com/thomasokken/free42/commit/3ef09eaa0aa94bbf7c86ef5d81d293075e77bd2b)
- All 6 special directories created after a FAT format

### DMCP changes

- Stabilization fixes to prevent issues related to the DM42 3.18 update

## DM42 v3.18 beta 2 (built with DMCP 3.21) — 2021-03-30

- Fixed allocation of the complex numbers

## DM42 v3.18 beta 1 (built with DMCP 3.21) — 2021-03-26

- Free42 update to 3.0.1
- Register allocation [patch](https://github.com/thomasokken/free42/commit/dc92bdb6121e42f53ac736740ddf7457d85b76bd)
- All 6 special directories created after a FAT format

### DMCP changes

- Stabilization fixes to prevent issues arising from DM42 3.18

## DM42 v3.17 (built with DMCP 3.20) — 2021-03-12

- Quick fix release only, no changes in DM42
- Fixed hypot() problem (see [forum post](https://forum.swissmicros.com/viewtopic.php?f=15&t=2859) for more details)

## DM42 v3.16 (built with DMCP 3.20) — 2020-10-09

- Free42 update to 2.5.20
- Fixed: No LCD repaint during PSE when RefLCD == 0
- Help File - Added Free42/DM42 flags

### DMCP changes

- Help system: Support for links between files
- Help system: Numpad like navigation keys

## DM42 v3.15 (built with DMCP 3.18) — 2020-03-30

- Free42 core update to 2.5.16
- State file extension renamed from '.s42' to '.f42' for compatibility with other platforms
- It is still possible to load '.s42' files and "Load State File" screen shows all '\*.?42' files now
- First load of foreign '.f42' file appends current DM42 specific state at the end of file
- 'Save State File' screen shows all '\*.?42' files too
- New state files have '.f42' extension and old '.s42' state files are renamed to '.f42' when used in 'Statefile Save'
- Thus, saved state files have '.f42' extension and should be directly usable on other platforms

### DMCP changes

- Fixed labels for date format change in 'Set Date' screen to match 'Set Time' time format change.
- File list: File filtering fix
- File list: Fix sporadic repeat of first chars in some filenames
- File list: Fix displaying zeroes and eventual hang at some pointwhile displaying directories with 100+ files.

## DM42 v3.14 (built with DMCP 3.15) — 2019-07-24

- New DMCP+DM42 combo fw only
- Look below for changes in DM42 v3.14 and DMCP v3.15

### DMCP v3.15 changes

- Improve response to simultaneous key presses

## DM42 v3.14 (built with DMCP 3.14) — 2019-07-16

- Update Free42 core to 2.2
- Fixed block graphics in 'Graphics in text' print
- Fixed bitmap error in print to graphics file
- Removed BOM from the printed text file
- Double NL printer flag
- Format date according to the flag 67
- Added RTC calibration possibility using /rtccalib.cfg file
- Added [\<--] as exit key to menus and screens

### DMCP v3.14 changes

- LCD handling enhancement
- Stability enhancement
- Keyboard handling enhancement

## DM42 v3.13 (built with DMCP 3.13) — 2019-03-15

- Help file renamed to dm42help.htm (automatically renames index.htm (you can download latest version from https://technical.swissmicros.com/dm42/fat/HELP/)
- Updated year in copyright messages
- Update Free42 core to 2.0.24
- Added flag 64 - value is 0 or 1 whether the shift was inactive or active (respectively) before last key press (useful in combination with KEYG/KEYX)

### DMCP v3.13 changes

- File listing enhancements - supports more files in directory listings, directory browsing and two column display
- Clear history buffer when help file changed
- Fix of hangs on some boards in various places (before or after flashing from FAT, after USB plug-in)

## DM42 v3.12 (built with DMCP 3.12) — 2019-01-22

- Update Free42 core to 2.0.22
- Fixed message font size (earlier followed font size of topmost register)
- Fixed missing pixels (as reported in EEVblog #1159 (https://www.youtube.com/watch?v=Ong91Ji3iDk)

### DMCP v3.12 changes

- Firmware update from FAT, doesn't wait for key press after successful flashing
- RESET+[+] jumps directly to MSC mode (checks for fw and keymap file and installs them without confirmation)
- Support for reset.bmp (loaded from /reset.bmp)
- Clarify DMY/MDY switching in date setting screen by removing [-1m] and adding [DMY]/[MDY].
- (Devel) System keymap support (loaded from /keymap.bin)
- (Testing) "System->Power OFF mode" menu item

## DM42 v3.11 (built with DMCP 3.11) — 2018-10-11

- Reverted to Intel® Decimal Floating-Point Math Library to version 2.0 Update 1
- Fixed div symbol problem if used as first character in alpha mode

### User Manual update

- [PDF version of user manual now available](https://technical.swissmicros.com/dm42/doc/dm42_user_manual.pdf)

### DMCP v3.11 update

- Fix for "Bug when connecting to USB cable"

## DM42 v3.10 (bult with DMCP 3.10) — 2018-10-01

- Update of Intel® Decimal Floating-Point Math Library to version 2.0 Update 2
- Build parameters tuned which gives ~5% speedup for calculations
- Calc help file updated to match current Setup menus [help_file_20180831.zip](https://technical.swissmicros.com/dm42/fat/HELP/help_file_20180831.zip)
- Off-images with flipped row order are accepted now
- Added printing to file (see ["Print to File" chapter](https://technical.swissmicros.com/dm42/doc/dm42_user_manual/#print_to_file) in DM42 User Manual)
- Fix the [issue with multi line messages and menus](https://forum.swissmicros.com/viewtopic.php?f=17&t=1960)
- Updated firmware build process - single firmware file should work now with dm_tool, dfu-util and from FAT update.

### User Manual update

- Print to File menu and functionality

### DMCP v3.10 update

- Upgrade system interface for bitmap handling to support print to file from DM42PGM

## DM42 v3.9.1 (built with DMCP 3.9a) — 2018-08-14

- Update to Free42 2.0.21
- Support for different font sizes in register stack (3. Settings > | 4. Stack Font Sizes >)
- Added LXYZT layout to stack layouts
- Displaying 'No program selected' when leaving 'save program' menu if nothing is selected (exited without note in earlier versions)

### User Manual updates in chapters

- Firmware Update
- Program Decoder/Encoder
- Changes since v3.7
- Quick Update Guide
- Program loading/update
- DMCP System Menu

### DMCP v3.9a update

- Menu lines aligned after line number

### DMCP v3.9 update

- Small number of boards exhibited excessive power-off current - fixed

### DMCP v3.8 update

- Fixed jump out of system menu to sleep
- Added program/system interface comparison to program info screen
- Extended DMCP interface to version 3.8 (added run_help_file() function)

## v3.7 — 2018-06-03

- Firmware split in two parts, DMCP and F42PGM

## v3.5 — 2018-03-25

- Flashing firmware from FAT disk (accessible from system menu)
- Second row of keys doesn't duplicate first row while the A..F menu is displayed
- Update to Free42 2.0.20

## v3.4a — 2018-03-07

- Fixed nonfunctional 'Beep Mute' in Settings menu

## v3.4 — 2018-03-06

- Speed improvement in battery mode
- Occasional lockup fix
- No need for RESET after fw flashing
- Fixed SEED 0
- Update to Free42 2.0.17
- Permanent menu flag (toggled by F2) now saved to state file

## v3.3 — 2018-02-12

- Modification of date/time settings dialogs
- Day increment problem fixed
- Prevent Help/Setup while program is running
- Added warning note to USB FAT disk screen
- Jump out of USB FAT disk mode now requires confirmation
- Changed LCD saving at power-down
- Partial input formatting fixed
- QSPI low-battery protection
- Force manual RESET after flashing
- Update to Free42 V2.0.11

## v3.2 — 2018-01-06

- UTF-8 up/down triangles swap fix
- Heavy calculation hang fix
- Free42 updated to V2.0.8
- Force RESET after flashing

## v3.1 — 2017-12-22

- Help text drawing fixes
- Free42 updated to V2.0.7
- '×' and '÷' glyphs in help system
- Font width calculation

## v3.0 — 2017-12-08

- Initial public release
