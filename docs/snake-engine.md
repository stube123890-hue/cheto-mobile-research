# Snake Engine — Detailed Method Breakdown

**Operation:** Snake Engine (`com.snake` v2.2.6, snakeengine.com)
**Method:** Virtual-app framework — runs target games as plugins inside its own process
**Signature:** Own UAE cert (`CN=SNAKE…`, `L=DUBAI`)
**Commerce:** Most sophisticated distribution — reseller hierarchy, device-bound keys,
  subscriptions, banned-device tracking

## 1. Architecture (virtualization, not injection)

Instead of repacking the game (HW Mods) or injecting into it (EasyVictory), Snake
Engine virtualizes:

1. User installs the **stock game** from Play Store — unmodified
2. Snake Engine runs the game as a plugin *inside its own virtualized process*
3. Proxy stub components (`ProxyActivity`, `ProxyService`, `ProxyProvider`,
   `ProxyReceiver`, `ProxyJobService`, `ProxyVpnService`) stand in for the game's
   real components
4. The real framework hides in 2,804 obfuscated classes stuffed into
   `androidx.appcompat.view.menu.*` (namespace camouflage)
5. Cheat modules are delivered separately — not in this APK

**Why:** no repacking, no root, works with the official game APK. The tradeoff is
overhead and detectability (see below).

## 2. Native core — libengine.so (8.5MB)

Not a game engine, not a cheat engine — the native core of the virtual-app framework:

- Backs `com.snake.helper.Native`'s 11 obfuscated JNI methods
  (`ac`, `aior`, `chl`, `djp`, … — single-purpose names, no semantics)
- Backs the framework's UID/PackageManager virtualization
- Fully stripped: 2,077 functions, exactly **one export: `JNI_OnLoad`**
  (all natives registered dynamically)

## 3. Protection (heaviest of the three operations)

`JNI_OnLoad` (@`0x1f3fa0`) is commercial-packer grade:

- **Direct syscalls** via `SVC #0` — bypasses PLT hooking (can't intercept what
  doesn't go through the PLT)
- **Self-modifying code** — writes ARM64 branch instructions into executable memory
  at runtime (7-iteration patch loop), defeating static control-flow recovery
- **XOR-obfuscated 64-bit data blobs** assembled at runtime
- **Full string-table encryption** — 721 strings recovered, **zero** resolve to any
  function. No `/proc/`, no hook-framework strings, nothing in plaintext.

Ghidra's auto-analyzer **hangs** on this binary (`GccExceptionAnalyzer` infinite-loops
on its exception tables — verified 3×). Workaround: strip `.eh_frame` /
`.gcc_except_table` from a working copy before analysis.

## 4. Storefront — libapp.so (Dart AOT)

The reseller storefront:
- Backend: `rest.snakeseller.com/api/request/`
- Topup: `snakeengine.com/topup`
- Device-bound license keys (`"CODE that will only work for this device id"`)
- **Banned-device tracking** — the server remembers burned devices
- Languages: EN/ES/ID/MS/TL — SEA / LATAM / ME markets
- Game-version gating: the storefront checks the installed game's version before
  serving the matching cheat module

## 5. Commerce model

The most distribution-sophisticated of the three:

```
snakeengine.com (marketing/topup)
  └─ rest.snakeseller.com/api/request/ (reseller API)
       ├─ reseller accounts + hierarchy
       ├─ device-bound license keys
       ├─ subscriptions
       └─ banned-device list
```

Compare: HW Mods sells "Lifetime" keys over Telegram; EasyVictory has a reseller
backend; Snake Engine has the full stack — reseller hierarchy, device binding,
burn tracking.

## Detection surface

| Vector | Status |
|---|---|
| Virtualization | **Highly exposed** — anti-cheat fingerprints virtualization (spoofed PackageManager, nonstandard UIDs, static stub package names like `com.snake.helper.ProxyActivity`) |
| Proxy stubs | Static package names are a signature |
| Native protection | Excellent vs *analysis*, irrelevant vs *detection* |
| Behavior | **Exposed** — same as all aimbots |

Snake Engine trades stealth for convenience: the user never touches APKs, but the
virtualization layer is the most fingerprintable approach of the three.

## Limits of this analysis

The native method bodies and the `RegisterNatives` table are only recoverable via
dynamic analysis (Frida memory dump post-`JNI_OnLoad`) — static analysis hit the
protector wall. The cheat modules themselves are delivered separately and were not
in the analyzed APK.
