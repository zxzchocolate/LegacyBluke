# USB debugging bridge (experimental)

This folder contains the Windows-side receiver for a future USB connection mode.

## Requirements
- Windows 10 or 11
- Python 3.10+ (mouse and keyboard receiver uses only the standard library)
- Android platform-tools (ADB)
- A USB data cable

## Start the Windows receiver
Open PowerShell in this folder and run:

    py .\legacybluke_usb_host.py

## Connect over USB debugging
On Android, enable Developer options and USB debugging, connect the phone, and accept the computer authorization prompt. Then run in another PowerShell window:

    adb devices
    adb reverse tcp:27183 tcp:27183

ADB reverse maps the phone's localhost port to the Windows receiver through the authorized USB debugging connection.

## Status and limitations
The host receiver handles relative mouse movement, mouse buttons, wheel, and virtual-key-code key press/release events over newline-delimited JSON.

**This is transport groundwork, not a finished in-app USB mode yet.** The Android app's existing controls are not wired to the bridge yet. Gamepad injection is not implemented; Windows requires a virtual gamepad driver/backend, which needs to be added separately. Existing Bluetooth support remains for Android 9+.

Only use ADB with devices you own or are authorized to administer.
