import sys
import random
import time
import math

class State:
    def __init__(self, A, C):
        self.A = A
        self.C = C

    def get_score(self):
        score = 0
        CA = [[] for _ in range(6)]
        for i in range(M):
            CA[self.C[i]-ord("a")].append(i)
        for i in range(N):
            dp = [[0] * M for _ in range(len(S[i])+1)]
            for j in range(M):
                dp[0][j] = 1 / M
            for j in range(len(S[i])):
                b = ord(S[i][j]) - ord("a")
                for k in range(M):
                    for l in CA[b]:
                        dp[j+1][l] += dp[j][k] * self.A[k][l] / 100
            count = sum(dp[-1]) * L
            if count >= 1:
                score += P[i]
        return score
    
class Neighborhood:
    def forward(self, state):
        pass
    def backward(self, state):
        pass

class SwapNeighborhood(Neighborhood):
    i = j = -1
    def forward(self, state):
        i = j = -1
        while i == j:
            i = random.randint(0, M-1)
            j = random.randint(0, M-1)
        state.A[i][j] += 1
        state.A[j][i] -= 1
        self.i = i
        self.j = j

    def backward(self, state):
        state.A[self.i][self.j] -= 1
        state.A[self.j][self.i] += 1

class SimulatedAnnealing:
    best_score = 0
    def __init__(self, initial_state:State, initial_temp:int, final_temp:int, start_time:float, end_time:float):
        self.state = initial_state
        self.temp = initial_temp
        self.final_temp = final_temp
        self.start_time = start_time
        self.end_time = end_time
        self.neighborhoods:list[Neighborhood] = []

    def anneal(self):
        self.best_score = self.state.get_score()
        while True:
            neighborhood = random.choice(self.neighborhoods)
            neighborhood.forward(self.state)
            new_score = self.state.get_score()
            temp = self.temp - (self.temp - self.final_temp) * (time.time() - self.start_time) / self.end_time
            prob = math.exp(min(0.0, (new_score - self.best_score) / temp))
            if prob > random.random():
                self.best_score = new_score
            else:
                neighborhood.backward(self.state)
            if time.time() - self.start_time > self.end_time:
                break

N,M,L = map(int,input().split())
S = []
P = []
for i in range(N):
    s,p = input().split()
    S.append(s)
    P.append(int(p))
SS = [[0] * 6 for i in range(6)]
for i in range(N):
    for j in range(len(S[i])-1):
        a = ord(S[i][j]) - ord("a")
        b = ord(S[i][j+1]) - ord("a")
        SS[a][b] += 1
C = [ord("a") + i%6 for i in range(M)]
A = [[0] * M for _ in range(M)]
for i in range(M):
    for j in range(M):
        total = sum(SS[i%6]) * 2
        A[i][j] = int(SS[i%6][j%6] / total * 100)
    A[i][0] += 100 - sum(A[i])

def get_score():
    score = 0
    CA = [[] for _ in range(6)]
    for i in range(M):
        CA[C[i]-ord("a")].append(i)
    for i in range(N):
        dp = [[0] * M for _ in range(len(S[i])+1)]
        for j in range(M):
            dp[0][j] = 1 / M
        for j in range(len(S[i])):
            b = ord(S[i][j]) - ord("a")
            for k in range(M):
                for l in CA[b]:
                    dp[j+1][l] += dp[j][k] * A[k][l] / 100
        count = sum(dp[-1]) * L
        if count >= 1:
            score += P[i]
    return score

best_score = get_score()
start = time.time()
start_temp = 180
end_temp = 1
while True:
    i = random.randint(0, M-1)
    p = random.random()
    if p < 0.6:
        j = random.randint(0, M-1)
        k = random.randint(0, M-1)
        if j == k : continue
        if A[i][k] == 0 : continue
        dp = random.randint(1, A[i][k])
        A[i][j] += dp
        A[i][k] -= dp
    else:
        j = C[i] - ord("a")
        while j == C[i] - ord("a"):
            j = random.randint(0, 5)
        old = C[i]
        C[i] = ord("a") + j
    new_score = get_score()
    temp = start_temp - (start_temp - end_temp) * (time.time() - start) / 1.9
    prob = math.exp(min(0.0, (new_score - best_score) / temp))
    if prob > random.random():
        best_score = new_score
        print(best_score, file=sys.stderr)
    else:
        if p < 0.6:
            A[i][j] -= dp
            A[i][k] += dp
        else:
            C[i] = old
    if time.time() - start > 1.9:
        break

for i in range(M):
    print(chr(C[i]),*A[i])