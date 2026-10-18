# Lineage — From 2022 PC Cheto to the Mobile Scene

## The fossil record

[8-Ball-Pool-Cheto](https://github.com/xpboosting/8-Ball-Pool-Cheto) (xpboosting, 2022,
archived 2023) is a Windows PC cheat for 8 Ball Pool 5.8.x. Its architecture:

- **External** process memory reading (`Memory.cpp` — read/write primitives)
- **Trajectory prediction** (`Prediction.cpp` — collision detection, velocity,
  cushion shots; `Ball.cpp`, `TableInfo.cpp` for game state)
- **Overlay rendering** (Direct2D overlay + ImGui menu)
- **Hardcoded offsets** (`Offsets.h` — `SharedUserInfo`, `SharedGameManager`, …)

The README says it plainly: *"Source need to be fixed but it has updated offsets."*
Game updates break hardcoded offsets — the eternal curse of memory cheats.

## The doctrine

```
Never patch the game.
Observe it from outside (memory reads),
solve the shot (trajectory + cushions),
draw the answer (overlay).
```

This is the architecture every mobile operation inherited.

## HW Mods — the direct port

HW Mods is this cheat translated to Android, nearly 1:1:

| PC Cheto (2022) | HW Mods (2024–26) |
|---|---|
| `ReadProcessMemory` | `/proc/self/mem` + `process_vm_readv` |
| Hardcoded offsets | Signature scanning (`memcmp` byte patterns) |
| D2DOverlay | Transparent Canvas overlay |
| `Prediction.cpp` collision solver | `FUN_001d6564` trajectory solver |
| Bank-shot support | `"Searching Bank Shot..."` |

And it **evolved past** the original: signature scanning instead of hardcoded offsets
means game updates don't break it the way they broke Cheto.

## EasyVictory — the naming lineage

EasyVictory's code contains `com.easyvictory.cheto/platform_channel`. "Cheto" isn't
a coincidence — it's a naming lineage. Whoever built EasyVictory came from this PC
cheat scene. Different architecture (in-process injection instead of external
observation), same roots.

## Snake Engine — the breakaway

Snake Engine abandoned the doctrine entirely: instead of observing the game
externally, it virtualizes the whole process. The only operation of the three that
doesn't descend from the PC Cheto architecture.

## The family tree

```
2022: xpboosting/8-Ball-Pool-Cheto (PC, open source, archived 2023)
  │
  ├─ HW Mods ─────── direct Android port, evolved (signature scanning)
  │
  ├─ EasyVictory ─── naming lineage ("cheto" channel), new architecture (injection)
  │
  └─ Snake Engine ── breakaway (virtualization, no shared doctrine)
```

A 2022 open-source PC cheat is the fossil record for a multi-operation mobile cheat
industry. The methodology outlived the repo.
