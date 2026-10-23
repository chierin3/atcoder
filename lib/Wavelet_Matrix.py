class Wavelet_Matrix:
    def __init__(self, data:list[int]):
        self.N = len(data)
        self.max_value = max(data)
        self.H = self.max_value.bit_length()
        self.matrix = [[0] * (self.N + 1) for _ in range(self.H)]
        self.total = [[0] * (self.N + 1) for _ in range(self.H + 1)]
        for h in range(self.H - 1, -1, -1):
            dir = []
            left = []
            right = []
            for i in range(self.N):
                self.total[h + 1][i + 1] = self.total[h + 1][i] + data[i]
            for i in range(self.N):
                dir.append((data[i] >> h) & 1)
                if dir[i] == 0:
                    left.append(data[i])
                else:
                    right.append(data[i])
            a = len(left)
            b = len(right)
            for i in range(a):
                data[i] = left[i]
            for i in range(b):
                data[a + i] = right[i]
            for i in range(self.N):
                self.matrix[h][i + 1] = self.matrix[h][i] + dir[i]
        for i in range(self.N):
            self.total[0][i + 1] = self.total[0][i] + data[i]

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
            return self.total[self.H][r] - self.total[self.H][l]
        ans = 0
        for h in range(self.H, 0, -1):
            l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
            if (a >> (h - 1)) & 1:
                ans += self.total[h - 1][r0] - self.total[h - 1][l0]
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

N = int(input())
A = list(map(int, input().split()))
Q = int(input())
wm = Wavelet_Matrix(A)
B = 0
for _ in range(Q):
    a, b, c = map(int, input().split())
    l = a ^ B
    r = b ^ B
    x = c ^ B
    ans = wm.subtree_sum(l - 1, r, x + 1)
    print(ans)
    B = ans
