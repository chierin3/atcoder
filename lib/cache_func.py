#再帰回数の上限を増やす
import sys
sys.setrecursionlimit(10**5)

from functools import cache

@cache
def func(n):
    return func(n-1) + func(n-2) if n > 1 else 1