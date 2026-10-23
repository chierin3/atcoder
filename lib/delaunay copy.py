import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1: Point = p1
        self.p2: Point = p2
        self.p3: Point = p3
        self.center: Point = None
        self.radius: float = None
        self.cal_center_coordinate_and_radius()

    def cal_center_coordinate_and_radius(self):
        c = 2 * ((self.p2.x - self.p1.x) * (self.p3.y - self.p1.y) - (self.p3.x - self.p1.x) * (self.p2.y - self.p1.y))
        if c == 0 : return
        cx = ((self.p1.x ** 2 + self.p1.y ** 2) * (self.p2.y - self.p3.y) +
              (self.p2.x ** 2 + self.p2.y ** 2) * (self.p3.y - self.p1.y) +
              (self.p3.x ** 2 + self.p3.y ** 2) * (self.p1.y - self.p2.y)) / c
        cy = ((self.p1.x ** 2 + self.p1.y ** 2) * (self.p3.x - self.p2.x) +
              (self.p2.x ** 2 + self.p2.y ** 2) * (self.p1.x - self.p3.x) +
              (self.p3.x ** 2 + self.p3.y ** 2) * (self.p2.x - self.p1.x)) / c
        self.center = Point(cx, cy)
        self.radius = math.sqrt((self.p1.x - cx) ** 2 + (self.p1.y - cy) ** 2)

    def contains(self, point: Point):
        return (point.x - self.center.x) ** 2 + (point.y - self.center.y) ** 2 <= self.radius ** 2
    
class DelaunayGraph:
    def __init__(self, W, H, positions):
        self.W = W
        self.H = H
        self.positions: list[Point] = positions
        self.triangles: list[Triangle] = []
        self.node_count = len(positions)
        self.G = [[False] * (self.node_count) for _ in range(self.node_count)]
        self.create()

    def create(self):
        # Create a super triangle that encompasses all points
        cx = self.W / 2
        cy = self.H / 2
        r = math.sqrt(self.W ** 2 + self.H ** 2) / 2
        self.triangles.append(Triangle(Point(cx - math.sqrt(3) * r, cy - r),
                                       Point(cx + math.sqrt(3) * r, cy - r),
                                       Point(cx, cy + 2 * r)))
        for i in range(self.node_count):
            p = self.positions[i]
            hit_triangles = []
            new_triangles = []
            for triangle in self.triangles:
                if triangle.contains(p):
                    hit_triangles.append(triangle)
                else:
                    new_triangles.append(triangle)
            triangles = new_triangles
            edges = []
            for triangle in hit_triangles:
                # Find edges of the triangle
                edges.append((triangle.p1, triangle.p2))
                edges.append((triangle.p2, triangle.p3))
                edges.append((triangle.p3, triangle.p1))
                # append the triangle to the graph
                triangles.append(Triangle(triangle.p1, triangle.p2, p))
                triangles.append(Triangle(triangle.p2, triangle.p3, p))
                triangles.append(Triangle(triangle.p3, triangle.p1, p))
            while edges:
                edge = edges.pop()
                if edge in edges:
                    edges.remove(edge)
                    edges.remove((edge[1], edge[0]))
            

            self.triangles = new_triangles
    
P = [Point(0, 0), Point(1, 0), Point(0, 1)]
T = Triangle(P[0], P[1], P[2])
print(f"Center: ({T.center.x}, {T.center.y}), Radius: {T.radius}")
print(f"Contains (0.2, 0.2): {T.contains(Point(0.2, 0.2))}")
print(f"Contains (2, 2): {T.contains(Point(2, 2))}")