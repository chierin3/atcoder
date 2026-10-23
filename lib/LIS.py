import bisect

# 入力を受け取る
N = int(input())  # 配列の長さ
A = list(map(int, input().split()))  # 配列A

# LIS（最長増加部分列）を求めるための配列を初期化
LIS = [10**10] * N  # 左からのLISを計算するための補助配列
L = [0] * N  # 各位置でのLISの長さを記録する配列
LIS_R = [10**10] * N  # 右からのLISを計算するための補助配列
R = [0] * N  # 各位置での右からのLISの長さを記録する配列

# 左からのLISを計算
for i in range(N):
    idx = bisect.bisect_left(LIS, A[i])  # A[i]を挿入できる位置を二分探索で見つける
    LIS[idx] = A[i]  # LIS配列を更新
    L[i] = idx + 1  # 現在の位置でのLISの長さを記録

# 右からのLISを計算
for i in range(N - 1, -1, -1):  # 逆順に処理
    idx = bisect.bisect_left(LIS_R, A[i])  # A[i]を挿入できる位置を二分探索で見つける
    LIS_R[idx] = A[i]  # LIS_R配列を更新
    R[i] = idx + 1  # 現在の位置での右からのLISの長さを記録

# 最長ビットニク列（山型列）の長さを計算
ans = 0
for i in range(N):
    # 左からのLISと右からのLISを組み合わせて山型列を作る
    ans = max(ans, L[i] + R[i] - 1)  # 重複部分を1引く

# 結果を出力
print(ans)