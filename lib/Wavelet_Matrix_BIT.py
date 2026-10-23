import bisect

class BIT:
    # 長さN+1の配列を初期化
    def __init__(self, N):
        self.size = N
        self.bit = [0]*(N+1)

    # i番目までの和を求める
    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i] # フェニック木のi番目の値を加算
            i -= -i & i # 最も右にある1の桁を0にする
        return res

    # i番目の値にxを足して更新する
    def add(self, i, x):
        while i <= self.size:
            self.bit[i] += x # フェニック木のi番目にxを足して更新
            i += -i & i # 最も右にある1の桁に1を足す

class Wavelet_Matrix:
    def __init__(self, data:list[int], weight:list[int]):
        self.N = len(data)
        self.max_value = max(data)
        self.H = self.max_value.bit_length()
        self.matrix = [[0] * (self.N + 1) for _ in range(self.H)]
        self.total = [BIT(self.N) for _ in range(self.H + 1)]
        for h in range(self.H - 1, -1, -1):
            dir = []
            left = []
            left_weight = []
            right = []
            right_weight = []
            for i in range(self.N):
                self.total[h + 1].add(i + 1, weight[i])
            for i in range(self.N):
                dir.append((data[i] >> h) & 1)
                if dir[i] == 0:
                    left.append(data[i])
                    left_weight.append(weight[i])
                else:
                    right.append(data[i])
                    right_weight.append(weight[i])
            a = len(left)
            b = len(right)
            for i in range(a):
                data[i] = left[i]
                weight[i] = left_weight[i]
            for i in range(b):
                data[a + i] = right[i]
                weight[a + i] = right_weight[i]
            for i in range(self.N):
                self.matrix[h][i + 1] = self.matrix[h][i] + dir[i]
        for i in range(self.N):
            self.total[0].add(i + 1, weight[i])

    # (h, l, r) の子の範囲を返す
    # 左の子の範囲は [l0, r0), 右の子の範囲は [l1, r1)
    def get_subtree_range(self, h, l, r):
        l1 = self.matrix[h][l]
        l0 = l - l1
        r1 = self.matrix[h][r]
        r0 = r - r1
        c0 = self.N - self.matrix[h][self.N]
        return l0, r0, c0 + l1, c0 + r1

    # l, r: [l, r) の範囲で k 番目に小さい値を返す
    # k は 0-indexed
    def kth_smallest_rec(self, l, r, k):
        ans = 0
        for h in range(self.H, 0, -1):
            l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
            left_count = r0 - l0
            if k < left_count:
                l = l0
                r = r0
            else:
                ans += (1 << (h - 1))
                l = l1
                r = r1
                k -= left_count
        return ans

    # l, r: [l, r) の範囲で k 番目に大きい値を返す
    # k は 0-indexed    
    def kth_biggest_rec(self, l, r, k):
        ans = 0
        for h in range(self.H, 0, -1):
            l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
            right_count = r1 - l1
            if k < right_count:
                ans += (1 << (h - 1))
                l = l1
                r = r1
            else:
                l = l0
                r = r0
                k -= right_count
        return ans
    
    # l, r: [l, r) の範囲の値の合計を返す
    # 値の範囲は [0, a) である   
    def subtree_sum(self, l, r, a):
        if a > self.max_value:
            return self.total[self.H].sum(r) - self.total[self.H].sum(l)
        ans = 0
        for h in range(self.H, 0, -1):
            l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
            if (a >> (h - 1)) & 1:
                ans += self.total[h - 1].sum(r0) - self.total[h - 1].sum(l0)
                l = l1
                r = r1
            else:
                l = l0
                r = r0
        return ans
    
    # l, r: [l, r) の範囲の値の合計を返す
    # 値の範囲は [a, b) である
    def subtree_sum_rec(self, l, r, a, b):
        ans = 0
        ans += self.subtree_sum(l, r, b)
        ans -= self.subtree_sum(l, r, a)
        return ans
    
    def add_weight(self, idx, delta):
        for h in range(self.H, 0, -1):
            self.total[h].add(idx + 1, delta)
            rank1 = self.matrix[h - 1][idx]
            rank0 = idx - rank1
            bit = self.matrix[h - 1][idx + 1] - self.matrix[h - 1][idx]
            if bit:
                idx = rank1 + (self.N - self.matrix[h - 1][self.N])
            else:
                idx = rank0
        self.total[0].add(idx + 1, delta)

N, Q = map(int,input().split())
P = []
for i in range(N):
    x, y, w = map(int,input().split())
    P.append((x, y, w, i))
queries = []
for i in range(Q):
    query = list(map(int,input().split()))
    queries.append(query)
    if query[0] == 0:
        P.append((query[1], query[2], query[3], N + i))
P.sort()
X = [x for x, y, w, i in P]
Y = [y for x, y, w, i in P]
W = [w if i < N else 0 for x, y, w, i in P]
I = {i:idx for idx, (x, y, w, i) in enumerate(P)}
wm = Wavelet_Matrix(Y, W)
for q in range(Q):
    query = queries[q]
    if query[0] == 0:
        idx = I[N + q]
        wm.add_weight(idx, query[3])
    else:
        x1, y1, x2, y2 = query[1], query[2], query[3], query[4]
        l = bisect.bisect_left(X, x1)
        r = bisect.bisect_left(X, x2)
        ans = wm.subtree_sum_rec(l, r, y1, y2)
        print(ans)