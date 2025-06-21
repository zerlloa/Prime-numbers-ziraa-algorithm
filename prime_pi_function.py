# Author: Al-Rashidi
# Email: theresnorealworld@gmail.com

import math
import itertools
import numpy as np

def T(x):
    pi_x = np.pi * x
    cot_pi_x = np.cos(pi_x) / np.sin(pi_x)
    return x + 0.5 + (1 / np.pi) * np.arctan(cot_pi_x)

def compute_pi_components(V):

    root = int(math.isqrt(V))
    D = sorted(r + 10*n for r in (3,7,9,11)
                         for n in range((root - r)//10 + 1)
                         if r + 10*n <= root)


    M = [3, 7, 9, 11]


    DD = [d for d in D if d <= int(math.isqrt(root))]


    O = sum(T((V - d*m)/(10*d)) for d in D for m in M)


    S = sorted({d * d2 for d in D for d2 in DD if d*d2 <= root})


    Oc = sum(T((V - s*m)/(10*s)) for s in S for m in M)


    Op = O - Oc


    def prod(seq):
        p = 1
        for x in seq:
            p *= x
        return p


    CF = 0.0
    for k in range(2, len(D)+1):
        for G in itertools.combinations(D, k):
            K = prod(G)
            if K < V:
                CF += (-1)**k * (
                    1 + sum(T((V - m*K)/(10*K)) for m in M if m*K < V)
                )


    CFa = 0.0
    for k in range(2, len(D)+1):
        for G in itertools.combinations(D, k):
            if any(d in S for d in G):
                K = prod(G)
                if K < V:
                    CFa += (-1)**k * (
                        1 + sum(T((V - m*K)/(10*K)) for m in M if m*K < V)
                    )


    Delta = CF - CFa


    Pc = Op - Delta


    Dx = (V*0.4-1)


    pi = (Dx - Pc) + 2

    return {
        "D":           D,
        "DD":          DD,
        "O":           O,
        "S":           S,
        "Oc":          Oc,
        "Op":          Op,
        "CF":          CF,
        "CFa":         CFa,
        "Delta":       Delta,
        "Pc":          Pc,
        "Dx":          Dx,
        "pi(v)":          pi
    }

# Just change V and see.
if __name__ == "__main__":
    V = 1000
    comp = compute_pi_components(V)
    for name, val in comp.items():
        print(f"{name} =", val)
