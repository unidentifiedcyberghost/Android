#!/usr/bin/env python3
"""
AndroidX — full CLI entrypoint (merged from original DroidHunter logic, adapted)
"""

import argparse
import sys
import os
import time
import json
import random
import shutil
import subprocess
import platform

# ── Rich UI ───────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.align import Align
    from rich.columns import Columns
except ImportError:
    print("[!] 'rich' not installed. Run: pip install rich")
    sys.exit(1)

# ── Modules ──────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from modules import adb_manager, apk_analyzer, network_scanner
from modules import vulnerability_scanner, exploit_engine, payload_generator, report_generator

console = Console()

VERSION     = "2.0.0"
AUTHOR      = "unidentifiedcyberghost x pinoyunknown"
INSTAGRAM   = "@unidentifiedcyberghost"
TOOL_NAME   = "AndroidX"
YEAR        = "2026"
OS_NAME     = platform.system()

# Glitch animation toggle
GLITCH_ENABLED = True


# ════════════════════════════════════════════════════════════════
#  BANNER & ANIMATION (Fixed "A n d r o i d X")
# ════════════════════════════════════════════════════════════════

BANNER_ART = r"""
  A   n   d   r   o   i   d       X
  ___  _  _  _  _  _  _  _  _  _ 
 / _ \| \| \| \| \| \| \| \| \| |
| | | |  |  |  |  |  |  |  |  | |
| | | |  |  |  |  |  |  |  |  | |
| |_| |  |  |  |  |  |  |  |  | |
 \___/|__|__|__|__|__|__|__|__|_|

           PHILIPPINE FLAG — ANDROIDX
"""

BANNER_LINES_GRADIENT = [
    "cyan", "bright_cyan", "yellow", "bright_yellow", "red", "bright_red"
]

DEV_CREDIT_LINE = "(developed by https://github.com/unidentifiedcyberghost x https://github.com/pinoyunknown : white-hat : Philippine Cybersecurity Experts)"


def get_banner_status():
    """Gather live status info for the banner."""
    try:
        devices = adb_manager.list_devices()
        device_count = len(devices)
        status_color = "green" if device_count > 0 else "red"
        device_text = f"[{status_color}]{device_count} Connected[/]"
    except Exception:
        device_text = "[yellow]ADB Not Found[/]"

    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")

    return (
        f"📅 [bold white]{now}[/]  |  "
        f"📱 [bold cyan]Devices:[/] {device_text}  |  "
        f"🚀 [bold green]v{VERSION}[/]  |  "
        f"OS: [bold yellow]{OS_NAME}[/]"
    )


def animate_glitch_banner():
    """Display a subtle reveal for the banner. Works cross-platform."""
    from rich.markup import escape
    lines = BANNER_ART.strip("\n").split("\n")

    frames = 8 if OS_NAME.startswith("Windows") else 12
    pause = 0.08 if OS_NAME.startswith("Windows") else 0.05

    chars = "01$#!@%^&*()_+=-[]{}|;:,.<>?/"
    for _ in range(frames):
        glitch_lines = []
        for line in lines:
            glitch_line = "".join(random.choice(chars) if c != " " else " " for c in line)
            color = random.choice(BANNER_LINES_GRADIENT)
            glitch_lines.append(f"[bold {color}]{escape(glitch_line)}[/]")
        try:
            console.clear()
        except Exception:
            print("\n" * 40)
        for gl in glitch_lines:
            console.print(Align.center(gl))
        time.sleep(pause)

    try:
        console.clear()
    except Exception:
        print("\n" * 40)
    for i, line in enumerate(lines):
        color = BANNER_LINES_GRADIENT[i % len(BANNER_LINES_GRADIENT)]
        console.print(Align.center(f"[bold {color}]{line}[/]"))
        time.sleep(0.04)


def glitch_print_center(text: str, frames: int = 8, intensity: float = 0.35, pause: float = 0.04):
    """Show a quick glitch animation for a centered text block.

    This prints several frames with random character substitutions then the original text.
    It intentionally prints frames above the following content to avoid complex cursor control across terminals.
    """
    if not GLITCH_ENABLED:
        console.print(Align.center(text))
        return

    glyphs = "█▓▒░#@%$&*<>?/|^~☆★01ABCxyz"
    lines = text.strip("\n").split("\n")

    for _ in range(frames):
        for line in lines:
            glitched = []
            for ch in line:
                if ch == " " or random.random() > intensity:
                    glitched.append(ch)
                else:
                    glitched.append(random.choice(glyphs))
            console.print(Align.center(f"[bold bright_cyan]{''.join(glitched)}[/]"))
        time.sleep(pause)
    # print the clean text
    for line in lines:
        console.print(Align.center(f"[bold cyan]{line}[/]"))


def print_banner():
    """Print the animated AndroidX banner with developer credit under it."""
    animate_glitch_banner()

    console.print()
    console.print(Align.center(Text(DEV_CREDIT_LINE, style="bold white")))
    console.print()

    tagline = Text("◈ ADVANCED ANDROID PENTESTING FRAMEWORK ◈", style="bold italic bright_cyan")
    console.print(Align.center(tagline))
    console.print()

    status_text = get_banner_status()
    console.print(Align.center(Panel(
        status_text,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 2),
        title="[bold cyan]System Status[/]",
        title_align="left"
    )))
    console.print()


# ════════════════════════════════════════════════════════════════
#  MAIN MENU, HANDLERS, SESSION STORAGE, CLI
# ════════════════════════════════════════════════════════════════

MENU_OPTIONS = [
    ("1",  "📱", "Device Manager",          "List & manage connected Android devices"),
    ("2",  "🔎", "APK Static Analyzer",     "Decompile & audit an APK file"),
    ("3",  "🌐", "Network Scanner",         "Port scan, WiFi info, host discovery"),
    ("4",  "🚨", "Vulnerability Scanner",   "CVE mapping, root check, insecure storage"),
    ("5",  "💥", "Exploit Engine",          "Launch activities, deep links, shell dropper"),
    ("6",  "🎯", "Payload Generator",       "APK payloads, reverse shells, obfuscation"),
    ("7",  "📋", "Report Generator",        "Generate HTML/JSON security report"),
    ("8",  "📡", "ADB WiFi Connect",        "Enable & connect ADB over WiFi"),
    ("9",  "⚡", "Auto ADB WiFi Connect",   "Automatically switch USB ADB to WiFi mode"),
    ("10", "📸", "Screenshot Capture",      "Capture device screenshot via ADB"),
    ("11", "📦", "Package Manager",         "Enumerate installed packages"),
    ("12", "🐛", "Logcat Analyzer",         "Capture & analyze logcat for secrets"),
    ("13", "🔐", "SSL Pinning Check",       "Detect SSL pinning in target app"),
    ("14", "📂", "File Transfer",           "Pull/push files from/to device"),
    ("15", "💻", "Interactive ADB Shell",   "Drop into live ADB shell"),
    ("16", "🧰", "Remote Control",          "Remote screen, file explorer, camera and device control tools"),
    ("17", "❔", "About",                   "About AndroidX"),
    ("0",  "🚪", "Exit",                    "Exit AndroidX"),
]

REMOTE_CONTROL_OPTIONS = [
    ("1", "🖥️", "Open Remote Screen", "Open Android screen with scrcpy"),
    ("2", "📁", "File Explorer",      "Browse device files"),
    ("3", "📷", "Remote Camera",      "Open remote camera tools"),
    ("4", "📸", "Take Screenshot",    "Capture device screenshot"),
    ("5", "🎥", "Screen Record",      "Record device screen"),
    ("0", "↩️", "Back",               "Return to main menu"),
]


# Session store
_SESSION = {"findings": [], "permissions": [], "secrets": [], "urls": []}


def _save_to_session(data: dict, source: str):
    if isinstance(data, dict):
        for vuln in data.get("vulnerabilities", []):
            _SESSION["findings"].append(vuln)
        for vuln in data.get("cves", []):
            _SESSION["findings"].append({
                "name": vuln.get("cve", "CVE"),
                "severity": vuln.get("severity", "MEDIUM"),
                "detail": vuln.get("detail", ""),
                "cve": vuln.get("cve"),
            })
        _SESSION["permissions"].extend(data.get("dangerous_permissions", []))
        _SESSION["secrets"].extend(data.get("secrets", []))
        _SESSION["urls"].extend(data.get("urls", []))


def _get_session() -> dict:
    return _SESSION.copy()


# Helper functions and menus

def print_main_menu():
    # Optionally show a quick glitch intro for the menu header
    header = "\n👻  {name}  —  Main Menu\n".format(name=TOOL_NAME)
    if GLITCH_ENABLED:
        glitch_print_center(header, frames=6, intensity=0.28, pause=0.03)

    t = Table(
        title=f"\n[bold bright_cyan]👻  {TOOL_NAME}  —  Main Menu[/]\n",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold white",
        show_lines=True,
        min_width=70,
    )
    t.add_column("  #  ",   style="bold cyan",   width=5,  no_wrap=True)
    t.add_column("  ",      style="bold cyan",   width=4,  no_wrap=True, justify="center")
    t.add_column("Module",  style="bold bright_cyan",   min_width=24)
    t.add_column("Description", style="bright_cyan",      min_width=34)

    for num, icon, name, desc in MENU_OPTIONS:
        style = "on #001a1a" if num == "0" else ""
        t.add_row(f"[bold cyan] {num} [/]", icon, f"[bright_cyan]{name}[/]", f"[cyan]{desc}[/]", style=style)

    console.print(t)


def print_remote_control_menu():
    header = "\n🎛️  {name}  —  Remote Control\n".format(name=TOOL_NAME)
    if GLITCH_ENABLED:
        glitch_print_center(header, frames=4, intensity=0.28, pause=0.03)

    t = Table(
        title=f"\n[bold bright_cyan]🎛️  {TOOL_NAME}  —  Remote Control[/]\n",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold white",
        show_lines=True,
        min_width=70,
    )
    t.add_column("  #  ",   style="bold cyan",   width=5,  no_wrap=True)
    t.add_column("  ",      style="bold cyan",             width=3,  no_wrap=True)
    t.add_column("Module",  style="bold bright_cyan",   min_width=24)
    t.add_column("Description", style="bright_cyan",      min_width=38)

    for num, icon, name, desc in REMOTE_CONTROL_OPTIONS:
        style = "on #001a1a" if num == "0" else ""
        t.add_row(f"[bold cyan] {num} [/]", icon, f"[bright_cyan]{name}[/]", f"[cyan]{desc}[/]", style=style)

    console.print(t)


def select_device() -> str:
    devices = adb_manager.list_devices()
    if not devices:
        return None
    if len(devices) == 1:
        dev = devices[0]["serial"]
        console.print(f"[bright_cyan]Auto-selected device:[/] {dev}")
        return dev
    serial = Prompt.ask("[cyan]Enter device serial[/]")
    return serial


# Module handlers (simplified references to modules)

def handle_device_manager():
    console.rule("[bold cyan]📱 Device Manager[/]")
    adb_manager.check_adb()
    device_id = select_device()
    if not device_id:
        return
    adb_manager.device_info(device_id)


def handle_apk_analyzer():
    console.rule("[bold cyan]🔎 APK Static Analyzer[/]")
    apk_path = Prompt.ask("[cyan]APK file path[/]")
    findings  = apk_analyzer.analyze_apk(apk_path)
    if Confirm.ask("[cyan]Save findings to report?[/]", default=True):
        _save_to_session(findings, "apk_analysis")
        console.print("[bright_cyan]✓ Added to session report.[/]")


def handle_network_scanner():
    console.rule("[bold cyan]🌐 Network Scanner[/]")
    choice = Prompt.ask("[cyan]Scan mode[/]", choices=["device", "host", "wifi", "discover", "mitm"], default="device")

    if choice == "device":
        device_id = select_device()
        if not device_id:
            return
        ip = network_scanner.get_device_ip(device_id)
        if ip:
            console.print(f"[bright_cyan]Device IP:[/] {ip}")
            network_scanner.port_scan(ip)
        else:
            console.print("[red]Could not determine device IP.[/]")

    elif choice == "host":
        target = Prompt.ask("[cyan]Target IP/hostname[/]")
        port_range = Prompt.ask("[cyan]Port range (comma-list or 'all')[/]", default="common")
        if port_range == "all":
            ports = list(range(1, 65536))
        elif port_range == "common":
            ports = None
        else:
            ports = [int(p.strip()) for p in port_range.split(",") if p.strip().isdigit()]
        network_scanner.port_scan(target, ports)

    elif choice == "wifi":
        device_id = select_device()
        if device_id:
            network_scanner.get_wifi_info(device_id)

    elif choice == "discover":
        subnet = Prompt.ask("[cyan]Subnet (e.g. 192.168.1)[/]")
        network_scanner.discover_devices(subnet)

    elif choice == "mitm":
        network_scanner.mitm_setup_guide()


def handle_vulnerability_scanner():
    console.rule("[bold cyan]🚨 Vulnerability Scanner[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg = Prompt.ask("[cyan]Target package (leave blank for device-level only)[/", default="")
    report = vulnerability_scanner.full_vulnerability_scan(device_id, pkg or None)
    _save_to_session(report, "vulnerability_scan")


def handle_exploit_engine():
    console.rule("[bold cyan]💥 Exploit Engine[/]")
    device_id = select_device()
    if not device_id:
        return

    exploit_engine.exploit_menu(device_id)
    choice = Prompt.ask("[red]Select exploit[/]", choices=[str(i) for i in range(10)])

    if choice == "1":
        pkg  = Prompt.ask("[cyan]Package name[/]")
        act  = Prompt.ask("[cyan]Activity class[/]")
        exploit_engine.launch_exported_activity(device_id, pkg, act)

    elif choice == "2":
        pkg    = Prompt.ask("[cyan]Package name[/]")
        action = Prompt.ask("[cyan]Intent action[/]")
        exploit_engine.trigger_broadcast_receiver(device_id, pkg, action)

    elif choice == "3":
        uri = Prompt.ask("[cyan]Content provider URI (content://...)[/]")
        exploit_engine.extract_content_provider(device_id, uri)

    elif choice == "4":
        pkg    = Prompt.ask("[cyan]Package name[/]")
        scheme = Prompt.ask("[cyan]Deep link scheme (e.g. myapp)[/]")
        exploit_engine.deep_link_fuzzer(device_id, pkg, scheme)

    elif choice == "5":
        pkg = Prompt.ask("[cyan]Package name[/]")
        exploit_engine.frida_injection_guide(pkg)

    elif choice == "6":
        lhost = Prompt.ask("[cyan]LHOST[/]")
        lport = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        exploit_engine.shell_payload_dropper(device_id, lhost, lport)

    elif choice == "7":
        pkg  = Prompt.ask("[cyan]Package name[/]")
        db   = Prompt.ask("[cyan]Database filename[/]")
        exploit_engine.extract_database(device_id, pkg, db)

    elif choice == "8":
        exploit_engine.bypass_lock_screen(device_id)

    elif choice == "9":
        exploit_engine.enable_developer_options(device_id)


def handle_payload_generator():
    console.rule("[bold cyan]🎯 Payload Generator[/]")
    payload_generator.payload_menu()
    choice = Prompt.ask("[red]Select payload type[/]", choices=["1", "2", "3", "4", "5", "0"])

    if choice == "1":
        lhost  = Prompt.ask("[cyan]LHOST[/]")
        lport  = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        ptype  = Prompt.ask("[cyan]Payload type[/]",
                             choices=["reverse_tcp", "reverse_https", "reverse_http", "shell_tcp"],
                             default="reverse_tcp")
        output = Prompt.ask("[cyan]Output file[/]", default="payload.apk")
        payload_generator.generate_msfvenom_apk(lhost, lport, ptype, output)

    elif choice == "2":
        action = Prompt.ask("[cyan]Intent action[/]")
        comp   = Prompt.ask("[cyan]Component (pkg/class or blank)[/]", default="")
        data   = Prompt.ask("[cyan]Data URI (or blank)[/]", default="")
        payload_generator.generate_intent_payload(action, comp or None, data or None)

    elif choice == "3":
        lhost = Prompt.ask("[cyan]LHOST[/]")
        lport = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        payload_generator.generate_reverse_shell_commands(lhost, lport)

    elif choice == "4":
        lhost  = Prompt.ask("[cyan]LHOST[/]")
        lport  = IntPrompt.ask("[cyan]LPORT[/]", default=4444)
        output = Prompt.ask("[cyan]Script filename[/]", default="adb_payload.sh")
        payload_generator.generate_adb_payload_script(None, lhost, lport, output)

    elif choice == "5":
        raw   = Prompt.ask("[cyan]Payload to obfuscate[/]")
        method = Prompt.ask("[cyan]Obfuscation method[/]", choices=["base64", "hex"], default="base64")
        payload_generator.obfuscate_payload(raw, method)


def handle_report_generator():
    console.rule("[bold cyan]📋 Report Generator[/]")
    target = Prompt.ask("[cyan]Target description (app/device name)[/], default=\"Unknown Target\"")

    data = _get_session()
    data["target"] = target

    fmt = Prompt.ask("[cyan]Report format[/]", choices=["html", "json", "both", "table"], default="html")

    if fmt in ("html", "both"):
        out = Prompt.ask("[cyan]HTML output filename[/]", default="androidx_report.html")
        report_generator.generate_html_report(data, out)

    if fmt in ("json", "both"):
        out = Prompt.ask("[cyan]JSON output filename[/]", default="androidx_report.json")
        report_generator.generate_json_report(data, out)

    if fmt == "table":
        report_generator.print_summary_table(data)


def handle_adb_wifi():
    console.rule("[bold cyan]📡 ADB WiFi Connect[/]")
    device_id = select_device()
    if not device_id:
        return
    port = IntPrompt.ask("[cyan]Port[/]", default=5555)
    adb_manager.enable_adb_wifi(device_id, port)


def handle_auto_adb_wifi():
    console.rule("[bold cyan]⚡ Auto ADB WiFi Connect[/]")
    device_id = select_device()
    if not device_id:
        return
    adb_manager.auto_adb_wifi_connect(device_id, 5555)


def handle_screenshot():
    console.rule("[bold cyan]📸 Screenshot Capture[/]")
    device_id = select_device()
    if not device_id:
        return
    path = adb_manager.take_screenshot(device_id)
    if path:
        console.print(f"[bold bright_cyan]✓ Screenshot saved:[/] {path}")


def handle_package_manager():
    console.rule("[bold cyan]📦 Package Manager[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg_type = Prompt.ask("[cyan]Package filter[/]",
                           choices=["all", "system", "third_party", "disabled"],
                           default="third_party")
    adb_manager.list_packages(device_id, pkg_type)


def handle_logcat():
    console.rule("[bold cyan]🐛 Logcat Analyzer[/]")
    device_id = select_device()
    if not device_id:
        return
    lines = IntPrompt.ask("[cyan]Lines to capture[/]", default=300)
    adb_manager.capture_logcat(device_id, lines)


def handle_ssl_check():
    console.rule("[bold cyan]🔐 SSL Pinning Check[/]")
    device_id = select_device()
    if not device_id:
        return
    pkg = Prompt.ask("[cyan]Package name[/]")
    network_scanner.check_ssl_pinning(device_id, pkg)


def handle_file_transfer():
    console.rule("[bold cyan]📂 File Transfer[/]")
    device_id = select_device()
    if not device_id:
        return
    direction = Prompt.ask("[cyan]Direction[/]", choices=["pull", "push"])
    if direction == "pull":
        remote = Prompt.ask("[cyan]Remote path (on device)[/]")
        local  = Prompt.ask("[cyan]Local destination[/]", default=".")
        adb_manager.pull_file(device_id, remote, local)
    else:
        local  = Prompt.ask("[cyan]Local file path[/]")
        remote = Prompt.ask("[cyan]Remote destination (on device)[/]")
        adb_manager.push_file(device_id, local, remote)


def handle_adb_shell():
    console.rule("[bold cyan]💻 Interactive ADB Shell[/]")
    device_id = select_device()
    if not device_id:
        return
    adb_manager.interactive_shell(device_id)


def check_scrcpy() -> bool:
    if shutil.which("scrcpy"):
        return True
    console.print("[bold red]scrcpy not found.[/] Install it with: [bold cyan]sudo apt install scrcpy[/]")
    return False


def open_remote_screen(device_id: str) -> bool:
    cmd = [
        "scrcpy",
        "-s", device_id,
        "--window-title", "Remote Screen",
        "--max-size", "900",
    ]
    try:
        subprocess.Popen(cmd)
        console.print("[bold bright_cyan]Remote Screen launched.[/]")
        return True
    except FileNotFoundError:
        console.print("[bold red]scrcpy not found.[/] Install it with: [bold cyan]sudo apt install scrcpy[/]")
    except OSError as exc:
        console.print(f"[bold red]Failed to launch Remote Screen:[/] {exc}")
    return False


def handle_remote_control():
    while True:
        console.print()
        print_remote_control_menu()
        valid_choices = [num for num, *_ in REMOTE_CONTROL_OPTIONS]
        choice = Prompt.ask("\n[bold cyan]Remote Control ▶[/]", choices=valid_choices, show_choices=False)

        if choice == "0":
            return

        if choice == "1":
            if not check_scrcpy():
                continue
            device_id = select_device()
            if not device_id:
                continue
            open_remote_screen(device_id)
            continue

        console.print("[yellow]This feature is not ready yet.[/]")


def handle_about():
    about = Panel(
        f"\n"
        f"  [bold cyan]👻  {TOOL_NAME} v{VERSION}[/]\n\n"
        f"  [bold bright_cyan]Advanced Android Penetration Testing Framework[/]\n\n"
        f"  [white]A comprehensive tool for ethical hackers and security professionals.\n"
        f"  Covers static APK analysis, dynamic runtime analysis via ADB,\n"
        f"  network scanning, vulnerability mapping, exploit assistance,\n"
        f"  payload generation, and professional report generation.[/]\n\n"
        f"  [bold cyan]Author   :[/] [white]{AUTHOR}[/]\n"
        f"  [bold cyan]Contact  :[/] [bright_cyan]{INSTAGRAM}[/]\n"
        f"  [bold cyan]Built to :[/] [white]Build to Exploit Android Devices using AndroidX[/]\n"
        f"  [bold cyan]Year     :[/] [white]{YEAR}[/]\n\n"
        f"  [bold red]⚠  For authorized penetration testing use only.[/]\n"
        f"  [dim]Unauthorized use is illegal and unethical.[/]\n",
        title="[bold]About AndroidX[/]",
        border_style="cyan",
        padding=(0, 4),
    )
    console.print(about)


# Handler map
HANDLER_MAP = {
    "1":  handle_device_manager,
    "2":  handle_apk_analyzer,
    "3":  handle_network_scanner,
    "4":  handle_vulnerability_scanner,
    "5":  handle_exploit_engine,
    "6":  handle_payload_generator,
    "7":  handle_report_generator,
    "8":  handle_adb_wifi,
    "9":  handle_auto_adb_wifi,
    "10": handle_screenshot,
    "11": handle_package_manager,
    "12": handle_logcat,
    "13": handle_ssl_check,
    "14": handle_file_transfer,
    "15": handle_adb_shell,
    "16": handle_remote_control,
    "17": handle_about,
}


def interactive_mode():
    print_banner()
    console.print(Panel(
        "[bold red]⚠  LEGAL DISCLAIMER[/]\n\n"
        "[white]AndroidX is designed for authorized security testing ONLY.\n"
        "Use of this tool against systems you do not own or have explicit written\n"
        "permission to test is [bold red]ILLEGAL[/] and may result in criminal prosecution.\n"
        "The author assumes no liability for misuse.[/]",
        border_style="red", padding=(0, 2)))

    if not Confirm.ask("\n[bold red]I confirm I have authorization to test the target system[/]", default=False):
        console.print("[yellow]Exiting. Obtain proper authorization before testing.[/]")
        sys.exit(0)

    while True:
        console.print()
        print_main_menu()
        valid_choices = [num for num, *_ in MENU_OPTIONS]
        choice = Prompt.ask("\n[bold cyan]AndroidX ▶[/]", choices=valid_choices, show_choices=False)

        if choice == "0":
            console.print("\n[bold bright_cyan]👻 Exiting AndroidX. Stay ethical.[/]\n")
            sys.exit(0)

        handler = HANDLER_MAP.get(choice)
        if handler:
            try:
                console.print()
                handler()
            except KeyboardInterrupt:
                console.print("\n[yellow]↩ Returned to main menu.[/]")
            except Exception as e:
                console.print(f"\n[bold red]✗ Error:[/] {e}")
        else:
            console.print("[red]Invalid option.[/]")

        console.print()
        Prompt.ask("[dim]Press ENTER to continue[/]", default="")


# ════════════════════════════════════════════════════════════════
#  CLI MODE  (argparse)
# ════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="androidx",
        description=f"{TOOL_NAME} v{VERSION} — Advanced Android Pentesting Tool by {AUTHOR}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AndroidX.py --interactive
  python3 AndroidX.py --apk app.apk --report html
  python3 AndroidX.py --device ABC123 --vuln-scan --pkg com.example.app
  python3 AndroidX.py --device ABC123 --port-scan
  python3 AndroidX.py --payload reverse_tcp --lhost 10.0.0.1 --lport 4444
  python3 AndroidX.py --device ABC123 --exploit deep-link --pkg com.example --scheme myapp
  python3 AndroidX.py --devices
        """
    )

    p.add_argument("--interactive", "-i",  action="store_true",    help="Launch interactive menu mode")
    p.add_argument("--version",     "-v",  action="store_true",    help="Show version")

    # Device
    dg = p.add_argument_group("Device")
    dg.add_argument("--devices",           action="store_true",    help="List connected devices")
    dg.add_argument("--device", "-d",      metavar="SERIAL",       help="Target device serial number")
    dg.add_argument("--info",              action="store_true",    help="Show device info")
    dg.add_argument("--shell",             metavar="CMD",          help="Run ADB shell command")
    dg.add_argument("--adb-shell",         action="store_true",    help="Drop into interactive ADB shell")
    dg.add_argument("--adb-wifi",          action="store_true",    help="Enable ADB over WiFi")
    dg.add_argument("--screenshot",        action="store_true",    help="Capture device screenshot")
    dg.add_argument("--logcat",            metavar="N", type=int,  help="Capture N lines of logcat", nargs="?", const=200)
    dg.add_argument("--packages",          choices=["all","system","third_party","disabled"],
                                                                   help="List installed packages")
    dg.add_argument("--pull",              metavar="REMOTE",       help="Pull file from device")
    dg.add_argument("--push",             nargs=2, metavar=("LOCAL","REMOTE"), help="Push file to device")

    # APK Analysis
    ag = p.add_argument_group("APK Analysis")
    ag.add_argument("--apk",              metavar="FILE",          help="APK file to analyze")

    # Network
    ng = p.add_argument_group("Network")
    ng.add_argument("--port-scan",        action="store_true",    help="Port scan device IP")
    ng.add_argument("--target",           metavar="IP",           help="Explicit scan target IP")
    ng.add_argument("--ports",            metavar="PORTS",        help="Comma-separated ports or 'all'")
    ng.add_argument("--wifi-info",        action="store_true",    help="Show WiFi info")
    ng.add_argument("--discover",         metavar="SUBNET",       help="Discover hosts on subnet")
    ng.add_argument("--ssl-pinning",      metavar="PKG",          help="Check SSL pinning for package")
    ng.add_argument("--mitm-guide",       action="store_true",    help="Show MitM setup guide")

    # Vulnerability
    vg = p.add_argument_group("Vulnerability")
    vg.add_argument("--vuln-scan",        action="store_true",    help="Run full vulnerability scan")
    vg.add_argument("--pkg",             metavar="PKG",           help="Target package name")
    vg.add_argument("--cve-check",       action="store_true",     help="Check Android CVEs for device")
    vg.add_argument("--root-check",      action="store_true",     help="Check if device is rooted")

    # Exploit
    eg = p.add_argument_group("Exploit")
    eg.add_argument("--exploit",          metavar="MODULE",
                    choices=["activity","broadcast","provider","deep-link","frida","shell-drop","db-extract","lock-bypass","dev-options"],
                    help="Exploit module to run")
    eg.add_argument("--activity",         metavar="CLASS",        help="Activity class for --exploit activity")
    eg.add_argument("--action",           metavar="ACTION",       help="Intent action")
    eg.add_argument("--uri",              metavar="URI",          help="URI for content provider / deep link")
    eg.add_argument("--scheme",           metavar="SCHEME",       help="Deep link scheme")
    eg.add_argument("--lhost",            metavar="IP",           help="Listener host")
    eg.add_argument("--lport",            metavar="PORT", type=int, default=4444, help="Listener port")
    eg.add_argument("--db-name",          metavar="DB",           help="Database filename to extract")

    # Payload
    pg = p.add_argument_group("Payload")
    pg.add_argument("--payload",          metavar="TYPE",
                    choices=["reverse_tcp","reverse_https","reverse_http","shell_tcp",
                             "intent","reverse-shells","adb-script","obfuscate"],
                    help="Generate a payload")
    pg.add_argument("--payload-out",      metavar="FILE",         help="Output file for payload")
    pg.add_argument("--obfuscate-method", choices=["base64","hex"], default="base64",
                    help="Obfuscation method")
    pg.add_argument("--raw-payload",      metavar="CMD",          help="Payload string to obfuscate")

    # Report
    rg = p.add_argument_group("Report")
    rg.add_argument("--report",           choices=["html","json","both","table"],
                    help="Generate report after scan")
    rg.add_argument("--report-out",       metavar="FILE",         help="Report output filename")
    rg.add_argument("--target-name",      metavar="NAME",         help="Target name for report", default="Unknown Target")

    return p


def cli_mode(args):
    """Run CLI operations based on parsed arguments."""
    print_banner()

    device_id = args.device
    apk_data = {}

    if args.version:
        console.print(f"[bold cyan]{TOOL_NAME}[/] v[bold bright_cyan]{VERSION}[/] by [bold]{AUTHOR}[/]")
        return

    if args.devices:
        adb_manager.check_adb()
        adb_manager.list_devices()

    if args.info and device_id:
        adb_manager.device_info(device_id)

    if args.shell and device_id:
        adb_manager.shell_cmd(device_id, args.shell)

    if args.adb_shell and device_id:
        adb_manager.interactive_shell(device_id)

    if args.adb_wifi and device_id:
        adb_manager.enable_adb_wifi(device_id, args.lport)

    if args.screenshot and device_id:
        adb_manager.take_screenshot(device_id)

    if args.logcat is not None and device_id:
        adb_manager.capture_logcat(device_id, args.logcat)

    if args.packages and device_id:
        adb_manager.list_packages(device_id, args.packages)

    if args.pull and device_id:
        adb_manager.pull_file(device_id, args.pull)

    if args.push and device_id:
        adb_manager.push_file(device_id, args.push[0], args.push[1])

    if args.apk:
        apk_data = apk_analyzer.analyze_apk(args.apk)
        _save_to_session(apk_data, "apk")

    if args.port_scan:
        target = args.target
        if not target and device_id:
            target = network_scanner.get_device_ip(device_id)
        if target:
            ports = None
            if args.ports == "all":
                ports = list(range(1, 65536))
            elif args.ports:
                ports = [int(p) for p in args.ports.split(",") if p.strip().isdigit()]
            network_scanner.port_scan(target, ports)
        else:
            console.print("[red]Provide --target or --device for port scan.[/]")

    if args.wifi_info and device_id:
        network_scanner.get_wifi_info(device_id)

    if args.discover:
        network_scanner.discover_devices(args.discover)

    if args.ssl_pinning and device_id:
        network_scanner.check_ssl_pinning(device_id, args.ssl_pinning)

    if args.mitm_guide:
        network_scanner.mitm_setup_guide()

    if args.vuln_scan and device_id:
        report = vulnerability_scanner.full_vulnerability_scan(device_id, args.pkg)
        _save_to_session(report, "vuln")

    if args.cve_check and device_id:
        findings = vulnerability_scanner.check_android_version_cves(device_id)
        _save_to_session({"cves": findings}, "cve")

    if args.root_check and device_id:
        vulnerability_scanner.check_root_status(device_id)

    if args.exploit and device_id:
        ex = args.exploit
        if ex == "activity":
            exploit_engine.launch_exported_activity(device_id, args.pkg, args.activity)
        elif ex == "broadcast":
            exploit_engine.trigger_broadcast_receiver(device_id, args.pkg, args.action)
        elif ex == "provider":
            exploit_engine.extract_content_provider(device_id, args.uri)
        elif ex == "deep-link":
            exploit_engine.deep_link_fuzzer(device_id, args.pkg, args.scheme)
        elif ex == "frida":
            exploit_engine.frida_injection_guide(args.pkg)
        elif ex == "shell-drop":
            exploit_engine.shell_payload_dropper(device_id, args.lhost, args.lport)
        elif ex == "db-extract":
            exploit_engine.extract_database(device_id, args.pkg, args.db_name)
        elif ex == "lock-bypass":
            exploit_engine.bypass_lock_screen(device_id)
        elif ex == "dev-options":
            exploit_engine.enable_developer_options(device_id)

    if args.payload:
        out = args.payload_out
        if args.payload in ("reverse_tcp","reverse_https","reverse_http","shell_tcp"):
            payload_generator.generate_msfvenom_apk(args.lhost, args.lport, args.payload, out or "payload.apk")
        elif args.payload == "intent":
            payload_generator.generate_intent_payload(args.action, args.pkg, args.uri)
        elif args.payload == "reverse-shells":
            payload_generator.generate_reverse_shell_commands(args.lhost, args.lport)
        elif args.payload == "adb-script":
            payload_generator.generate_adb_payload_script(device_id, args.lhost, args.lport, out or "adb_payload.sh")
        elif args.payload == "obfuscate":
            payload_generator.obfuscate_payload(args.raw_payload or "", args.obfuscate_method)

    if args.report:
        data = _get_session()
        data["target"] = args.target_name
        if apk_data:
            data.update(apk_data)
        if args.report in ("html", "both"):
            out = args.report_out or "androidx_report.html"
            report_generator.generate_html_report(data, out)
        if args.report in ("json", "both"):
            out = args.report_out or "androidx_report.json"
            report_generator.generate_json_report(data, out)
        if args.report == "table":
            report_generator.print_summary_table(data)


# ════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════

def main():
    parser = build_parser()

    if len(sys.argv) == 1:
        interactive_mode()
        return

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        cli_mode(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold bright_cyan]👻 AndroidX interrupted. Stay ethical.[/]\n")
        sys.exit(0)
