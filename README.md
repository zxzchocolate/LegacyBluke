# LegacyBluke

**A legacy-focused fork of Bluke for Android devices.**

LegacyBluke is a modified version of [Bluke](https://github.com/arnav-kr/Bluke), focused on adapting its codebase for older Android devices by removing dependencies on Android's `BluetoothHidDevice` API.

The goal is to make the project more compatible with legacy Android versions and explore alternative approaches to Bluetooth input functionality.

## Project Goals

- Remove direct dependencies on `BluetoothHidDevice`.
- Improve compatibility with older Android devices.
- Preserve useful parts of the original Bluke interface and functionality where possible.
- Provide a codebase for experimenting with legacy Bluetooth input support.
- Keep the project open source and easy to build.

## Compatibility

Compatibility depends on the Android version, device firmware, Bluetooth hardware, and the implementation used by the fork.

Removing `BluetoothHidDevice` does **not** automatically enable Bluetooth keyboard or mouse functionality. A replacement implementation or another supported communication method is needed for those features to work.

Some features from the original Bluke may be unavailable or incomplete in this fork.

## Building

### Requirements

- Android Studio
- A compatible JDK
- Android SDK components required by the project
- The included Gradle Wrapper

### Clone the repository

```bash
git clone https://github.com/zxzchocolate/LegacyBluke.git
cd LegacyBluke
```

### Build the debug APK

**Linux / macOS**

```bash
chmod +x gradlew
./gradlew assembleDebug
```

**Windows**

```powershell
.\gradlew.bat assembleDebug
```

The debug APK should be generated at:

```text
app/build/outputs/apk/debug/app-debug.apk
```

### Install on a connected device

Enable USB debugging, connect your Android device, and run:

```bash
./gradlew installDebug
```

On Windows, use:

```powershell
.\gradlew.bat installDebug
```

## Project Status

LegacyBluke is an experimental fork under active modification. Features, compatibility, and build requirements may differ from the original project as development continues.

## Upstream Project

LegacyBluke is based on [Bluke by arnav-kr](https://github.com/arnav-kr/Bluke).

The original project provides the foundation for the application's interface and input features. This fork modifies that codebase to investigate compatibility with older Android devices.

## License

This project retains the original project's **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for the applicable license terms.

## Credits

- [Bluke](https://github.com/arnav-kr/Bluke) — original project.
- [kbsim](https://github.com/tplai/kbsim) — source of some mechanical switch audio assets, as credited by the upstream project.

