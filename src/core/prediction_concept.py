"""
Illustrative concept: 2D vector math used in trajectory prediction.

This demonstrates the *concepts* (vector ops behind aim solving).
It is not connected to any game and cannot function as a cheat.
"""

import math


class Vec2:
    """Minimal 2D vector for concept demonstration."""

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y

    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)

    def scaled(self, s):
        return Vec2(self.x * s, self.y * s)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return Vec2(self.x / l, self.y / l) if l else Vec2()

    def angle(self):
        return math.atan2(self.y, self.x)


def predict_first_collision(cue_pos, aim_angle, balls, ball_radius):
    """
    Concept: walk a ray from the cue ball along aim_angle,
    return the first ball it would hit (if any).

    This is the core idea behind "Scanning Angles" in aimbot
    shot solvers — simplified to one ray, no cushions, no spin.
    Real solvers score many angles and handle bank shots.
    """
    direction = Vec2(math.cos(aim_angle), math.sin(aim_angle))
    best, best_t = None, float("inf")
    for ball in balls:
        rel = ball - cue_pos
        # project ball center onto the ray
        t = rel.x * direction.x + rel.y * direction.y
        if t < 0:
            continue
        closest = cue_pos + direction.scaled(t)
        miss = (ball - closest).length()
        if miss <= ball_radius * 2 and t < best_t:
            best, best_t = ball, t
    return best, best_t


if __name__ == "__main__":
    cue = Vec2(0, 0)
    balls = [Vec2(10, 1), Vec2(10, -3)]
    hit, dist = predict_first_collision(cue, 0.1, balls, 1.0)
    print("first collision:", hit.x, hit.y, "at distance", round(dist, 2))
