import math

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def midpoint(self, other):
        return Point2D((self.x + other.x) / 2, (self.y + other.y) / 2)

    def __str__(self):
        return f"({self.x}, {self.y})"

# --- ทดสอบ ---
p1 = Point2D(0, 0)
p2 = Point2D(3, 4)
print(f"จุด p1 = {p1}")
print(f"จุด p2 = {p2}")
print(f"ระยะห่าง = {p1.distance(p2):.2f}")
print(f"จุดกึ่งกลาง = {p1.midpoint(p2)}")
