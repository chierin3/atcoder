#k進数表記のaを10進数に変換
def digit(a:int,k:int)->int:
    i = 0
    ans = 0
    while a:
        ans += (a%10) * (k**i)
        a //= 10
        i += 1
    return ans

#10進数表記のaをk進数に変換
def redigit(a:int,k:int)->int:
    i = 0
    ans = 0
    while a:
        ans += (a%k) * (10**i)
        a //= k
        i += 1
    return ans

#sk進数のaをdk進数に変換
def transdigit(a:int,sk:int,dk:int)->int:
    ans = digit(a,sk)
    ans = redigit(ans,dk)
    return ans

#2進数表記のnにおける1の個数を数える
def bit_total(n:int)->int:
    ans = 0
    while n :
        ans += n % 2
        n //= 2
    return ans

print(transdigit(121,3,2))
print(bit_total(7))