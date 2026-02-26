# Restoration Instructions

This document provides detailed instructions on how to use the files in this repository to restore your SwissMicros calculator to its factory defaults.

## Identify Your Calculator Series

First, determine which series your calculator belongs to:

- **Pioneer Models**: DM32, DM42, DM41X, and R47. (Includes variants like DM42n and DM41Xn; STM32U5 CPU). These mount as a USB drive when connected to a computer and USB disk mode is activated.
- **Voyager Models**: DM11, DM12, DM15, DM16, DM41 (LPC1115 CPU). The firmware for these models is typically flashed using a specific tool.

---

## 1. Pioneer Models (DM32, DM42, DM41X, R47)

For Pioneer models, the factory default files are stored in directories named after the model (e.g., `Pioneer_Models/DM42`).

**Note regarding R47:** The R47 is a community-developed project (see [GitLab releases](https://gitlab.com/rpncalculators/c43/-/releases)). Although not yet fully public, it is available via this [hidden shop link](https://www.swissmicros.com/product/model-r47).

### Steps:
1.  **Backup**: Before proceeding, ensure you have backed up any important programs or data currently on your calculator. Restoring factory defaults may overwrite existing files.
2.  **Locate Files**: Navigate to the `Pioneer_Models` directory in this repository and find the subdirectory matching your calculator model.
    -   Example: For a DM42, go to `Pioneer_Models/DM42`.
3.  **Connect Calculator**: Connect your calculator to your computer via USB and activate USB disk mode from the setup menu. It should appear as a removable drive (e.g., `DM42`).
4.  **Copy Files**: Look for folders like `HELP`, `PROGRAMS`, and `OFFIMG` within the model's directory in this repository. Copy these folders to the root directory of your calculator's USB drive.
    -   **Overwrite**: If prompted, confirm that you want to overwrite existing files.
5.  **Firmware Updates**: If there are `.bin` files (firmware updates), these should be copied to the root of the calculator's drive. After copying, safely eject the drive. The update will be initiated automatically.

*Note: For advanced recovery or if the USB disk method is unavailable, the `STM32CubeProgrammer` tool can be used with Pioneer models.*

---

## 2. Voyager Models (DM11, DM12, DM15, DM16, DM41)

For Voyager models, the firmware can be updated easily using the web-based Voyager Web Tool.

### Steps:
1.  **Open Web Tool**: Navigate to [https://tech.swissmicros.com/FlashingTool/](https://tech.swissmicros.com/FlashingTool/) using a browser that supports WebSerial (e.g., Chrome, Edge, Opera).
2.  **Connect**: Connect your calculator to your computer via USB and click the **Connect** button in the web tool.
3.  **Select Firmware**: Switch to the **Firmware** tab. You can select the desired firmware from the dropdown menu or load a local `.hex` file from the `Voyager_Models` directory of this repository.
4.  **Flash**:
    -   **Enter Bootloader Mode**:
        -   **Method 1 (Menu)**: On the calculator, go to `SETUP` -> `SYSTEM` -> `Bootloader` (see [User Manual](https://technical.swissmicros.com/voyager/doc/voyager_user_manual.html#conf_bootloader)).
        -   **Method 2 (No Battery)**: Since the USB chip (CP2102) is powered by the cable, you can enter bootloader mode without a battery. Connect the calculator via USB, click **Connect** in the web tool, then insert the battery within 1-2 seconds.
        -   *Note: Newer models with LPC111X CPUs do not have a physical bootloader button.*
    -   Click **Flash** to start the update process.
5.  **Verification**: After flashing is complete, the calculator will restart with the new firmware.

*Note: The legacy method using `lpc21isp` or `FlashMagic` is still possible but the Web Tool is recommended for ease of use.*

---

## Troubleshooting

-   **File Mismatch**: Ensure you are using the files exactly matching your model number. Using files from a different model may cause unexpected behavior.
-   **Connection Issues**: If the calculator does not appear as a drive (Pioneer models), try a different USB cable or port.
-   **Flashing Failures** (Voyager models): Check your connection and ensure the battery level is sufficient before flashing.
