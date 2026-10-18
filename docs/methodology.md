# Shared Methodology — The Techniques in Depth

The techniques all three operations (and the 2022 PC original) build on.
Concepts only — no working implementations.

## 1. Memory observation

The foundation: read the game's process memory without modifying it.

**PC:** `ReadProcessMemory` on the game process handle, walking pointer chains from
a module base address + hardcoded offsets.

**Android (HW Mods):** open `/proc/self/mem` and `pread()` at computed offsets, or
`process_vm_readv` (syscall 270). ASLR is defeated by parsing `/proc/self/maps`
(or `dl_iterate_phdr`) to find the target library's base address, then applying
struct offsets. Every read validated against known byte signatures.

**Why read-only matters:** writing to game memory is what memory-integrity checks
detect. Pure observation leaves almost no forensic footprint.

**The offset problem:** hardcoded offsets break on every game update (this killed the
2022 PC Cheto — "source need to be fixed but it has updated offsets"). The evolution
is **signature scanning**: scan memory for known byte patterns to locate structures
dynamically instead of trusting fixed addresses.

## 2. Trajectory solving

Given ball positions, cue angle, and table geometry, compute the shot:

1. Model each ball as a circle (2D position + radius)
2. For each candidate aim angle, simulate: cue ball path → first collision →
   post-collision velocities → target ball path → pocket or cushion
3. Score angles by outcome (pocketed ball > cushion contact > nothing)
4. Bank shots: reflect the path across cushion geometry, solve recursively

Physics inputs: ball radius, cushion damping (energy lost per bounce), table
friction, coordinate scale. The math is `atan2`/`sincos`/`asin` territory —
2D rigid-body collision with spin as a 2D vector modifier.

The PC original's `Prediction.cpp` shows the shape: `findFirstCollision`,
`calcVelocity`, `calcVelocityPostCollision`, per-ball `PredictionInfo` with position
history. Every mobile operation reimplements this.

## 3. Overlay rendering

Draw the predicted guideline **above** the game, never inside it:

- **PC:** Direct2D overlay window (transparent, topmost, click-through)
- **Android external (HW Mods):** transparent `Canvas` on a `WindowManager` overlay
  (`SYSTEM_ALERT_WINDOW`)
- **Android in-process (EasyVictory):** type-1002 full-screen view, per-frame JNI draw
  with GL-thread synchronization

Calibration matters: table size, position, zoom, and camera FOV must align the
overlay with the rendered table per device — hence the calibration menus.

## 4. Anti-detection

**Signature spoofing (HW Mods):** patch the app's base class to a signature-killer,
use xhook to intercept cert queries, return the original developer's cert. Defeats
cert-pinning checks — but only cert checks.

**Library hiding (EasyVictory):** parse `/proc/self/maps`, walk ELF program headers,
unlink or scrub the cheat library from the loader's view so enumeration doesn't
find it.

**Virtualization stealth (Snake Engine):** the whole game runs inside the cheat's
process — nothing to hide because the game never sees outside. But the
virtualization layer itself is fingerprintable.

**What none of them beat:** behavioral detection. Inhuman shot accuracy, impossible
reaction times, and statistical anomalies are visible server-side no matter how
clean the client looks. This is why commercial cheats still get users banned.

## 5. Commercialization

All three operations are businesses, not hobby projects:

- License keys (lifetime, per-game, or device-bound)
- Server-side validation with RSA-encrypted traffic
- Reseller hierarchies and backends
- Remote config and kill switches (the operator can disable your cheat remotely)
- Banned-device tracking

The cheat is the product; the license server is the business.
