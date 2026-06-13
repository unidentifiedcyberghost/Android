<div align="center">

# 👻 AndroidX
### AndroidX — Android Security Assessment / Penetration Testing Framework

**Developed by:** (developed by https://github.com/unidentifiedcyberghost x https://github.com/pinoyunknown : white-hat : Philippine Cybersecurity Experts)

![Version](https://img.shields.io/badge/Version-2.0.0-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-cyan?style=for-the-badge&logo=python)

> ⚠️ **For authorized security testing and educational purposes only.**

</div>

---

## What is AndroidX?

AndroidX is a CLI-based Android security assessment and penetration testing framework designed for ethical hackers, security researchers, and developers to perform authorized testing and auditing of Android devices and applications. AndroidX provides device management, APK static analysis, network scanning, vulnerability checks, exploit helpers, payload generation, remote control helpers, and professional report generation — all from a single terminal interface.

Core goals:
- Provide a unified, user-friendly CLI for common Android security workflows.
- Offer both interactive and scripted CLI modes for automation and repeatable testing.
- Work cross-platform (Windows 10/11 and Linux) with clear runtime checks for optional external tooling.


## Features

- Device Manager: list devices, device info, screenshots, logcat capture, file transfer, interactive ADB shell
- APK Static Analyzer: permission audit, hardcoded secret detection, exported components, basic vulnerability heuristics
- Network Scanner: port scanning, subnet discovery, WiFi info
- Vulnerability Scanner: CVE mapping heuristics, root detection, insecure storage checks
- Exploit Helpers: activity launch, deep-link fuzzer, broadcast trigger, content provider extraction
- Payload Generator: msfvenom wrapper command templates, adb payload scripts, reverse shell commands, obfuscation utilities
- Report Generator: HTML/JSON report export and CLI summary tables


## Requirements

- Python 3.8+ (3.10/3.11 recommended)
- pip
- Modules (install via requirements.txt): rich, requests
- Optional external tools for full functionality:
  - adb (Android Platform Tools) — required for device interactions
  - scrcpy — optional (remote screen streaming)
  - msfvenom / Metasploit — optional (payload generation)
  - frida / objection — optional (dynamic instrumentation)
  - mitmproxy — optional (network interception)


## Legal Disclaimer (Read Carefully)

AndroidX is a toolset intended for professional security assessments, education, and authorized penetration testing only. Use of AndroidX against systems or devices for which you do not have explicit, written permission is illegal and unethical.

By using AndroidX you confirm that:
- You own the device or application under test, OR
- You have explicit written authorization from the device owner or organization to perform the testing.

The authors and contributors assume no responsibility for misuse. Unauthorized activities may lead to civil and criminal liability.

If you are unsure whether you have permission to test a target, do not proceed and obtain written authorization first.


## Installation

Follow the instructions for your OS below.

### Windows 10 / Windows 11

1) Install Python 3.8+ and ensure `python` or `py` is on your PATH.
2) Install Android Platform Tools (adb):
   - Download "platform-tools" from Google and add the folder containing adb.exe to your PATH environment variable.
   - Verify: open PowerShell or Windows Terminal and run `adb version`.
3) Clone this repository and create a virtual environment:
   ```powershell
   git clone https://github.com/unidentifiedcyberghost/Android.git
   cd Android
   py -3 -m venv venv
   venv\Scripts\Activate.ps1    # PowerShell
   # or: venv\Scripts\activate.bat  (cmd.exe)
   pip install -r requirements.txt
   ```
4) Run AndroidX:
   ```powershell
   py AndroidX.py
   # or
   python AndroidX.py
   ```

Notes for Windows:
- Use Windows Terminal or PowerShell for best ANSI/color support.
- If `scrcpy` is not available on Windows, remote-screen features will be disabled (the CLI detects this).


### Linux (Debian/Ubuntu example)

1) Install Python 3.8+ and git.
2) Install adb and scrcpy (optional):
   ```bash
   sudo apt update
   sudo apt install -y adb scrcpy
   ```
3) Clone and install dependencies:
   ```bash
   git clone https://github.com/unidentifiedcyberghost/Android.git
   cd Android
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4) Run AndroidX:
   ```bash
   python3 AndroidX.py
   ```


## Quick Usage Guide

AndroidX supports two primary modes: interactive menu mode and CLI (flags) mode.

### Interactive Mode (Recommended)

Start the interactive UI:
```bash
python3 AndroidX.py
# or
py AndroidX.py
```

The interactive mode shows the animated banner, a system status panel, and a menu of modules. Navigate the options by entering the menu numbers.

Example flow:
- 1 → Device Manager → list devices → select a device → take screenshot
- 2 → APK Static Analyzer → provide APK path → generate JSON/HTML report


### CLI Mode (Scriptable)

Use flags to automate tasks in scripts or CI. Examples:

- List connected devices:
  ```bash
  python3 AndroidX.py --devices
  ```

- Full device info:
  ```bash
  python3 AndroidX.py --device ABC123 --info
  ```

- Analyze APK and produce HTML report:
  ```bash
  python3 AndroidX.py --apk target.apk --report html --target-name "com.example.app"
  ```

- Port scan device IP:
  ```bash
  python3 AndroidX.py --device ABC123 --port-scan
  ```

- Full vulnerability scan on device:
  ```bash
  python3 AndroidX.py --device ABC123 --vuln-scan --pkg com.example.app
  ```

- Capture last 200 lines of logcat:
  ```bash
  python3 AndroidX.py --device ABC123 --logcat 200
  ```

- Enable ADB over WiFi:
  ```bash
  python3 AndroidX.py --device ABC123 --adb-wifi
  ```

Run `python3 AndroidX.py --help` to see the full list of CLI flags and options.


## Optional Packaging

If you prefer a standalone executable (Windows .exe or Linux single-file binary), I can produce PyInstaller builds. Let me know which platforms you want and I will prepare release binaries.


## Configuration & Safety

- You can toggle the animated banner by editing the `AndroidX.py` file (comment out `animate_glitch_banner()` call inside `print_banner()`), or I can add a `--no-banner` flag if you want.
- A safe-mode option can be added to disable payload/exploit features; ask me and I will implement it.


## Troubleshooting

- "adb not found": ensure Android Platform Tools are installed and `adb` is on PATH.
- Colors/animations look broken on Windows cmd: use Windows Terminal or PowerShell, or disable banner animations.
- msfvenom or scrcpy features show "not found": install those external tools if you need those features.


## Contributing

Contributions are welcome. Open an issue or PR if you want new features, bug fixes, or packaging help.


## License

MIT License — see LICENSE file. The original license is preserved. Redistribution and modification are permitted under the MIT terms.
