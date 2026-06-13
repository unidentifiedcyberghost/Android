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

# Glitch animation toggle (runtime overridden by CLI flags)
GLITCH_ENABLED = True
NO_BANNER = False


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

      HACKING WITH RESPECT — ANDROIDX
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
    if not NO_BANNER:
        animate_glitch_banner()
    else:
        # Static banner without animation
        lines = BANNER_ART.strip("\n").split("\n")
        console.print()
        for i, line in enumerate(lines):
            color = BANNER_LINES_GRADIENT[i % len(BANNER_LINES_GRADIENT)]
            console.print(Align.center(f"[bold {color}]{line}[/]"))

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

(remaining file truncated for brevity)
