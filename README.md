# 8BP Cheto — Mobile Methodology Research

An educational teardown of how mobile 8 Ball Pool cheats work. This repo documents the
**methodology** behind modern Android aimbots — the architecture, the techniques, and how
three independent commercial operations converged on the same playbook.

This is **research, not a cheat**. There is no working cheat code here — only concepts,
architecture, and illustrative snippets so the community can understand the techniques.

## The core doctrine

Every major operation implements one idea, inherited from the 2022 open-source PC cheat
[8-Ball-Pool-Cheto](https://github.com/xpboosting/8-Ball-Pool-Cheto):

> **Never patch the game. Observe it from outside, solve the shot, draw the answer.**

## The three operations

| | HW Mods (@HwMods) | EasyVictory | Snake Engine |
|---|---|---|---|
| Method | External memory-read + overlay | In-process injection | Virtual-app sandbox |
| Stealth | Highest | Medium | Lowest |
| Overhead | Lowest | Medium | Highest |
| Needs | Repacked game APK | Injection into game process | Nothing — runs stock APKs |

Each operation gets a detailed method breakdown:

- **[docs/hw-mods.md](docs/hw-mods.md)** — the external aimbot: memory scrape, trajectory solver, overlay
- **[docs/easyvictory.md](docs/easyvictory.md)** — the injection kit: hooks, path redirect, ESP
- **[docs/snake-engine.md](docs/snake-engine.md)** — the virtualization container
- **[docs/comparison.md](docs/comparison.md)** — side-by-side: efficiency, vulnerability, detection surface
- **[docs/lineage.md](docs/lineage.md)** — from 2022 PC Cheto to the modern mobile scene
- **[docs/methodology.md](docs/methodology.md)** — the shared techniques in depth

## Repo layout

```
docs/   — detailed writeups (start here)
src/
  core/    — illustrative prediction/vector concepts
  memory/  — illustrative memory-observation patterns
  overlay/ — illustrative overlay-rendering patterns
```

Everything in `src/` is illustrative — it demonstrates concepts, it doesn't compile
into anything usable. That's deliberate.

## Why this exists

Cheat methodology is security research. Understanding how aimbots observe memory, how
overlays evade rendering hooks, and how signature spoofing defeats cert checks is useful
for anti-cheat engineers, Android security researchers, and curious developers.

## Disclaimer

8 Ball Pool is a live online game. Aimbots ruin matches and get accounts banned —
Miniclip bans behaviorally, and inhuman accuracy is detectable no matter how stealthy
the tool. This repo is for understanding, not for cheating.
