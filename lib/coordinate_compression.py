#座標圧縮
H,W,N = map(int,input().split())
A = [0] * N
B = [0] * N
for i in range(N):
    A[i],B[i] = map(int,input().split())
Adict = {x:i+1 for i,x in enumerate(sorted(list(set(A))))}
Bdict = {x:i+1 for i,x in enumerate(sorted(list(set(B))))}
for i in range(N):
    print(Adict[A[i]],Bdict[B[i]])