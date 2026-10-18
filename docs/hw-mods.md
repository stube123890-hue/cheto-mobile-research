# HW Mods — Detailed Method Breakdown

**Operation:** HACKER WORLD / HW MODS (Telegram @HwMods)
**Target:** 8 Ball Pool 56.32.0, repacked as `com.miniclip.eightballpool` (stock package name kept)
**Signature:** AOSP debug key — not Miniclip's
**Method:** External memory-read aimbot + transparent overlay. No root required.

## 1. Injection chain (repack-time, not runtime)

No Frida, no substrate — everything is baked in when the APK is repacked:

1. **App start** — the stock `EightBallPoolApplication` extends `MultiDexApplication`,
   which the modder patched to extend `bin.mt.signature.KillerApplication`
   (open-source ApkSignatureKillerEx) instead of `android.app.Application`.
2. **`KillerApplication.attachBaseContext`** runs first — loads `libSignatureKiller.so`,
   which uses **xhook** to intercept native `open()` and `PackageManager` signature
   queries. When the game or its anti-cheat asks "what is my signing cert?", it gets
   Miniclip's *original* signature back instead of the debug key. This is the anti-ban.
3. **`MenuRuntime.initialize()`** — loads `libHwMods.so` via `JNI_OnLoad`, starts the mod
   engine threads, registers activity lifecycle callbacks.
4. **`com.hackerworld.mods.Menu` Service** — draws the floating mod menu overlay via
   `WindowManager` (`SYSTEM_ALERT_WINDOW` permission). Full custom widget framework:
   buttons, checkboxes, spinners, color pickers, collapsible sections.

## 2. Memory observation (the aimbot's eyes)

**Function:** `FUN_001ebaa8` @ `0x1ebaa8` (in `libHwMods.so`)

- Tries `dl_iterate_phdr` first to enumerate loaded modules
- Falls back to parsing `/proc/self/maps` with `sscanf("%llx-%llx %4s %llx")`
- Filters readable regions, basename-matches **`libloader.so`**, returns its base address
- This resolves the ASLR slide so hardcoded struct offsets land correctly

**Function:** `FUN_001ec9a8` @ `0x1ec9a8` (control-flow flattened)

Dual read primitives, both read-only:
- `open("/proc/self/mem", O_LARGEFILE)` + `pread(fd, buf, 0x20, offset)` — 32-byte reads
- `process_vm_readv` (syscall 270) on its own PID — second primitive

Every read is validated with `memcmp` against hardcoded byte signatures; `close(fd)` on
all paths. This is signature-verified, read-only capture — the game is never written to.

## 3. Trajectory solver (the aimbot's brain)

**Function:** `FUN_001cf184` @ `0x1cf184` — the shot state machine

- Menu command IDs `0x16`–`0x23` drive the cycle
- Aim cycle: `"Scanning Angles"` → per-angle scoring via `FUN_0026b084` →
  `"Firing"`/`"Aiming"` → clock timeout → `"No Shot Found"`
- Includes **bank/cushion shot solving** (`"Searching Bank Shot..."`, `"Cushion Shot"` toggle)

**Function:** `FUN_001d6564` — the actual solver (22KB, defeats Ghidra's decompiler — flattened)

Recovered physics tunables:
- `math_params.radius_mult` — ball radius multiplier
- `math_params.cushion_damping` — cushion energy loss
- `math_params.friction` — table friction
- `math_params.scale` — coordinate scaling

Math primitives used: `atan2`, `sincos`, `asin`. The exact solver algorithm needs
dynamic analysis (Frida) — static analysis hit the flattening wall.

**Table calibration** (per-device alignment): the menu exposes Table Size, Position Y,
Width Stretch, Scale Zoom, Speed Scale, Camera FOV — these align the overlay prediction
with the actual rendered table across resolutions.

## 4. Overlay rendering (the aimbot's hands)

- `"Waiting for host GL prediction frame"` (`FUN_001d36c4` — also reads `/proc/self/mem`)
- `"Canvas prediction frame submitted"` — drawn on a **transparent WindowManager canvas**
- `nativePredictionFrame` + `nativeUsesCanvas` bridge the native solver to the overlay
- The extended guideline appears over the game; the game itself is untouched

## 5. Spin control

Same memory pipeline: `"Adjusting Spin..."` → `"Applying Spin..."` → `"Spin Busy"`.
Spin stored as a 2D vector. Degrades gracefully (`"native spin control unavailable"`)
when the spin state can't be resolved.

## 6. Autoplay bot

`nativeAutoplayTick()` — one of only 6 JNI natives registered. Tick-driven: called on
the game loop, reads table state, computes and executes shots automatically. Mode flag
with values 0–3.

## 7. License system (commercial operation)

- `CrmAuth.exchange()` — network license check with deadline/timeout
- `nativeCheckKey`, `isKeyAuthenticated()`, `getExpiryDate()`, `"Lifetime"` tier
- RSA-encrypted license traffic
- `nativeFetchRemoteConfig()`, `nativeGetNotice()`, `nativeIsMaintenance()` —
  **server-side remote config and kill switch**: the operator can push notices, change
  features, or disable the mod entirely

## 8. Self-protection

- `libHackerWorldProtection.so` — `"Protected By @GoToHellxD"`: anti-tamper/anti-debug
  for the mod's own libraries
- VPN/proxy detection (`"VPN / Proxy Detected! Disable to proceed."`) — blocks traffic
  sniffing of the license protocol
- `com.hackerworld.encryption.LundLele` — string/config encryption
- Runtime XOR string decryption in `JNI_OnLoad`, control-flow flattening with
  XOR-mutated state transitions, fully stripped binary (2,103 functions, 1 export)

## 9. What it does NOT do

- No unlimited coins/cash (server-side anyway)
- No cue/table unlocks
- No DEX gameplay patches — the 20 DEX files' game classes are stock
- No root required

## Detection surface

| Vector | Status |
|---|---|
| Signature check | Spoofed via xhook (ApkSignatureKillerEx) |
| Memory integrity | Read-only — nothing to detect |
| Overlay | Transparent canvas — visible to overlay detectors |
| Behavior | **Exposed** — inhuman accuracy is bannable |
| Debug cert | Covered by the spoof unless probed deeply |
