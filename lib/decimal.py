#四捨五入
#round関数は偶数丸めのため不可
from decimal import Decimal,ROUND_HALF_UP

X = float(input())
x = Decimal(X)
print(x.quantize(Decimal("1"),rounding=ROUND_HALF_UP))

#端数切り上げ除算
a = int(input())
b = 10
print((a+b-1)//b)