class Node:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None

class KD_Tree:
    def __init__(self, points):
        self.points = points
        self.k = len(points[0]) if points else 0
        self.root = self.build_tree(points, depth=0)

    def build_tree(self, points, depth):
        if not points:
            return None

        axis = depth % self.k
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        node = Node(points[median])
        node.left = self.build_tree(points[:median], depth + 1)
        node.right = self.build_tree(points[median + 1:], depth + 1)
        return node

N,K = map(int, input().split())
points = []
for _ in range(N):
    x, y = map(int, input().split())
    points.append((x, y))
kd_tree = KD_Tree(points)
ans = []
for i in range(N):
    pass