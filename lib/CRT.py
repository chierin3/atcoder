# 中国剩余定理（Chinese Remainder Theorem, CRT）
# a[i] ≡ x (mod m[i]) の連立合同式を解く
def CRT(a:list[int], m:list[int]):
    M = 1
    for i in m:
        M *= i
    x = 0
    for i in range(len(a)):
        Mi = M // m[i]
        inv = pow(Mi, -1, m[i])
        x += a[i] * Mi * inv
        x %= M
    return x

# 別解
def CRT2(a:list[int], m:list[int]):
    M = 1
    x = 0
    for i in range(len(a)):
        y = pow(M, -1, m[i])
        c = (a[i] - x) * y % m[i]
        x += M * c
        M *= m[i]
    return x

def CRT3(a:list[int], m:list[int]):
    c = []
    for i in range(len(a)):
        x = 0
        M = 1
        for j in range(i):
            x = (x + c[j] * M) % m[i]
            M = (M * m[j]) % m[i]
        y = pow(M, -1, m[i])
        c.append((a[i] - x) * y % m[i])
    x = 0
    for i in range(len(a) - 1, -1, -1):
        x *= m[i]
        x += c[i]
    return x

A, B, a, b = map(int, input().split())
print(CRT([a, b], [A, B]))