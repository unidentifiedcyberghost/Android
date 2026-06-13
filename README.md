<div align="center">

# 👻 AndroidX
### AndroidX — Advanced Android Offensive Framework

**Developed by:** (developed by https://github.com/unidentifiedcyberghost x https://github.com/pinoyunknown : white-hat : Philippine Cybersecurity Experts)

[![Instagram](https://img.shields.io/badge/Instagram-pinoyunknown-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/pinoyunknown)
[![X](https://img.shields.io/badge/X-hPsuomynonA-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/hPsuomynonA)
[![GitHub](https://img.shields.io/badge/GitHub-unidentifiedcyberghost-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/unidentifiedcyberghost)
[![GitHub](https://img.shields.io/badge/GitHub-pinoyunknown-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pinoyunknown)

![Version](https://img.shields.io/badge/Version-2.0.0-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-cyan?style=for-the-badge&logo=python)

> ⚠️ **For authorized security testing, research, and education only.**

</div>

---

## Overview

AndroidX is an offensive Android tooling framework built for red-teamers, security researchers, and penetration testers who need a single, scriptable CLI to perform comprehensive Android assessments. AndroidX focuses on pragmatic workflows: quickly enumerating devices, performing thorough static APK analysis, scanning networks, producing attack payloads and assisting controlled exploit actions for authorized engagements.

This README has been customized to reflect AndroidX's goals and usage; it intentionally differs from other forks and predecessors.


## What makes AndroidX different

- Unified UX: a colorful, consistent terminal UI focused on speed and clarity.
- Cross-platform: works on Windows 10/11 and common Linux distributions.
- Offensive-first features: helper flows and templates for exploitation (for use only with explicit authorization).
- Extensible: modular design so you can add Frida scripts, YARA rules, or custom payload templates.


## Features (short)

- Device management (ADB): enumerate devices, detailed device info, screenshots, logcats
- APK static auditing: permission analysis, exported component detection, secret scanning
- Network scanning: port scanning, subnet discovery, WiFi information
- Vulnerability heuristics: CVE checks, root checks, insecure storage detection
- Exploit helpers: launch activities, trigger broadcasts, deep-link fuzzing, content provider access
- Payload generation: msfvenom command templates, reverse-shell lists, adb payload scripts
- Reporting: export JSON and styled HTML reports for delivery


## Requirements & Notes

- Python 3.8+ (3.10/3.11 recommended)
- pip
- Dependencies: see requirements.txt (rich, requests)
- Optional tools (recommended for full feature set): adb, scrcpy, msfvenom, frida/objection, mitmproxy


## Quick install (Windows & Linux)

Follow the platform instructions in the earlier README section or use these condensed commands.

Windows (PowerShell):
```powershell
git clone https://github.com/unidentifiedcyberghost/Android.git
cd Android
py -3 -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
py AndroidX.py
```

Linux (Debian/Ubuntu):
```bash
git clone https://github.com/unidentifiedcyberghost/Android.git
cd Android
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 AndroidX.py
```


## Usage examples

Interactive mode (recommended):
```bash
python3 AndroidX.py
```

Scripted mode (examples):
```bash
# List devices
python3 AndroidX.py --devices

# Analyze an APK and generate HTML report
python3 AndroidX.py --apk myapp.apk --report html --report-out myreport.html

# Scan a device's IP for open ports
python3 AndroidX.py --device ABC123 --port-scan
```


## Visual & CLI style changes

- The CLI has a cyan-focused theme (cyan borders, bright-cyan titles) and rounded border boxes to improve readability.
- All interactive menus and panels are tuned for high-contrast terminals such as Windows Terminal, PowerShell, and modern Linux terminals.


## Legal & Safety Reminder

AndroidX is a powerful offensive toolkit. It must only be used when you have explicit written authorization. The creators accept no responsibility for misuse. Always gather written permission before performing offensive actions.


## Contributing & Packaging

If you want distribution builds (.exe/.AppImage), I can add CI workflows to build one-file PyInstaller artifacts. I can also help add a --no-banner flag and safe-mode defaults on request.


## License

MIT License — see LICENSE file.
