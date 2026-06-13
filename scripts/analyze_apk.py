#!/usr/bin/env python3
"""
scripts/analyze_apk.py
Wrapper to run modules/apk_analyzer.analyze_apk(path) and optionally write JSON output.
Usage:
  python scripts/analyze_apk.py app.apk
  python scripts/analyze_apk.py app.apk --out findings.json
"""
import sys
import argparse
import json
sys.path.insert(0, ".")

from modules import apk_analyzer

def main():
    p = argparse.ArgumentParser(prog="analyze_apk")
    p.add_argument("apk", help="Path to APK file")
    p.add_argument("--out", "-o", help="Write JSON results to file")
    args = p.parse_args()

    res = apk_analyzer.analyze_apk(args.apk)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=2)
        print(f"Wrote results to {args.out}")
    else:
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
