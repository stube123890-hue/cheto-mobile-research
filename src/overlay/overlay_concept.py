"""
Illustrative concept: overlay rendering pattern.

Real aimbots draw predicted guidelines on a transparent overlay window
positioned above the game (Android WindowManager overlay, or Direct2D
on PC). This file demonstrates ONLY the *drawing math* — projecting a
predicted path onto a 2D canvas — with no window, no overlay, and no
game involved. Output is ASCII art.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.prediction_concept import Vec2, predict_first_collision
import math


def render_ascii_path(cue, aim_angle, balls, ball_radius, width=40, height=12):
    """Draw a predicted shot path as ASCII art. Concept only."""
    grid = [["." for _ in range(width)] for _ in range(height)]

    def plot(p, ch):
        x, y = int(p.x), int(p.y)
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = ch

    plot(cue, "C")
    for b in balls:
        plot(b, "O")

    direction = Vec2(math.cos(aim_angle), math.sin(aim_angle))
    hit, dist = predict_first_collision(cue, aim_angle, balls, ball_radius)
    steps = int(dist) if hit else width
    for i in range(1, steps):
        plot(cue + direction.scaled(i), "-")
    if hit:
        plot(hit, "X")

    return "\n".join("".join(row) for row in grid)


if __name__ == "__main__":
    cue = Vec2(2, 6)
    balls = [Vec2(20, 7), Vec2(30, 3)]
    print(render_ascii_path(cue, 0.05, balls, 1.0))
    print("\nC=cue ball  O=balls  -=predicted path  X=predicted hit")
