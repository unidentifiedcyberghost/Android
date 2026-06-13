#!/usr/bin/env python3
"""
scripts/adb_cli.py
Small CLI wrapper for modules/adb_manager.py
Usage examples:
  python scripts/adb_cli.py list
  python scripts/adb_cli.py check
  python scripts/adb_cli.py run --device DEVICE_SERIAL -- adb shell id
"""
import sys
import argparse
sys.path.insert(0, ".")

from modules import adb_manager as adb
import json


def cmd_list(args):
    devices = adb.list_devices()
    # list_devices already prints a rich table; also output JSON for automation
    print(json.dumps(devices, indent=2))


def cmd_check(args):
    ok = adb.check_adb()
    print(json.dumps({"adb_ok": bool(ok)}))


def cmd_run(args):
    # run arbitrary adb subcommand (pass after --)
    if not args.command:
        print("No adb command provided. Use -- to separate adb args.")
        return
    device = args.device
    # args.command may include a leading '--' from argparse.REMAINDER; strip it
    cmd = args.command
    if len(cmd) > 0 and cmd[0] == "--":
        cmd = cmd[1:]
    out, rc = adb.run_adb(cmd, device_id=device)
    print(json.dumps({"returncode": rc, "stdout": out}))


def main():
    p = argparse.ArgumentParser(prog="adb_cli")
    sub = p.add_subparsers(dest="cmd")
    s_list = sub.add_parser("list", help="List connected devices")
    s_list.set_defaults(func=cmd_list)
    s_check = sub.add_parser("check", help="Check adb availability")
    s_check.set_defaults(func=cmd_check)
    s_run = sub.add_parser("run", help="Run arbitrary adb args (pass after --)")
    s_run.add_argument("--device", "-s", help="Device serial (optional)", default=None)
    s_run.add_argument("command", nargs=argparse.REMAINDER, help="ADB subcommand (start with adb args after --)")
    s_run.set_defaults(func=cmd_run)

    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
