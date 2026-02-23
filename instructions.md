# Restoration Instructions

This document provides detailed instructions on how to use the files in this repository to restore your SwissMicros calculator to its factory defaults.

## Identify Your Calculator Series

First, determine which series your calculator belongs to:

- **Pioneer Models**: DM32, DM42, DM41X, DM42n, etc. These mount as a USB drive when connected to a computer and USB disk mode is activated.
- **Voyager Models**: DM11, DM12, DM15, DM16, DM41. The firmware for these models is typically flashed using a specific tool.

---

## 1. Pioneer Models (DM32, DM42, DM41X, etc.)

For Pioneer models, the factory default files are stored in directories named after the model (e.g., `Pioneer_Models/DM42`).

### Steps:
1.  **Backup**: Before proceeding, ensure you have backed up any important programs or data currently on your calculator. Restoring factory defaults may overwrite existing files.
2.  **Locate Files**: Navigate to the `Pioneer_Models` directory in this repository and find the subdirectory matching your calculator model.
    -   Example: For a DM42, go to `Pioneer_Models/DM42`.
3.  **Connect Calculator**: Connect your calculator to your computer via USB and activate USB disk mode from the setup menu. It should appear as a removable drive (e.g., `DM42`).
4.  **Copy Files**: Look for folders like `HELP`, `PROGRAMS`, and `OFFIMG` within the model's directory in this repository. Copy these folders to the root directory of your calculator's USB drive.
    -   **Overwrite**: If prompted, confirm that you want to overwrite existing files.
5.  **Firmware Updates**: If there are `.bin` files (firmware updates), these should be copied to the root of the calculator's drive. After copying, safely eject the drive. The update will be initiated automatically.

---

## 2. Voyager Models (DM11, DM12, DM15, DM16, DM41)

For Voyager models, the repository provides firmware files in `.hex` format located in the `Voyager_Models` directory.

### Steps:
1.  **Locate Firmware**: Navigate to the `Voyager_Models` directory and find the `.hex` file corresponding to your specific model variant.
2.  **Flashing Tool**: You will need a suitable flashing tool to write the firmware to your calculator. Common tools include the STM32CubeProgrammer or similar utilities compatible with the microcontroller used in your device.
3.  **Flash Firmware**:
    -   Connect your calculator to the computer using the appropriate interface/cable for flashing.
    -   Open your flashing software.
    -   Load the `.hex` file you downloaded.
    -   Execute the flash/program operation.
4.  **Verification**: After flashing is complete, disconnect the calculator and power it on to verify it is running the restored firmware.

---

## Troubleshooting

-   **File Mismatch**: Ensure you are using the files exactly matching your model number. Using files from a different model may cause unexpected behavior.
-   **Connection Issues**: If the calculator does not appear as a drive (Pioneer models), try a different USB cable or port.
-   **Flashing Failures** (Voyager models): Check your connection and ensure the battery level is sufficient before flashing.
