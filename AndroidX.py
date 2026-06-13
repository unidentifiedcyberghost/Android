@@
 def build_parser() -> argparse.ArgumentParser:
@@
     p.add_argument("--interactive", "-i",  action="store_true",    help="Launch interactive menu mode")
     p.add_argument("--version",     "-v",  action="store_true",    help="Show version")
+    p.add_argument("--no-banner",            action="store_true",    help="Disable animated ASCII banner")
+    p.add_argument("--no-glitch",            action="store_true",    help="Disable per-header glitch animations")
@@
 def main():
     parser = build_parser()
@@
     args = parser.parse_args()
+
+    # Apply runtime flags to UI toggles
+    if getattr(args, "no_banner", False):
+        globals()["NO_BANNER"] = True
+    if getattr(args, "no_glitch", False):
+        globals()["GLITCH_ENABLED"] = False
@@
     if __name__ == "__main__":
     try:
         main()
     except KeyboardInterrupt:
         console.print("\n\n[bold bright_cyan]👻 AndroidX interrupted. Stay ethical.[/]\n")
         sys.exit(0)
