import collections
class mdeque:
    max:int
    min:int
    dq:collections.deque
    def __init__(self,dq:collections.deque) -> None:
        self.dq = dq.copy()
        self.max = max(dq)
        self.min = min(dq)
    def append(self,v:int):
        mxbol = False
        mnbol = False
        if self.max == self.dq[0] and self.max > v:
            mxbol = True
        elif self.max <= v:
            self.max = v
        if self.min == self.dq[0] and self.min < v:
            mnbol = True
        elif self.min >= v:
            self.min = v
        self.dq.append(v)
        if mxbol : self.max = max(self.dq)
        if mnbol : self.min = min(self.dq)