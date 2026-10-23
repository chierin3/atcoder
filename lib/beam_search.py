from copy import deepcopy

class State:
    first_action = -1
    def legalActions(self)->list:
        raise NotImplementedError
    def advance(self,action):
        raise NotImplementedError
    def __lt__(self,other)->bool:
        raise NotImplementedError

def beemSearchAction(state:State,depth:int=4,width:int=2):
    Q = [state]
    for d in range(depth):
        candidate = []
        for w in range(width):
            if not Q : break
            q = Q.pop()
            now_state = deepcopy(q)
            legal_actions = now_state.legalActions()
            for action in legal_actions:
                next_state = deepcopy(now_state)
                next_state.advance(action)
                if d == 0 : next_state.first_action = action
                candidate.append(next_state)
        candidate.sort()
        Q.append(candidate.pop())
        Q.append(candidate.pop())
    return Q.pop().first_action

def chokudaiSearchAction(state:State,depth:int=4,width:int=1,number:int=2):
    beam:list[list[State]] = [ [] for _ in range(number) ]
    beam[0].append(state)
    for n in range(number):  
        for d in range(depth):
            beam[d].sort()
            for w in range(width):
                if not beam[d] : break
                q = beam[d].pop()
                now_state = deepcopy(q)
                legal_actions = now_state.legalActions()
                for action in legal_actions:
                    next_state = deepcopy(now_state)
                    next_state.advance(action)
                    if d == 0 : next_state.first_action = action
                    beam[d+1].append(next_state)
    for d in range(depth,-1,-1):
        if beam[d] :
            beam[d].sort() 
            return beam[d][-1].first_action 
    return -1