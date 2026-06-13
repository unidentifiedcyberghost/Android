## CLI Wrappers (scripts/)

To support automation and CI, AndroidX includes small wrapper scripts under `scripts/` that provide minimal argparse-driven CLIs for common functionality. They import the corresponding `modules/` code so they are thin shells that are easy to integrate into pipelines.

Note: place the scripts in `scripts/` and make them executable:
- mkdir -p scripts
- paste the scripts (adb_cli.py, analyze_apk.py, port_scan.py, generate_report.py)
- chmod +x scripts/*.py

### adb_cli.py
Purpose: thin wrapper around modules/adb_manager for listing devices, checking adb, and running arbitrary adb subcommands.

Usage:
- List devices (prints JSON array of device objects):
  - python scripts/adb_cli.py list
- Check ADB availability:
  - python scripts/adb_cli.py check
- Run arbitrary adb args (pass adb args after `--`):
  - python scripts/adb_cli.py run --device DEVICE_SERIAL -- shell id

Example:
- python scripts/adb_cli.py run --device emulator-5554 -- shell getprop ro.build.version.release

Output format:
- JSON with keys such as returncode and stdout for `run`, and arrays/objects for `list` and `check`.

### analyze_apk.py
Purpose: run static analysis on an APK (wraps modules/apk_analyzer.analyze_apk) and optionally write JSON output.

Usage:
- Print results to stdout:
  - python scripts/analyze_apk.py path/to/app.apk
- Save to JSON:
  - python scripts/analyze_apk.py path/to/app.apk --out findings.json

Example:
- python scripts/analyze_apk.py examples/app.apk --out out/apk_findings.json

Output:
- JSON object representing findings, permissions, CVEs, secrets, etc. (matching module return format).

### port_scan.py
Purpose: quick multithreaded port scanner wrapper for modules/network_scanner.port_scan.

Usage:
- Scan default/common ports:
  - python scripts/port_scan.py 192.168.1.5
- Scan explicit ports:
  - python scripts/port_scan.py 192.168.1.5 --ports 22,80,443
- Set per-port timeout:
  - python scripts/port_scan.py 192.168.1.5 --timeout 0.5

Example:
- python scripts/port_scan.py 10.0.0.42 --ports 22,80,5555

Output:
- JSON: { "target": "<target>", "open_ports": [ <port ints> ] }

### generate_report.py
Purpose: produce a JSON or HTML report from findings/session JSON. If `modules.report_generator` exposes a `generate_report` function, the wrapper will try to use it; otherwise it falls back to writing raw JSON or a simple HTML file.

Usage:
- Generate HTML from findings:
  - python scripts/generate_report.py --findings findings.json --out report.html --format html
- Generate JSON output (sanity/roundtrip):
  - python scripts/generate_report.py --findings findings.json --out summary.json --format json

Example:
- python scripts/generate_report.py --findings out/apk_findings.json --out reports/report.html --format html

Fallback behavior:
- If no `modules.report_generator` implementation is present, `--format json` writes the raw JSON and `--format html` writes a basic HTML page with the JSON embedded.

---

## Full Command Reference (Interactive + CLI Mode)

### Interactive main menu (launch via `python AndroidX.py` or `python AndroidX.py --interactive`)
Menu options (select the number in the TUI):
- 1  📱 Device Manager — List & manage connected Android devices (ADB)
- 2  🔎 APK Static Analyzer — Decompile & audit an APK file
- 3  🌐 Network Scanner — Port scan, WiFi info, host discovery
- 4  🚨 Vulnerability Scanner — CVE mapping, root detection, insecure storage checks
- 5  💥 Exploit Engine — Launch activities, deep links, shell dropper (use responsibly)
- 6  🎯 Payload Generator — Build APK payloads, reverse shells, apply obfuscation
- 7  📋 Report Generator — Generate HTML/JSON security report from session/findings
- 8  📡 ADB WiFi Connect — Enable & connect ADB over WiFi
- 9  ⚡ Auto ADB WiFi Connect — Auto-switch USB ADB to TCP/IP WiFi mode
- 10 📸 Screenshot Capture — Capture device screenshot via ADB
- 11 📦 Package Manager — Enumerate installed packages on device
- 12 🐛 Logcat Analyzer — Capture & analyze logcat output for secrets
- 13 🔐 SSL Pinning Check — Detect potential SSL pinning in an app
- 14 📂 File Transfer — Pull/push files to/from device
- 15 💻 Interactive ADB Shell — Open an interactive adb shell on device
- 16 🧰 Remote Control — Remote screen, file explorer, camera and control tools (scrcpy, etc.)
- 17 ❔ About — Show version/credits
- 0  🚪 Exit

Each menu item guides you through required prompts (device serial, file path, IP address, etc.). Findings can be saved to the session and exported via Reports.

### CLI flags (AndroidX.py)
- --interactive, -i
  - Start interactive TUI (default way to use the tool for humans).
- --version, -v
  - Print version and exit.
- --no-banner
  - Disable animated ASCII banner (show static banner + status instead).
- --no-glitch
  - Disable per-header glitch animation (quiet mode). Overrides other glitch flags.
- --glitch-frames INT
  - Override default header glitch frame count (int).
- --glitch-intensity FLOAT
  - Override header glitch intensity (0.0–1.0).
- --glitch-pause FLOAT
  - Override pause (seconds) between glitch frames.

Examples:
- Start interactive with quiet UI:
  - python AndroidX.py --interactive --no-glitch --no-banner
- Start with adjusted glitch:
  - python AndroidX.py --glitch-frames 4 --glitch-intensity 0.12 --glitch-pause 0.02

### Wrapper commands summary (scripts/)
- scripts/adb_cli.py
  - list, check, run
  - e.g. python scripts/adb_cli.py list
- scripts/analyze_apk.py
  - analyze APK, optionally write JSON
  - e.g. python scripts/analyze_apk.py app.apk --out findings.json
- scripts/port_scan.py
  - port scanning helper
  - e.g. python scripts/port_scan.py 192.168.1.5 --ports 22,80,443
- scripts/generate_report.py
  - generate report from saved findings/session JSON
  - e.g. python scripts/generate_report.py --findings findings.json --out report.html --format html

---

## Example automation workflows

1) Auto-run APK analysis and produce JSON:
- python scripts/analyze_apk.py app.apk --out findings.json

2) Scan the app build server for exposed adb port:
- python scripts/port_scan.py build-server.example.com --ports 5555,22

3) Run quick device checks from a CI job (list devices, check adb):
- python scripts/adb_cli.py check
- python scripts/adb_cli.py list

4) Generate a report after tests:
- python scripts/generate_report.py --findings findings.json --out report.html --format html

---

## Next steps
- Add more wrapper scripts for payload generation, exploit engine calls, and automated vulnerability scans.
- Optionally add a `--quiet` flag to AndroidX.py to produce pure JSON outputs for automation.
- If you want, I can commit these scripts and the README updates on a branch and open a PR for you.
