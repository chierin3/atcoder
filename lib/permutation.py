import itertools

#0以上n-1以下の整数の長さmの順列を生成
def getPerm(n:int,m:int)->list[tuple]:
    return list(itertools.permutations(range(n),m))

print(getPerm(4,2))

#文字列並び替えの全列挙(重複を除く)
def getPermS(S:str)->set:
    return set(map("".join,itertools.permutations(S)))

print(getPermS("abc"))

#文字列並び替えの全列挙
#ansに返り値の配列、resに経過を記録する配列を渡す
def dfs(S:str,fl:int,ans:list,res:list):
    if fl == 0 :
        ans.append("".join(map(str,res)))
        return
    for i in range(len(S)):
        if fl & (1<<i) :
            resC = res.copy()
            resC.append(S[i])
            dfs(S,fl^(1<<i),ans,resC)

S,K = input().split()
K = int(K)
l = len(S)
slist = []
dfs(S,(1<<l)-1,slist,[])
slist = sorted(list(set(slist)))
print(slist[K-1])