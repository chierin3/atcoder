mod = 1000000007

#aのb乗をmで割った余りを出力する
def Power(a:int,b:int,m:int=mod)->int:
    ans = 1
    i = 0
    while True:
        w = (1<<i)
        if b < w : break
        if b & w : ans = (ans * a) % m
        a = (a * a) % m
        i += 1
    return ans

def hash_value(H:list,l:int,r:int):
    ans = H[r] - (H[l-1] * Power(100,r-l+1) % mod)
    if ans < 0 : ans += mod
    return ans

def hash_mod(s:str):
    return hash(s) % mod

def hash_str(S:str)->list[int]:
    H = [0] * (len(S)+1)
    for i in range(len(S)):
        H[i+1] = (100 * H[i] + hash_mod(S[i])) % mod
    return H

N,Q = map(int,input().split())
S = input()
H1 = hash_str(S)
H2 = hash_str(S[::-1]) 
for i in range(Q):
    l,r = map(int,input().split())
    if hash_value(H1,l,r) == hash_value(H2,N-r+1,N-l+1) :print("Yes")
    else:print("No")