@@
-    p.add_argument("--no-banner",            action="store_true",    help="Disable animated ASCII banner")
-    p.add_argument("--no-glitch",            action="store_true",    help="Disable per-header glitch animations")
+    p.add_argument("--no-banner",            action="store_true",    help="Disable animated ASCII banner")
+    p.add_argument("--no-glitch",            action="store_true",    help="Disable per-header glitch animations")
+    p.add_argument("--glitch-frames",        type=int, default=None,   help="Override default glitch frame count (int)")
+    p.add_argument("--glitch-intensity",     type=float, default=None, help="Override default header glitch intensity (0.0-1.0)")
+    p.add_argument("--glitch-pause",         type=float, default=None, help="Override pause between glitch frames (seconds)")
@@
-    # Apply runtime flags to UI toggles
-    if getattr(args, "no_banner", False):
-        globals()["NO_BANNER"] = True
-    if getattr(args, "no_glitch", False):
-        globals()["GLITCH_ENABLED"] = False
+    # Apply runtime flags to UI toggles
+    if getattr(args, "no_banner", False):
+        globals()["NO_BANNER"] = True
+    if getattr(args, "no_glitch", False):
+        globals()["GLITCH_ENABLED"] = False
+
+    # Apply optional glitch overrides if provided
+    if args.glitch_frames is not None:
+        globals()["_DEFAULT_GLITCH_FRAMES"] = int(args.glitch_frames)
+    if args.glitch_intensity is not None:
+        globals()["_DEFAULT_GLITCH_INTENSITY"] = float(args.glitch_intensity)
+    if args.glitch_pause is not None:
+        globals()["_DEFAULT_GLITCH_PAUSE"] = float(args.glitch_pause)
@@
-    if not GLITCH_ENABLED:
-        console.print(Align.center(text))
-        return
+    if not GLITCH_ENABLED:
+        console.print(Align.center(text))
+        return
@@
-    for _ in range(frames):
+    for _ in range(frames):
         for line in lines:
             glitched = []
@@
     for line in lines:
         console.print(Align.center(f"[bold cyan]{line}[/]"))
+
@@
 def animate_glitch_banner():
@@
-    frames = 8 if OS_NAME.startswith("Windows") else 12
-    pause = 0.08 if OS_NAME.startswith("Windows") else 0.05
+    frames = _DEFAULT_GLITCH_FRAMES if OS_NAME.startswith("Windows") else _DEFAULT_GLITCH_FRAMES
+    pause = _DEFAULT_GLITCH_PAUSE if OS_NAME.startswith("Windows") else _DEFAULT_GLITCH_PAUSE
@@
-    chars = "01$#!@%^&*()_+=-[]{}|;:,.<>?/"
+    chars = "01$#!@%^&*()_+=-[]{}|;:,.<>?/"
