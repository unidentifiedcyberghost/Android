"""
DroidHunter — APK Static Analyzer Module
Author: HexSecTeam | Instagram: @hexsecteam
"""

import zipfile
import os
import re
import hashlib
import struct
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# ─── Dangerous Android Permissions ────────────────────────────────────────────
DANGEROUS_PERMS = {
    "android.permission.READ_CONTACTS":          "HIGH",
    "android.permission.WRITE_CONTACTS":         "HIGH",
    "android.permission.READ_SMS":               "HIGH",
    "android.permission.SEND_SMS":               "HIGH",
    "android.permission.RECEIVE_SMS":            "HIGH",
    "android.permission.READ_CALL_LOG":          "HIGH",
    "android.permission.WRITE_CALL_LOG":         "HIGH",
    "android.permission.RECORD_AUDIO":           "HIGH",
    "android.permission.CAMERA":                 "MEDIUM",
    "android.permission.ACCESS_FINE_LOCATION":   "HIGH",
    "android.permission.ACCESS_COARSE_LOCATION": "MEDIUM",
    "android.permission.READ_EXTERNAL_STORAGE":  "MEDIUM",
    "android.permission.WRITE_EXTERNAL_STORAGE": "MEDIUM",
    "android.permission.PROCESS_OUTGOING_CALLS": "HIGH",
    "android.permission.INTERNET":               "LOW",
    "android.permission.CHANGE_WIFI_STATE":      "MEDIUM",
    "android.permission.BLUETOOTH":              "LOW",
    "android.permission.NFC":                    "LOW",
    "android.permission.GET_ACCOUNTS":           "MEDIUM",
    "android.permission.USE_CREDENTIALS":        "HIGH",
    "android.permission.READ_PHONE_STATE":        "HIGH",
    "android.permission.CALL_PHONE":             "HIGH",
    "android.permission.RECEIVE_BOOT_COMPLETED": "MEDIUM",
    "android.permission.SYSTEM_ALERT_WINDOW":    "HIGH",
    "android.permission.INSTALL_PACKAGES":       "CRITICAL",
    "android.permission.DELETE_PACKAGES":        "CRITICAL",
    "android.permission.BIND_DEVICE_ADMIN":      "CRITICAL",
    "android.permission.MOUNT_UNMOUNT_FILESYSTEMS": "HIGH",
    "android.permission.MASTER_CLEAR":           "CRITICAL",
}

# (rest of file unchanged...)

