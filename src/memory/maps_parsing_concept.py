"""
Illustrative concept: how external memory observation works at a high level.

Real aimbots parse /proc/self/maps to defeat ASLR, then read process
memory at computed offsets. This file demonstrates ONLY the *idea* of
resolving a module base address — using this process's own maps as a
harmless example. It reads nothing belonging to another process and
implements no cheat functionality.
"""

import re


def find_module_base(module_substring):
    """
    Concept: parse /proc/self/maps (this process only) and return the
    lowest mapped address for a module whose path contains the substring.

    Real cheats do this for the *game's* library to defeat ASLR, then
    apply struct offsets. This demo just shows the parsing technique
    on our own process.
    """
    bases = []
    with open("/proc/self/maps") as f:
        for line in f:
            m = re.match(r"([0-9a-f]+)-[0-9a-f]+ \S+ \S+ \S+ \S+\s+(.*)", line)
            if not m:
                continue
            addr, path = m.group(1), m.group(2).strip()
            if module_substring in path:
                bases.append(int(addr, 16))
    return min(bases) if bases else None


if __name__ == "__main__":
    # Harmless demo: find libc in OUR OWN process maps.
    base = find_module_base("libc.so")
    print("own libc base (concept demo):", hex(base) if base else "not found")
