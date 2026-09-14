# Voyager Firmware History

## V34 — 2025-04-15

### DM1x

- Default CPU speed is back to 12MHz
- Fixed: spurious [.] key press after dot/comma toggle from setup menu (ruined X value)
- Fixed: uninterpretable program/function when started from 2-line mode
- Fixed battery reading below 1.8V

### DM16

- Fixed internal RCL/STO address/offset calculation for MC0 firmware

### DM15

- Fixed: "Elelementary charge" (name of constant)
- Fixed: The kWh -> ft lbs conversion is displayed in the conversion menu as "\*2.655>6 ft lbs"
- Fixed: Non-interruptible program execution when GSB A is invoked as [f][Sqrt] or [Sqrt] in USER mode
- Fixed: No instruction mnemonics in subroutines (by J-F Garnier)

### DM12

- New 2-line mode, showing both the x- and y-registers simultaneously
- Added instruction mnemonic (in addition to key code) in Program Mode and when using SST/BST
- Function name preview
- Text descriptions for error codes

### DM41

- Added "Setup menu", simplifying access to all [ON]+key functions

## V33 — 2024-12-21

### DM41

- Corrected SETAF behavior for negative correction factors (caused time corruption)

### DM1x

- New "Setup Menu", simplifying access to all [ON]+key functions

### DM15/16

- New 2-line mode, showing both the x- and y-registers simultaneously
- Added instruction mnemonic (in addition to key code) in Program Mode and when using SST/BST
- Function name preview
- Text descriptions for error codes

### DM15

- "Constants and conversions" menu

### DM16

- New firmware version (DM16_MC0) with extended memory
- Enhanced version of SHOW HEX/DEC/OCT/BIN (preview complete numbers for HEX/DEC/OCT)

## V32 — 2021-08-31

### ALL

- Lowered consumption in serial console

### DM1x

- Added new 5x7 inspired font
- Default speed set to 12MHz to prolong battery life
- Added configuration key to toggle between annunciators on top or bottom
- Displaying "MEMORY CLEAR" instead of "Pr Error"

## V31 — 2020-10-19

### ALL

- Fixed battery consumption problem

## V30 — 2020-01-17

> !!! V30 firmware was removed after confirmation of excessive consumption in OFF mode

### ALL

- Added 'bootloader' serial console command
- Abandoned support for 32kB firmwares
- Improvements to Nut emulation layer

### DM41

- Stopwatch now generates 'TIMER ALARM' when SW is hidden as well when calculator is turned off.

## V29 — 2019-06-05

### DM41

- Past due alarm bypass at auto power-down

### DM15_Mxx

- GTO I: extended range to 999

### DM15_M80

- Change initial register allocation to match other DM15 models

## V28 — 2019-02-22

### DM1x

- Fixed irregular LCD blinking

### DM41

- Fixed non-responsive keys during ALARM acknowledgment period
- Emulation fixes - should fix earlier synthetic programming inaccuracies

## V27 — 2018-09-05

### DM1x

- Programs were sometimes almost impossible to stop e.g. when PSE was used in short loop. Now fixed.
- Fixed missing dot in program listing of RCL .1 and similar (for non-segment fonts)

### DM41

- Fixed continuous stopwatch operation

## V26 — 2018-03-25

- New bold 7-segment font (all DM1x models)
- Bugfix: Registers overwritten after numeric integration. Fixed in DM15_M80, released as DM15_M80_V16a_32k.hex for old 32k machines
- Bugfix: MEM output fixed in DM15_M80 and DM15_M1B

### DM41

- Speed improvement

## V25 — 2018-01-18

- Fixed timing of alarm catalog listing
- Fixed GETKEY delay to ~10s duration
- Added X-mem module to DM41
- New slim 7-segment font for DM1x models

## V24 — 2017-10-31

- Modify time module ROM to remap T/R/M keys from [7], [9] and [RCL] to landscape positions in ALMCAT
- Fixed PSE delay on all models

## V23 — 2017-05-10

- added manual setting of time and date
- fixed memory dump for DM12

## V22 — 2016-10-02

- Fixed occasional calculator hanging
- Changed init after reset (no moving text anymore), more battery friendly
- Fixed CAT 4/6 delay for DM41
- Fixed default date for DM41 (2014-01-01 Wednesday)

## V21 — 2016-03-03

- DM1X fixed PSE (keep any button pressed to interrupt)
- DMXX add setting via console to increase the time-out of the serial console mode
- DMXX Fixed julian date calculation ([ON]+[STO/RCL] +/- one hour just around midnight causing day transition)
- DM1X for all boards with RTC: add [ON]+[A] displaying the time with 1s increments by RTC and sleep in the mean time
- DMXX Add timeout to clock mode [ON]+[A] to 5min
- DM41 adjusted key mapping for LCD contrast settings to the same as the other models

## V19 — 2015-07-18

- DM41 bugfix ON-key conflicting with RTC (long running pgm suddenly stopped and sporadic lock-ups)

## V18 — 2015-04-23

- DM41 without extended module

## V17 — 2015-04-20

- initial release DM41 with extended module

## V16 — 2014-02-13

- fixed keyboard timing issues introduced in V15
- optimized power consumption
- DM15 versions include all three fonts in one firmware
- \*\*\* this will be the last firmware version \<32k; only newer calculators with an LPC1115 will be support by the next releases \*\*\*

## V15 — 2013-09-25

- rewritten keyscan routine - improved key respond - affects all models

## V14 — 2013-06-18

- enhanced pending key indicator for DM15
- LCD contrast setting changed - changing settings requires confirmation

## V13 — 2013-03-05

- fixed pending key indicator display (little square upper left corner)

## V12 — 2013-02-17

- fixed bug for complex mode in both extended ROMs versions for DM15C_M80 and DM15C_M1B (many thanks to Yukihiro Imanaga 今永之弘)

## V11 — 2013-01-22

- fixed SST autorepeat delay for 10C, 11C and 12C
- all model names are reduced from DM1xCC to DM1x
- extended memory version renamed from MEM80/MEM1B to M80/M1B

## V10 — 2012-11-26

- slim font added to all firmware versions ([ON]+[7] cycles through three fonts) except DM-15 has two different firmware versions each with only two fonts

## V9 — 2012-11-26

- added low battery indicator
- fixed serial communication race condition
- turning calc ON sends message to serial port

## V8 — 2012-08-29

- added self captured 16C ROM, now we got them all
- added LCD contrast settings [ON]+[CHS]
- updated annunciators in key-test for 10C

## V7 — 2012-07-15

- Fixed problem with MEM display on 15C
- added battery voltage displayed in [ON]+[E] screen
- added read battery voltage on console (calculators from first batch do not have a Vref diode)

## V6 — 2012-07-01

- removed the firmware naming 'VANILLA'
- all ROM files are based on own extraction except for the 16C which we don't have yet
- changed CPU speed to 48MHz. switch to 12MHz and back with [ON]+[9]

## V4 — 2012-04-04

- fixed PREFIX shows the enhanced MEM display

## V3 — 2012-03-25

- Enhanced MEM display for memory extended firmwares
- [ON]+[E] displays firmware version on LCD

## V2 — 2012-03-22

- initial release DM11CC

## V2 — 2012-03-14

- initial release DM12CC

## V2 — 2012-02-21

- corrected ROM in DM15CC_ROM_MEM80_V2.hex
- thanks to Jean-Francois Garnier for pointing to that mistake

## V1 — 2012-02-10

- initial versions DM15CC, DM16CC
