import numpy as np
import math

def zscore(x:np.ndarray, axis = None)->np.ndarray:
    xmean = x.mean(axis=axis, keepdims=True)
    xstd  = np.std(x, axis=axis, keepdims=True)
    if xstd :
        zscore = (x-xmean)/xstd
    else :
        zscore = np.array([0]*x.size)
    return zscore

def min_max(x:np.ndarray, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    if min == max :
        result = np.array([0]*x.size)
    else :
        result = (x-min)/(max-min)
    return result

def sigmoid(a,x)->float:
    return 1 / (1 + math.e**(-a*x))

def softmax(a,x)->np.ndarray:
    exp_x = np.exp(a*x)
    sum_exp_x = np.sum(exp_x)
    return exp_x / sum_exp_x

p = np.array([0,0,0,1.2])
p1 = zscore(p)
p1 = p1.clip(0,None)
p2 = min_max(p)**0.5
p3 = softmax(2,p)
print(p1)
print(p2)
print(p3,p3.sum())
print(sigmoid(0.1,-10))