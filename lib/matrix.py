
# N * N行列AとBの積を計算する関数
def multiply(A, B, mod):
    N = len(A)
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        for k in range(N):
            if A[i][k] == 0:
                continue
            aik = A[i][k]
            for j in range(N):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C

# N * N行列Aをn乗する関数
def power_matrix(A, n, mod):
    N = len(A)
    result = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    while n > 0:
        if n % 2 == 1:
            result = multiply(result, A, mod)
        A = multiply(A, A, mod)
        n //= 2
    return result

N, K = map(int, input().split())
mod = 10**9 + 7
A = []
for _ in range(N):
    row = list(map(int, input().split()))
    A.append(row)
A_powered = power_matrix(A, K, mod)
ans = 0
for i in range(N):
    for j in range(N):
        ans = (ans + A_powered[i][j]) % mod
print(ans)