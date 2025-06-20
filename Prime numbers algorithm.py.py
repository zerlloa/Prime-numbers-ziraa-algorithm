# © 2025 Abdullah Al-Rashidi. All rights reserved.
# This code is protected. Commercial use, redistribution or modification is prohibited.
# Contact: Theresnorealworld@gmail.com

import timeit
import numpy as np

start_time = timeit.default_timer()

# Constants
FINAL_LIMIT = 10000000  # Adjusted limit
STAGE1_LIMIT = int(np.sqrt(FINAL_LIMIT))  # Sta4e 1 limit based on square root
Ms = np.array([3, 7, 9, 11])  # Multipliers

# Function to precompute factors for Stage 1
def precompute_factors_stage1(Ms, Ps, max_limit):
    S_set = set()
    for ms in Ms:
        for ps in Ps:
            S = ms * ps
            if S <= max_limit:
                S_set.add((S, ps * 10))  # Store S and F as a tuple
    return list(S_set)

# Function to precompute factors for Stage 2
def precompute_factors_stage2(Ms, Ps, max_limit, layer):
    S_set = set()

    # Handle Layer 5: Every Ms * every Ps
    if layer == 5:
        for ms in Ms:
            for ps in Ps:
                S = ms * ps
                if S <= max_limit:
                    S_set.add((S, ps * 10))  # Store S and F as a tuple
    else:
        # Standard handling for other layers (retain original mapping logic)
        layer_mappings = {
            1: {1: 11, 7: 3, 3: 7, 9: 9},
            2: {1: 3, 7: 9, 3: 11, 9: 7},
            3: {1: 7, 7: 11, 3: 9, 9: 3},
            4: {1: 9, 7: 7, 3: 3, 9: 11},
        }

        if layer in layer_mappings:
            layer_map = layer_mappings[layer]
            for ending, ms in layer_map.items():
                filtered_Ps = [ps for ps in Ps if ps % 10 == ending]
                for ps in filtered_Ps:
                    S = ms * ps
                    if S <= max_limit:
                        S_set.add((S, ps * 10))
        else:
            raise ValueError("Invalid layer selected.")

    return list(S_set)

# Optimized sieve for Stage 1
def sieve_with_numpy_stage1(max_num, precomputed_factors):
    sieve = np.ones((max_num // 2) + 1, dtype=bool)
    sieve[0] = False  # Mark index 0 (representing 1) as non-prime

    for S, F in precomputed_factors:
        if S % 2 == 0:
            continue  # Skip even numbers
        sieve[(S // 2)::(F // 2)] = False

    return np.r_[2, (np.where(sieve)[0] * 2 + 1)]  # Convert indices to prime numbers

# Optimized sieve for Stage 2
def sieve_with_numpy_stage2(max_num, precomputed_factors, layer):
    sieve = np.ones((max_num // 2) + 1, dtype=bool)
    sieve[0] = False  

    for S, F in precomputed_factors:
        if S % 2 == 0:
            continue  
        sieve[(S // 2)::(F // 2)] = False  

    layer_rules = {
        1: [5, 3, 7, 9],
        2: [5, 1, 7, 9],
        3: [5, 1, 3, 9],
        4: [5, 1, 3, 7],
        5: [5]
    }

    for rule in layer_rules[layer]:
        if rule % 2 == 0:  
            continue  
        sieve[(rule // 2)::5] = False  

    return np.r_[2, (np.where(sieve)[0] * 2 + 1)]  

# Initialize process
layer = 5
Ps = np.array([3, 7])  # Initial primes
results = []
precomputed_factors_stage1 = np.empty((0, 2), dtype=int)

# Stage 1
new_factors = precompute_factors_stage1(Ms, Ps, STAGE1_LIMIT)
precomputed_factors_stage1 = np.vstack((precomputed_factors_stage1, new_factors))
Ps = sieve_with_numpy_stage1(STAGE1_LIMIT, precomputed_factors_stage1)
results.append((STAGE1_LIMIT, len(Ps)))

# Stage 2
precomputed_factors_stage2 = np.empty((0, 2), dtype=int)
new_factors = precompute_factors_stage2(Ms, Ps, FINAL_LIMIT, layer)
precomputed_factors_stage2 = np.vstack((precomputed_factors_stage2, new_factors))
Ps = sieve_with_numpy_stage2(FINAL_LIMIT, precomputed_factors_stage2, layer)
results.append((FINAL_LIMIT, len(Ps)))

elapsed_time = timeit.default_timer() - start_time

# Output results
print(Ps)
print(f"Elapsed Time: {elapsed_time:.8f} seconds")
for limit, count in results:
    print(f"Limit: {limit:,} -> Total Ps: {count}")
