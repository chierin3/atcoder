# 桁DPのテンプレート
N = list(map(int,input().strip()))
d = len(N)
state_num = 2 * 1024

# Rolling DP 色々試してみたところ一番高速
# 配列を多次元にすると遅くなるので注意
dp = [0] * state_num
dp[0] = 1
mod = 998244353
for i in range(d):
    ndp = [0] * state_num
    for s in range(state_num):
        if dp[i][s] == 0:
            continue
        j = s & 1
        k = s >> 1
        r = 10 if j else N[i] + 1
        for n in range(r):
            nj = j or n < N[i]
            if n == 0 and k == 0:
                nk = 0
            else:
                nk = k | (1 << n)
            ns = nj | (nk << 1)
            ndp[ns] = (ndp[ns] + dp[s]) % mod
    dp = ndp

ans = 0
for s in range(state_num):
    k = s >> 1
    if bin(k).count("1") == 3:
        ans = (ans + dp[s]) % mod
                
ans = (ans - 1) % mod # 0を除外
print(ans)