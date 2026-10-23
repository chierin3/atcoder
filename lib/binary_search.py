import bisect

def binary_search(list,value):
    result = bisect.bisect(list,value)
    if list[result-1] == value:
        return True
    else:
        return False

a = [1,2,3,4,5]
b = 0
print(binary_search(a,b))