from scipy.spatial import Delaunay
import numpy as np

class DelaunayGraph:
    def __init__(self, positions):
        self.positions = positions
        self.node_count = len(positions)
        self.G = [[False] * (self.node_count) for _ in range(self.node_count)]
        self.create()

    def create(self):
        np_positions = np.array(self.positions)
        tri = Delaunay(np_positions)
        triangles = tri.simplices
        for triangle in triangles:
            u, v, w = triangle
            self.G[u][v] = True
            self.G[u][w] = True
            self.G[v][u] = True
            self.G[v][w] = True
            self.G[w][u] = True
            self.G[w][v] = True

    def get_common_points(self, arg:list[int]):
        points = []
        for i in range(self.node_count):
            for a in arg:
                if self.G[i][a] == -1:
                    break
            else:
                points.append(i)
        return points

# 入力読み込み
N = int(input())
pst = []
for i in range(N):
    x, y = map(int, input().split())
    pst.append((x, y))

DG = DelaunayGraph(pst)