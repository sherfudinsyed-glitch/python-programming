import time
import sys

# Original Naive Version (for comparison)
def ways_naive(n):
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

# Redesigned Iterative Version
def ways_iterative(n):
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1

# Validation
n_val = 1000

print(f"Testing for n = {n_val}")
print("-" * 30)

# Test Iterative
start = time.perf_counter()
result_iter = ways_iterative(n_val)
end = time.perf_counter()
print(f"Iterative Result: {result_iter}")
print(f"Iterative Time: {end - start:.6f} seconds")

# Test Naive (Only for a small n, as 1000 would hang the computer)
small_n = 30
start = time.perf_counter()
result_naive = ways_naive(small_n)
end = time.perf_counter()
print(f"\nSmall scale test (n={small_n})")
print(f"Naive Result: {result_naive}")
print(f"Naive Time: {end - start:.6f} seconds")
