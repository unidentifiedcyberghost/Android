#!/usr/bin/env python3
"""
Modified from AndroidX (forked)
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

# color gradient for banner lines
BANNER_LINES_GRADIENT = [
    "blue", "bright_blue", "yellow", "bright_yellow", "red", "bright_red"
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

    # On Windows terminals some colors / fast clears can flicker; use fewer frames
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
            # fallback: print newlines
            print("\n" * 40)
        for gl in glitch_lines:
            console.print(Align.center(gl))
        time.sleep(pause)

    # Settling phase (line by line reveal)
    try:
        console.clear()
    except Exception:
        print("\n" * 40)
    for i, line in enumerate(lines):
        color = BANNER_LINES_GRADIENT[i % len(BANNER_LINES_GRADIENT)]
        console.print(Align.center(f"[bold {color}]{line}[/]"))
        time.sleep(0.04)


def print_banner():
    """Print the animated AndroidX banner with developer credit under it."""
    animate_glitch_banner()

    # Developer credit printed under the banner
    console.print()
    console.print(Align.center(Text(DEV_CREDIT_LINE, style="bold white")))
    console.print()

    # Tagline
    tagline = Text("◈ ADVANCED ANDROID PENTESTING FRAMEWORK ◈", style="bold italic bright_magenta")
    console.print(Align.center(tagline))
    console.print()

    # Status Panel
    status_text = get_banner_status()
    console.print(Align.center(Panel(
        status_text,
        border_style="magenta",
        box=box.HORIZONTALS,
        padding=(0, 2),
        title="[bold magenta]System Status[/]",
        title_align="left"
    )))
    console.print()


# Note: Many functions in this file (menus, handlers, build_parser, interactive_mode, cli_mode)
# are preserved from the original project. The codebase's modules were also updated to
# be more cross-platform where required (ping flags, adb detection). AndroidX aims to run
# on Windows 10/11 and on Linux. Some features (scrcpy, msfvenom) remain platform-specific
# external tools and will be detected at runtime.


# ════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════

def main():
    parser = build_parser()

    if len(sys.argv) == 1:
        # No args → interactive
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
        console.print("\n\n[bold magenta]👻 AndroidX interrupted. Stay ethical.[/]\n")
        sys.exit(0)
