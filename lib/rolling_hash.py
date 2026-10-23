import random

hash_map = dict()
mod = (1 << 61) - 1
base = 31
for i in range(2):
    hash_map[str(i)] = random.randint(1, mod)

# 文字列sの長さがnのとき、s[:1]からs[:n]までのハッシュ値を求める
def get_rolling_hash(s):
    hashs = []
    hash_value = 0
    n = len(s)
    for j in range(n):
        hash_value = (hash_value * base + hash_map[s[j]]) % mod
        hashs.append(hash_value)
    return hashs

T = int(input())
for _ in range(T):
    A = input()
    B = input()
    N = len(A)
    ha = get_rolling_hash(A)[-1]
    hb = get_rolling_hash(B)[-1]
    T = pow(base, N, mod)
    for i in range(N):
        if ha == hb:
            print(i)
            break
        # 一致しない場合、Aを1文字左に回転
        ha = (ha * base - hash_map[A[i]] * T + hash_map[A[i]]) % mod
    else:
        print(-1)
