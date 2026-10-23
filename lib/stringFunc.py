#回文判定
def isPalindrome(S:str)->bool:
    l = len(S)
    for i in range(l//2):
        if S[i] != S[l-i-1] : return False
    return True

# Sの部分文字列の回文判定（最大mismatch数を指定可能）
def count_palindromic_substrings(S, max_mismatches=0):
    ans = 0
    # 文字列長が奇数の場合と偶数の場合の両方を考慮する
    for i in range(2):
        for j in range(len(S)):
            count = 0
            l = j
            r = j + i
            while l >= 0 and r < len(S):
                if S[l] != S[r]:
                    count += 1
                if count > max_mismatches:
                    break
                ans += 1
                l -= 1
                r += 1
    return ans

# ２次元文字列の転置
H,W = map(int, input().split())
S = [list(input()) for _ in range(H)]
if H > W:
    S = list(zip(*S))  # Transpose the grid
    H, W = W, H

print(isPalindrome("ababa"))