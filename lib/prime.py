#エラトステネスの篩
N,K = map(int,input().split())
is_prime = [True] * (N+1)
is_prime[0] = False
is_prime[1] = False
for i in range(4,N+1,2):
    is_prime[i] = False
for i in range(3,int(round(N**(1/2)+1,1)),2):
    if is_prime[i]:
        for j in range(i*i,N+1,i):
            is_prime[j] = False

#素因数の種類の数え上げ
N,K = map(int,input().split())
cnt = [0] * (N+1)
for i in range(2,N+1):
    if cnt[i] >= 1 : continue
    for j in range(i,N+1,i) : cnt[j] += 1
ans = 0
for i in range(N+1):
    if cnt[i] >= K : ans += 1
print(ans)

#素因数分解
#エラトステネスの篩を利用して、素数で割り続けることで素因数分解を行う方法です。
from collections import defaultdict
M = 10**7
mod = 998244353
is_prime = [i for i in range(M + 1)] #素数であれば自分自身、そうでなければ最小の素因数を格納するリスト
i = 2
while i * i <= M:
    if is_prime[i] == i:
        for j in range(i * i, M + 1, i):
            is_prime[j] = i
    i += 1

N = int(input())
A = list(map(int, input().split()))

prime_count = [defaultdict(int) for _ in range(N)]
E1 = dict()
for i in range(N):
    n = A[i]
    #nが1になるまで、最小の素因数で割り続けることで、素因数分解を行います。
    while n > 1:
        prime_count[i][is_prime[n]] += 1
        n //= is_prime[n]
    for k, v in prime_count[i].items():
        if k not in E1 or E1[k] < v:
            E1[k] = v
            
#Lは、Aの要素の最小公倍数を表す変数です。各素因数の最大の指数を掛け合わせることで、最小公倍数を求めます。
L = 1
for k in E1.keys():
    L = L * (k ** E1[k]) % mod