#extend-point-to-vector

import math

# --- Point Class ---
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise ValueError("Argument must be a Point")
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

# --- Vector Class ---
class Vector(Point):
    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise ValueError("Can only add Vector to Vector")
        return Vector(self.x + other.x, self.y + other.y)

# --- Demo Code ---
if __name__ == "__main__":
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print(p1)                             # Point(3, 4)
    print(f"Equal? {p1 == p2}")           # False
    print(f"Distance: {p1.distance_to(p2):.2f}")  # 5.0

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(v1)                             # Vector<1, 2>
    print(v2)                             # Vector<3, 4>

    v3 = v1 + v2
    print(f"v1 + v2 = {v3}")              # Vector<4, 6>

    # Show that Vector still acts like a Point
    print(f"Distance between vectors: {v1.distance_to(v2):.2f}")


