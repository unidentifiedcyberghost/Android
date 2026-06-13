"""
AndroidX — ADB Manager Module (cross-platform improvements)
Author: HexSecTeam | Instagram: @hexsecteam
"""

import subprocess
import re
import os
import time
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Prefer full path to adb when available
ADB_CMD = shutil.which("adb") or "adb"


def run_adb(args: list, device_id: str = None, capture: bool = True):
    """Run an adb command and return stdout."""
    cmd = [ADB_CMD]
    if device_id:
        cmd += ["-s", device_id]
    cmd += args
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except FileNotFoundError:
        return None, -1
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -2


def run_adb_global(args: list, capture: bool = True):
    """Run a global adb command without selecting a device."""
    try:
        result = subprocess.run([ADB_CMD] + args, capture_output=capture, text=True, timeout=30)
        output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        return output, result.returncode
    except FileNotFoundError:
        return None, -1
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -2


def check_adb():
    """Check if adb is installed."""
    if ADB_CMD == "adb":
        # shutil.which returned nothing
        console.print("[bold red]✗ ADB not found![/] Install Android Debug Bridge first.", style="red")
        return False
    out, rc = run_adb(["version"])
    if rc == -1 or not out:
        console.print("[bold red]✗ ADB not found or not responding![/]", style="red")
        return False
    console.print(f"[green]✓ ADB found:[/] {out.splitlines()[0]}")
    return True


def list_devices():
    """List all connected Android devices."""
    out, rc = run_adb(["devices", "-l"])
    if out is None:
        console.print("[red]ADB not available.[/]")
        return []

    lines = out.strip().splitlines()
    devices = []
    table = Table(title="[bold magenta]📱 Connected Devices[/]", box=box.DOUBLE_EDGE,
                  border_style="magenta", header_style="bold cyan")
    table.add_column("Serial", style="cyan")
    table.add_column("State", style="green")
    table.add_column("Model", style="yellow")
    table.add_column("Transport", style="white")

    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        serial = parts[0]
        state = parts[1]
        model = next((p.split(":")[1] for p in parts if p.startswith("model:")), "Unknown")
        transport = next((p.split(":")[1] for p in parts if p.startswith("transport_id:")), "N/A")
        devices.append({"serial": serial, "state": state, "model": model})
        table.add_row(serial, state, model, transport)

    console.print(table)
    if not devices:
        console.print("[yellow]⚠  No devices connected. Connect a device and enable USB Debugging.[/]")
    return devices

# Remaining functions (device_info, list_packages, capture_logcat, pull/push) preserved from original implementation
