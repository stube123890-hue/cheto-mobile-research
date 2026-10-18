# EasyVictory — Detailed Method Breakdown

**Operation:** EasyVictory (t.me/easyvictorybox, discord.gg/easyvictory)
**App:** EV_Loader 1.2.3 — Flutter app (`com.miniclip.battlerivals`, fake Miniclip cert)
**Method:** Cheat platform — mod store (Dart UI) + in-process injection framework
**Sister app:** `com.easyai.easyai` ("buy via our EasyAI app")
**Supported games:** 8 Ball Pool, Carrom, + 1 encrypted title

## 1. Architecture (two halves)

**Half 1 — Mod store (Dart/Flutter):**
- Accounts, per-game license keys ("Bind Game to Key"), premium tiers
- Reseller program (`storage.easyvictory.me` backend)
- Mod catalog downloads, APK installs via `PackageInstaller` (`InstallResultReceiver`)

**Half 2 — Injection framework (`com.easyvictory.loader.*` in DEX):**
- Designed to run *inside* the target game's process
- `libcxx_evrt.so` (3MB) — the native injection runtime ("evrt" = EasyVictory Runtime)

## 2. Process entry

evrt doesn't inject at runtime — it's a library *of the modded APK*:

1. `Plugin.initialize()` (Java, runs in-game) does `System.loadLibrary("cxx_evrt")`
2. **Before** loading, it patches `AppComponentFactory` and injects a custom
   `Instrumentation` via reflection — this is how it gets its code running inside
   the game's process
3. All JNI methods bind through dynamic `registerNatives` — the `.so` exports only
   **one symbol**, hiding the entire native API surface

## 3. APK/OBB path redirection

`initialize()` builds redirect paths from token-gated config:
- `baseAPKRedirectPath`
- `splitConfigArm64RedirectPath`
- `mainOBBRedirectPath`

Then rewrites the game's `ApplicationInfo` paths so Android loads **modded APK/OBB
content** instead of the originals. The game runs normally but serves attacker
content.

## 4. hideLibrary (anti-detection)

**Function:** `FUN_0016d000` @ `0x16d000` — hand-rolled `/proc/self/maps` parser

- Opens `/proc/self/maps`, parses each line, builds a linked list of loaded ELF modules
- Checks `\x7fELF` magic, skips `/linker`
- **Function:** `FUN_0016c9ac` @ `0x16c9ac` — prefers `dl_iterate_phdr`, falls back to the
  maps parser, then walks each module's ELF program headers to compute load bias
- Ships its own dlmalloc-style allocator (doesn't trust the host's)

The final hide step (linker-list unlink vs maps scrubbing) lives in the encrypted
region — infrastructure proven, exact technique needs dynamic analysis.

## 5. ESP overlay

- `onDrawImplJNI(Canvas)` bound via `registerNatives`
- Java side: type-1002 full-screen `WindowManager` view, `FloatLogo`,
  `executeGLThreadJob` for GL-thread synchronization
- Per-frame Canvas draws from *inside* the game process (unlike HW Mods' external canvas)
- Native draw body is in the protected region

## 6. Method hooking

- Java `Hooker` / `HookCallback` — reflection-level dispatch
- Native side has the classic inline-hook engine footprint:
  `mprotect` + `mmap` + `dlopen`/`dlsym` + custom ELF/load-bias resolution
- Trampoline writer is encrypted — strongly indicated, not conclusively proven
- **No xhook** — different hooking approach from HW Mods

## 7. Per-game switching

`EnumC0486d.e(packageName)` — early-returns on unknown games; per-game branches select
ESP behavior, autoplay, and path redirection. 8 Ball Pool confirmed via hashCode match;
Carrom confirmed; third title encrypted in the string table.

## 8. Anti-analysis (3 layers, commercial-packer grade)

1. **String encryption** — 28k strings, only `/proc/self/maps` + `bFHooK` in plaintext
2. **Encrypted `.init_array`** — high-entropy constructor bytes
3. **Decoy `JNI_OnLoad`** — the exported `JNI_OnLoad` (0x31a000) points into `.bss.3`
   *uninitialized* memory; real code decrypts at runtime

## 9. The "cheto" lineage

The code contains a `com.easyvictory.cheto/platform_channel`. "Cheto" is the name of
the 2022 open-source PC cheat (xpboosting/8-Ball-Pool-Cheto) — this is a naming
lineage, not shared code. Whoever built EasyVictory came from that PC cheat scene.
See [lineage.md](lineage.md).

## Detection surface

| Vector | Status |
|---|---|
| In-process hooks | **Exposed** — inline hooks are what anti-cheat scans for |
| Instrument./AppComponentFactory patch | Detectable via framework integrity checks |
| Path redirection | Detectable via ApplicationInfo validation |
| ESP overlay | Type-1002 window — visible to overlay detectors |
| String encryption | Slows analysis, not detection |
| Behavior | **Exposed** — same as all aimbots |
