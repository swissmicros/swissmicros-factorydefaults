# DM32 Program Firmware History

> Please remember it is always wise to make FAT disk backup before any update.

Platform firmware: see [DMCP5 system firmware history](../DMCP5_HISTORY.md)
([upstream](https://technical.swissmicros.com/dmcp/firmware_dmcp5/history.html)).

## DM32 v2.11 — 2025-12-05

### Fixes

- Fixed: crash after using equation solver with Flag-11 ([forum](https://forum.swissmicros.com/viewtopic.php?f=33&t=4159))
- Font design: visually improved a selection of glyphs in the SwissKeys font (the "bold" font).

## DM32 v2.10 — 2024-08-17

### Fixes

- Fixed: Difference in error messages (STAT ERROR and INVALID y^x)
- Fixed: SOLVE (i) asks for solve variable

## End of Beta Phase

## DM32 v2.09 — 2024-05-06

### Enhancements

- Added RANDSEED to statefile
- Statefile parsing enhancements
- Stack Right-align option

## DM32 v2.08 — 2024-03-18

### Enhancements

- Added CPU frequency switching when powered from USB
- Added remote calls from CALC mode
- Added Extended GTO functionality ([see in doc](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_moving_to_a_specific_program_line_with_gto))
- Added support for automatic load of dependent states ([see in doc](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_load_statefile_dependencies))

### Fixes

- Fixed: The '0' style doesn't match register font in SHOW box
- Fixed: F3 (SST) should act only if no other key processing is pending
- Fixed: F3 (SST) long press to NULL behavior
- Fixed: Remote XEQ calls to current context
- Fixed: First remote XEQ call should clear remote call stack
- Fixed: Current state filename should be pre-selected in "Save" dialog

## DM32 v2.07 — 2023-12-08

### Enhancements

- Added remote XEQ functionality ([see in manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_remote_xeq))
- Added SHOW view of EQN message
- SHOW extended to all program lines in program mode

### Fixes

- F2 key (i.e. debug view toggle) deactivated for non-CALC modes and during number entry
- Fixed USB disk id to 0483:5720 so it corresponds to USB MSC by STM
- Fixed: Program SOLVE ending in "NO ROOT FOUND" prevents subsequently keyed XEQ from running (until pressing [R/S])
- Fixed: Number entered as '1E-' ([E][+/-]) should be interpreted as '1'
- Fixed: Message triangle cut-off after File->Load Clean State
- Fixed: Left/right scrolling of long EQN message (i.e. EQN in PRGM mode with flag10 set) doesn't work

## DM32 v2.06 — 2023-11-01

- Added "Debug View" ([see in manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_debug_view))
- Added Step-out and Step-over ([see in manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_single_step_execution))
- SHOW box style changed to better match overall look
- Fixed: Sometimes SHOW displays "SHOW" instead of expected text on long key press
- Fixed: Wrong CLEAR menu in PRGM and EQN mode after elaborated key combinations
- SHOW hold isn't killed by shift presses (simplifies screenshot invocation)
- SHOW hold isn't canceled by screenshot
- Fixed: Integration ends on overflow when Flag5=0 (should give an integration result) .. this also fixed a problem with restarting integration after an overflow
- Fixed: Memory corruption in EQN list (reported by Raul). Exhibit itself during EQN edit by displaying "NO EQN" on other lines and all those equations are lost.

## DM32 v2.05 — 2023-09-08

### New enhancements:

- Extended Registers ([see in manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#indirect_only))
- New GUI for MEM->VAR list
- New GUI for MEM->PGM list
- New GUI for EQN list
- New GUI for PRGM mode
- SHOW hold functionality ([see in manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#show_hold))

## DM32 v2.04 — 2023-08-01

### Fixes

- Fixed possible cause of: Crash when too long filename is used
- Fixed: Integ x^(-0.5) from 0 to 1 fails
- Fixed: Precise log10 for integer powers
- Substituted "Press EXIT" for "Press ON" in DMCP5
- Fixed: STOP in Solve and Integ functions doesn't halt the program
- Support for stepping through Integration and Solve
- Fixed: Wrong Solve output when initial guess is already a root
- Fixed: Sporadic hang in Integration
- Fixed: VIEW stack lift inconsistency
- Fixed: "NO ROOT RND" in Solar Compass
- Fixed: Displaying of RUNNING/INTEGRATING/SOLVING based on actual PRGM/Integ/Solve state
- Fixed: Use multiplication to evaluate integer factorials
- Fixed: No root for solve Z=X^Y
- Statefile cleanup: Remove redundant MFRAC keyword, add missing /c value
- Fixed: Precise XROOT calculations for integer values
- Fixed: Incorrect complex power (real negative integer)
- Fixed: Y-register (error) negative for integration from A to B if A>B
- Fixed: R/S displays PRGM step during enter of EQN parameter
- Fixed: RTN in CALC mode should work as GTO..
- Fixed: GTO.. should clear call stack
- Fixed: Getting BARG when SOLVE is re-activated during previous SOLVE input
- Fixed: Reset state after any state-file load error
- State restore after RESET: Prioritize existence of STATES.CFG even if the default state isn't set
- Fixed: No function preview on key hold when Solve input is active
- Experimental mapping F5=Up, F6=Down

## DM32 v2.03 — 2023-06-15

### Fixes

- Fixed: Wrong display update during Integrate (Display is constantly repainted instead of steady INTEGRATING message)
- Fixed: Integration/Solve restart doesn't work
- Fixed: FN= setting isn't stored in statefile
- Fixed: Integration isn't internally terminated after an error (doesn't allow to start new integration after an error)
- Fixed: 'Div by 0' in Example2 of Inverse-Normal Distribution
- Fixed: Reflect SCI setting in Integration (Handling of errors in Integration algorithm depends on FIX/SCI mode setting)
- Fixed: Error in Exampe2 of "Polynomial Root Finder"
- Fixed: DM32 vs 32SII difference Statistics Normal Distribution Program Stack Z not the same
- Fixed: Wrong program size display in MEM->PGM
- Fixed: program edit: R/S during number input fails
- Fixed: In calc menus F-keys act immediately
- Fixed: SHOW doesn't reflect inverted dot/comma mode
- Fixed: Wrong display of RADIX, in inverted dot/comma mode
- Fixed: Remove debug numbers from header title
- Fixed: Stack values lost upon INPUT in program

## DM32 v2.02 — 2023-05-21

- Initial public release
