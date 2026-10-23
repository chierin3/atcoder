def mod_Gamma(A, Gamma, mod):
    d = len(Gamma) - 1
    while len(A) - 1 >= d:
        n = len(A) - 1
        for i in range(d):
            A[n - d + i] -= A[n] * Gamma[i]
            A[n - d + i] %= mod
        A.pop()
    return A

def convolution(A, B, mod):
    d = len(A) + len(B) - 1
    C = [0] * d
    for i in range(len(A)):
        for j in range(len(B)):
            C[i + j] += A[i] * B[j]
            C[i + j] %= mod
    return C

def modpow(N, Gamma, mod):
    R = [1]
    B = [0, 1]
    while N > 0:
        if N % 2 == 1:
            R = mod_Gamma(convolution(R, B, mod), Gamma, mod)
        B = mod_Gamma(convolution(B, B, mod), Gamma, mod)
        N //= 2
    return R

def Fiduccia(A, Gamma, N, mod):
    R = modpow(N, Gamma, mod)
    ans = 0
    for i in range(len(R)):
        ans += A[i] * R[i]
        ans %= mod
    return ans

# Aは初期値のリスト、Gammaは漸化式の係数、Nは求めたい項数、modは剰余
# Gammaは[-a_{d-1}, -a_{d-2}, ..., -a_0, 1]の形で与える
# 0-indexedで考えると、A[i]はi番目の項の値を表す
K, N = map(int,input().split())
A = [1] * K
mod = 10**9 + 7
Gamma = [-1] * (K + 1)
Gamma[K] = 1
ans = Fiduccia(A, Gamma, N - 1, mod)
print(ans)