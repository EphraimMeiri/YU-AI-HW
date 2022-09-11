#search

import state
import frontier

def search(n):
    ins_count=0
    pop_count=0
    dep_count=0
    for round in range(1,101):
        #print("_",round)
        s=state.create(n)
        #print(s)
        f=frontier.create(s)
        while not frontier.is_empty(f):
            s=frontier.remove(f)
            pop_count+=1
            if state.is_target(s):
                dep_count+= f[1]
                #print([s, f[1]])
                break
                # return [s, f[1]]
            ns=state.get_next(s)
            #print(ns)
            for i in ns:
                ins_count+=1
                frontier.insert(f,i) 
    dep_count/=100
    ins_count/=100
    pop_count/=100
    print("Average depth:",dep_count)
    print("Average number pushed:",ins_count)
    print("Average number popped:",pop_count)
    
    # return 0
print("SEARCH 2")
answer=search(2)
print(f"\nSEARCH 3")
answer=search(3)
print(f"\nSEARCH 4")
answer=search(4)
# print(answer)

"""
SEARCH 2
Average depth: 1.61
Average number pushed: 5.83
Average number popped: 5.44

SEARCH 3
Average depth: 5.97
Average number pushed: 6474.5
Average number popped: 3764.76
---------------------------------


SEARCH 2
Average depth: 1.81
Average number pushed: 7.34
Average number popped: 6.72

SEARCH 3
Average depth: 5.93
Average number pushed: 1457.94
Average number popped: 838.62
---------------------------------

SEARCH 2
Average depth: 1.71
Average number pushed: 6.62
Average number popped: 6.09

SEARCH 3
Average depth: 6.03
Average number pushed: 1374.49
Average number popped: 791.47

SEARCH 4

"""
