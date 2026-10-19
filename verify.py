#!/usr/bin/env python3
"""Verify codim8_sets.txt (plain Python 3, no dependencies).

Each line "n: s_1 ... s_n" gives a set S of n integers in {1,...,255}; s is the column
(bit 0, ..., bit 7) of the parity-check matrix H_S of a binary [n, n-8] code C_S.
For every line, check:
  - |S| = n and the elements are distinct and in {1,...,255}, so d(C_S) >= 3;
  - C_S is LCD, i.e. the 8 x 8 matrix U_S = H_S H_S^T over GF(2) is nonsingular;
  - S is a cap (no a XOR b in S for distinct a, b in S), so d(C_S) >= 4,
    when n <= 72 or n is even with n <= 120.
"""
import sys

M = 8

def gram_rows(S):
    """Rows of U_S = H_S H_S^T as 8-bit integers."""
    rows = []
    for i in range(M):
        r = 0
        for j in range(M):
            if sum((s >> i) & (s >> j) & 1 for s in S) & 1:
                r |= 1 << j
        rows.append(r)
    return rows

def rank_gf2(rows):
    rows, r = list(rows), 0
    for bit in range(M):
        p = next((i for i in range(r, len(rows)) if (rows[i] >> bit) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and (rows[i] >> bit) & 1:
                rows[i] ^= rows[r]
        r += 1
    return r

def is_cap(S):
    T = set(S)
    return not any((a ^ b) in T for i, a in enumerate(S) for b in S[i + 1:])

path = sys.argv[1] if len(sys.argv) > 1 else 'codim8_sets.txt'
cap_ns = set(range(9, 73)) | set(range(74, 121, 2))
count = errors = 0
for line in open(path):
    head, body = line.split(':')
    n, S = int(head), [int(x) for x in body.split()]
    count += 1
    if len(S) != n or len(set(S)) != n or not all(1 <= x <= 255 for x in S):
        print(f'FAIL n={n}: size or range'); errors += 1; continue
    if rank_gf2(gram_rows(S)) != M:
        print(f'FAIL n={n}: not LCD'); errors += 1; continue
    if n in cap_ns and not is_cap(S):
        print(f'FAIL n={n}: not a cap'); errors += 1; continue
print(f'Verified {count} codes, {errors} errors.')
