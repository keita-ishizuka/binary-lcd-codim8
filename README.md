# Construction data for binary LCD codes of codimension 8

DOI: [10.5281/zenodo.23486097](https://doi.org/10.5281/zenodo.23486097)

Explicit binary LCD [n, n-8] codes for 9 <= n <= 247, used in

> K. Ishizuka and Y. Kamio, "Caps and LCD codes with large dimensions."

The paper determines d_2^E(n, n-8) for all n; the constructions for 41 <= n <= 246 are taken from this data.

## Files

- `codim8_sets.txt`: one line `n: s_1 s_2 ... s_n` per length n (239 lines).
  Each s_i is an integer in {1, ..., 255}; its binary digits (bit 0, ..., bit 7) form the i-th column of the
  8 x n parity-check matrix H_S of the code C_S. The matrix U_S = H_S H_S^T over GF(2) is nonsingular, so
  C_S is an LCD [n, n-8, >= 3] code. For n <= 72 and for even n <= 120 the set S is a cap, so d(C_S) >= 4.
- `verify.py`: checks all of the above (plain Python 3, no dependencies): `python3 verify.py codim8_sets.txt`.
- `codim8_data.sobj`, `codim8_verify.sage`: the same data as a SageMath dictionary `{n: S}` and the original
  SageMath check (`sage codim8_verify.sage`).

Both checks report `Verified 239 codes, 0 errors.`

## License

CC BY 4.0. Please cite the paper and this record if you use the data.
