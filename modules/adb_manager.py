"""
DroidHunter — ADB Manager Module
Author: HexSecTeam | Instagram: @hexsecteam
"""

import subprocess
import re
import os
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def run_adb(args: list, device_id: str = None, capture: bool = True):
    """Run an adb command and return stdout."""
    cmd = ["adb"]
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
        result = subprocess.run(["adb"] + args, capture_output=capture, text=True, timeout=30)
        output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
        return output, result.returncode
    except FileNotFoundError:
        return None, -1
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -2


def check_adb():
    """Check if adb is installed."""
    out, rc = run_adb(["version"])
    if rc == -1:
        console.print("[bold red]✗ ADB not found![/] Install Android Debug Bridge first.", style="red")
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


def device_info(device_id: str):
    """Gather comprehensive device info."""
    props = {
        "Brand": "ro.product.brand",
        "Model": "ro.product.model",
        "Android Version": "ro.build.version.release",
        "SDK Level": "ro.build.version.sdk",
        "Build ID": "ro.build.id",
        "Security Patch": "ro.build.version.security_patch",
        "Fingerprint": "ro.build.fingerprint",
        "CPU ABI": "ro.product.cpu.abi",
        "IMEI (if rooted)": "ril.serialnumber",
        "Serial": "ro.serialno",
    }

    table = Table(title=f"[bold magenta]🔎 Device Info [{device_id}][/]",
                  box=box.SIMPLE_HEAVY, border_style="cyan", header_style="bold cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    for label, prop in props.items():
        val, _ = run_adb(["shell", f"getprop {prop}"], device_id)
        table.add_row(label, val or "[dim]N/A[/]")

    console.print(table)
