# Author: Al-Rashidi
# Email: Theresnorealworld@gmail.com

import math
from itertools import combinations
from collections import Counter

def compute_pi_components(V):

    root = int(math.isqrt(V))
    D = sorted(r + 10 * n for r in [3, 7, 9, 11] for n in range(root // 10 + 1) if r + 10 * n <= root)


    Dprime = sorted(d for d in D if d <= int(math.isqrt(root)))


    Sc = sorted({d * dp for d in D for dp in Dprime if d * dp <= root})


    M = [3, 7, 9, 11]


    O = Counter()
    for d in D:
        for m in M:
            s = d * m
            f = 10 * d
            n_max = (V - s) // f
            for n in range(n_max + 1):
                O[s + f * n] += 1


    Oc = Counter()
    for s0 in Sc:
        for m in M:
            s = s0 * m
            f = 10 * s0
            n_max = (V - s) // f
            for n in range(n_max + 1):
                Oc[s + f * n] += 1


    Op = O - Oc


    Ds = {d1 * d2 for d1 in D for d2 in D if d1 <= d2 and d1 * d2 <= root and d1 * d2 > 1}


    CF_all = Counter()
    for k in range(2, len(D) + 1):
        CFk = Counter()
        for G in combinations(D, k):
            K = math.prod(G)
            if K < V:
                CFk[K] += 1
                for m in M:
                    s = m * K
                    f = 10 * K
                    n_max = (V - s) // f
                    for n in range(n_max + 1):
                        CFk[s + f * n] += 1
        if k == 2:
            CF_all = CFk.copy()
        else:
            CF_all -= CFk


    CFa_all = Counter()
    for k in range(2, len(D) + 1):
        CFa_k = Counter()
        for G in combinations(D, k):
            if any(d in Ds for d in G):
                K = math.prod(G)
                if K < V:
                    CFa_k[K] += 1
                    for m in M:
                        s = m * K
                        f = 10 * K
                        n_max = (V - s) // f
                        for n in range(n_max + 1):
                            CFa_k[s + f * n] += 1
        if k == 2:
            CFa_all = CFa_k.copy()
        else:
            CFa_all -= CFa_k


    Delta = CF_all - CFa_all


    Pc = Op - Delta


    Dx = [d for d in range(1, V + 1) if d % 10 in (1, 3, 7, 9) and d != 1]


    pure_composites = set(Pc.elements())
    P = sorted(set(Dx) - pure_composites)
    P = [2, 5] + P

    return {
        'D': D,
        'DD': Dprime,
        'Sc': Sc,
        'M': M,
        'O': O,
        'Oc': Oc,
        'Op': Op,
        'CF': CF_all,
        'CFa': CFa_all,
        'Delta': Delta,
        'Pc': Pc,
        'Dx': Dx,
        'PR': P,
        'PR all': len(P)
    }

# Just change V and see.
if __name__ == "__main__":
    V = 1000
    comp = compute_pi_components(V)
    for name, val in comp.items():
        print(f"{name} =", val)
