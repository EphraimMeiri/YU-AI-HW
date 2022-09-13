#search

import state
import frontier

def search(n):
    ins_count=0
    pop_count=0
    dep_count=0
    cost_count=0
    for round in range(1,101):
        s=state.create(n)
        f=frontier.create(s)
        while not frontier.is_empty(f):
            s=frontier.remove(f)
            pop_count+=1
            if state.is_target(s):
                if len(s[0])!=0:           
                    dep_count+= f[1]
                    cost_count+= len(s[1])
                else:
                    print("Failed")
                break
            ns=state.get_next(s)
            for i in ns:
                ins_count+=1
                frontier.insert(f,i) 
    dep_count/=100
    ins_count/=100
    pop_count/=100
    cost_count/=100
    print("\nAverage depth:",dep_count)
    print("Average number pushed:",ins_count)
    print("Average number popped:",pop_count)
    print("Average path   length:",cost_count)
    # return 0
print("SEARCH 2")
answer=search(2)
print(f"\nSEARCH 3")
answer=search(3)
print(f"\nSEARCH 4")
answer=search(4)
# print(answer)

"""
UNWeighted results for dist1:
SEARCH 2

Average depth: 2.54
Average number pushed: 2.54
Average number popped: 2.75
Average path   length: 1.53

SEARCH 3

Average depth: 41.31
Average number pushed: 41.31
Average number popped: 24.02
Average path   length: 6.46

SEARCH 4
Average depth: 71870.78
Average number pushed: 71870.78
Average number popped: 34019.49
Average path   length: 16.14
----------------------------------------
Weighted results for dist1:
SEARCH 2

Average depth: 2.49
Average number pushed: 2.49
Average number popped: 2.72
Average path   length: 1.58

SEARCH 3

Average depth: 42.02
Average number pushed: 42.02
Average number popped: 24.3
Average path   length: 6.1

SEARCH 4

Average depth: 12728.88
Average number pushed: 12728.88
Average number popped: 6045.9
Average path   length: 16.54
----------------------------------------
UNWeighted results for dist2:
SEARCH 2

Average depth: 2.57
Average number pushed: 2.57
Average number popped: 2.84
Average path   length: 1.53

SEARCH 3

Average depth: 32.62
Average number pushed: 32.62
Average number popped: 19.19
Average path   length: 6.45

SEARCH 4

Average depth: 18572.37
Average number pushed: 18572.37
Average number popped: 9131.36
Average path   length: 16.71
----------------------------------------
Weighted results for dist2:
SEARCH 2

Average depth: 2.25
Average number pushed: 2.25
Average number popped: 2.51
Average path   length: 1.28

SEARCH 3

Average depth: 26.25
Average number pushed: 26.25
Average number popped: 15.25
Average path   length: 6.58

SEARCH 4

Average depth: 48734.73
Average number pushed: 48734.73
Average number popped: 23909.28
Average path   length: 23.58
----------------
----------------
----------------
How does this affect the runtime (number of states checked) and optimality (actual cost of found solution) of the code?

"""


























""" OLD RESULTS, didn't include path length:

UNweighted results for dist1:

SEARCH 2
Average depth: 2.92
Average number pushed: 2.92
Average number popped: 3.06

SEARCH 3
Average depth: 31.31
Average number pushed: 31.31
Average number popped: 18.06

SEARCH 4
Average depth: 34771.21
Average number pushed: 34771.21
Average number popped: 16467.46

Weighted results for dist1:
SEARCH 2
Average depth: 2.64
Average number pushed: 2.64
Average number popped: 2.86

SEARCH 3
Average depth: 27.0
Average number pushed: 27.0
Average number popped: 15.43

SEARCH 4
Average depth: 6269.58
Average number pushed: 6269.58
Average number popped: 2936.1


"""