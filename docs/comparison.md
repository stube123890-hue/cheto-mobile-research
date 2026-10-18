# Three-Way Comparison

## Headline

Three commercial cheat operations. Zero shared code, certs, servers, or brands.
Same playbook — arrived at independently, because it's what works against Miniclip.

## Method comparison

| | HW Mods | EasyVictory | Snake Engine |
|---|---|---|---|
| **Approach** | External overlay aimbot | In-process injection kit | Virtual-app sandbox |
| **Game binary** | Repacked APK | Modded APK w/ framework | Stock Play APK, untouched |
| **Memory access** | Read-only (`/proc/self/mem`, `process_vm_readv`) | In-process (direct) | Via virtualization layer |
| **Rendering** | Transparent Canvas overlay (external) | ESP Canvas (in-process) | Overlay via framework |
| **Hooking** | None — never touches game code | Inline hooks (`mprotect`+`mmap`) | Framework-level virtualization |
| **Anti-ban** | xhook signature spoof | hideLibrary, path redirect | UID/PM virtualization |
| **Root needed** | No | No | No |

## Efficiency ranking

1. **HW Mods** (lowest overhead) — memory reads + Canvas draw; no injection, no hooks,
   no virtualization layer. Just observation and drawing.
2. **EasyVictory** (medium) — in-process hooks and per-frame JNI draws cost more,
   but buy deeper control (can modify behavior, not just observe).
3. **Snake Engine** (highest) — full process virtualization layer; heaviest, but the
   user never touches APKs.

## Vulnerability ranking (most detectable → least)

1. **Snake Engine** — virtualization is fingerprintable: spoofed PackageManager,
   nonstandard UIDs, static stub package names. Anti-cheat vendors specifically
   hunt virtual-app frameworks.
2. **EasyVictory** — inline hooks and patched `Instrumentation`/`AppComponentFactory`
   are exactly what integrity checks look for.
3. **HW Mods** — read-only memory access leaves almost no forensic footprint; the
   xhook signature spoof covers cert checks. Main exposure is **behavioral**
   (inhuman accuracy) — which no tool can hide.

## Protection ranking (hardest to reverse → easiest)

1. **Snake Engine** — commercial packer: direct syscalls, self-modifying code,
   full string encryption. Ghidra's analyzer hangs on it.
2. **EasyVictory** — 3-layer anti-analysis: string encryption, encrypted init,
   decoy `JNI_OnLoad` in `.bss`.
3. **HW Mods** — XOR string decrypt, control-flow flattening, stripped binary.
   Still the most approachable of the three statically.

Note the irony: the stealthiest cheat (HW Mods) is the easiest to reverse, and the
most detectable (Snake Engine) is the hardest. Stealth and anti-analysis are
different problems.

## Commercial comparison

| | HW Mods | EasyVictory | Snake Engine |
|---|---|---|---|
| Sales | Telegram (@HwMods) | App + resellers | Full reseller hierarchy |
| License | "Lifetime" keys, RSA | Per-game keys | Device-bound keys |
| Kill switch | Remote config | — | Banned-device tracking |
| Markets | — | — | EN/ES/ID/MS/TL (SEA/LATAM/ME) |

## What's common (the playbook)

- Commercial: paid licenses, server validation, resellers — in all three
- 8 Ball Pool as the flagship target — in all three
- Overlay-based visuals — nobody patches game rendering
- Core logic in native code — not Java
- Anti-analysis — string encryption and obfuscation everywhere
- The static-analysis wall — all three need Frida/dynamic analysis to finish
- **Behavioral detection beats them all** — inhuman accuracy is bannable regardless
  of how stealthy the tool is
