#aのb乗をmで割った余りを出力する
def Power(a:int,b:int,m:int=1000000007)->int:
    ans = 1
    i = 0
    while True:
        w = (1<<i)
        if b < w : break
        if b & w : ans = (ans * a) % m
        a = (a * a) % m
        i += 1
    return ans

#aの階乗をmで割った余りを出力する
def Factorial(a:int,m:int=1000000007)->int:
    ans = 1
    for i in range(1,a+1) : ans = (ans * i) % m
    return ans

#nCrをmで割った余りを出力する
def Combination(n:int,r:int,m:int=1000000007)->int:
    a = Factorial(n,m)
    b = Factorial(r,m) * Factorial(n-r,m)
    return a * Power(b,m-2,m) % m   

print(Combination(50,10))
print(Power(2,10**9))