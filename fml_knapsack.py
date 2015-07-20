#!/usr/pic1/bin/python3
# http://pro.boxoffice.com/statistics/long_term_predictions?w=1
from memoized import memoized
from retrieval import projections_table

# knapsack W is total weight
lookup = projections_table()
W = 1000

@memoized
def m(w, dep):
    if w <= 0:
        return (), (dep - 8) * -2000000 #account for empty screens, -2MM penalty
    elif dep == 8:
        return (), 0
    else:
        maxval = 0
        rst_picks = ()
        for name, info in lookup.items():
            if info['cost'] > w:
                continue
            potential_picks, value = m(w - info['cost'], dep+1)
            tmp = info['proj'] + value
            if tmp > maxval:
                maxval = tmp
                rst_picks = (name, ) + potential_picks

        return rst_picks, maxval

picks, value = m(W, 0)

for p in picks: print(p)
print('-' * 14)
print("cost: ${}".format(sum(lookup[v]['cost'] for v in picks)))
print("earn: ${}MM".format(value/1000000))
