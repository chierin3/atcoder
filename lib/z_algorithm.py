def z_algorithm(seq):
    n = len(seq)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    i = 1
    j = 0
    while i < n:
        while i + j < n and seq[j] == seq[i + j]:
            j += 1
        z[i] = j
        if j == 0:
            i += 1
        else:
            k = 1
            while k < j and k + z[k] < j:
                z[i + k] = z[k]
                k += 1
            i += k
            j -= k
    return z

N = int(input())
S = input()
ans = 0
for i in range(N - 1):
    Z = z_algorithm(S[i:])
    for j in range(1, len(Z)):
        ans = max(ans, min(Z[j], j))
print(ans)