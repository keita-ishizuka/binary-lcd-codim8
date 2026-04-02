"""
Verify all LCD codes in codim8_data.sobj.

For each entry codes[n] = S, check:
  - |S| = n, elements are distinct and in {1,...,255}
  - C_S is LCD (G G^T nonsingular)
  - S is a cap when n <= 72 or (n <= 120 and n even)
"""

m = 8
F = GF(2)

def is_lcd(H):
    """Check LCD: equivalent to (H H^T)^{-1} exists, i.e. U_S nonsingular."""
    return (H * H.transpose()).det() != 0

def is_cap(S):
    """S is a cap iff no a XOR b is in S for distinct a, b in S."""
    S_set = set(S)
    for i, a in enumerate(S):
        for b in S[i+1:]:
            if (a ^^ b) in S_set - {a, b}:
                return False
    return True

codes = load("codim8_data")
cap_ns = set(range(9, 73)) | set(range(74, 121, 2))
errors = 0

for n in sorted(codes.keys()):
    S = codes[n]

    if len(S) != n or len(set(S)) != n or not all(1 <= x <= 255 for x in S):
        print(f"FAIL n={n}: size or range error")
        errors += 1
        continue

    H = matrix(F, m, n, [[(s >> i) & 1 for s in S] for i in range(m)])
    if not is_lcd(H):
        print(f"FAIL n={n}: not LCD")
        errors += 1
        continue

    if n in cap_ns and not is_cap(S):
        print(f"FAIL n={n}: not a cap")
        errors += 1
        continue

print(f"Verified {len(codes)} codes, {errors} errors.")
