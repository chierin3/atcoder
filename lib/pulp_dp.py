from tabnanny import verbose
import pulp

N,W = map(int,input().split())
w = []
v = []
for i in range(N):
    a,b = map(int,input().split())
    w.append(a)
    v.append(b)

prob = pulp.LpProblem('kp01', sense = pulp.LpMaximize)
xs = [pulp.LpVariable('{}'.format(x), cat='Binary', lowBound = 0) for x in range(N)]
prob += pulp.lpDot(v, xs)
prob += pulp.lpDot(w, xs) <= W

status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
print(int(prob.objective.value()))