"""Exercise (Chapter 2): Unfolding a Many-Body Spectrum.

Mixed-field Ising chain, N = 12, open boundaries (J = 1, h_x = 1.05, h_z = 0.5).
Checks every number quoted in the book's solution:
  full-spectrum gap ratio ~ 0.42, reflection sectors ~ 0.54 / 0.52,
  degree-9 unfolding -> unit mean spacing and Var(s) ~ 0.275 (surmise 0.273),
  degree-2 under-fit -> Var ~ 0.36, Chebyshev degree-300 fit -> 0.250 and degree-800 -> 0.18 (gradual over-fit),
  monomial np.polyfit at nominal degree 300 -> ~0.27 because the solver keeps only ~50 singular values,
  cubic smoothing spline (s = 1) over-fit -> Var ~ 0.002.
"""
import warnings
import numpy as np
from numpy.polynomial import Chebyshev
from scipy.interpolate import UnivariateSpline

warnings.filterwarnings("ignore", category=np.exceptions.RankWarning)

N, J, hx, hz = 12, 1.0, 1.05, 0.5
D = 2**N
idx = np.arange(D)
bits = (idx[:, None] >> np.arange(N)[None, :]) & 1
z = 1 - 2*bits
H = np.diag(J*np.sum(z[:, :-1]*z[:, 1:], axis=1) + hz*np.sum(z, axis=1)).astype(float)
for j in range(N):
    H[idx, idx ^ (1 << j)] += hx
E_full = np.linalg.eigvalsh(H)


def gap_ratio(E):
    s = np.diff(E)
    return (np.minimum(s[:-1], s[1:]) / np.maximum(s[:-1], s[1:])).mean()


refl = np.zeros(D, dtype=int)
for j in range(N):
    refl |= ((idx >> j) & 1) << (N - 1 - j)
sym, asym, seen = [], [], np.zeros(D, bool)
for i in range(D):
    if seen[i]:
        continue
    j = refl[i]
    seen[i] = seen[j] = True
    v = np.zeros(D)
    if i == j:
        v[i] = 1.0
        sym.append(v)
    else:
        v[i] = v[j] = 1/np.sqrt(2)
        sym.append(v)
        w = np.zeros(D)
        w[i], w[j] = 1/np.sqrt(2), -1/np.sqrt(2)
        asym.append(w)
Bp, Bm = np.array(sym).T, np.array(asym).T
E_plus = np.linalg.eigvalsh(Bp.T @ H @ Bp)
E_minus = np.linalg.eigvalsh(Bm.T @ H @ Bm)


def central(E, keep=0.8):
    n = len(E)
    lo = int(round(n*(1-keep)/2))
    return E[lo:n-lo], np.arange(lo+1, n-lo+1, dtype=float)


def unfold_poly(E, deg):
    Ec, Nc = central(E)
    return Chebyshev.fit(Ec, Nc, deg)(Ec)


def var_unit_mean(s):
    s = s/s.mean()
    return s.var()


r_full, r_plus, r_minus = gap_ratio(E_full), gap_ratio(E_plus), gap_ratio(E_minus)
e9, e2, e300, e800 = unfold_poly(E_plus, 9), unfold_poly(E_plus, 2), unfold_poly(E_plus, 300), unfold_poly(E_plus, 800)
Ec, Nc = central(E_plus)
spl = UnivariateSpline(Ec, Nc, k=3, s=1)(Ec)

print(f"sector dimensions: {len(E_plus)} / {len(E_minus)}")
print(f"<r> full = {r_full:.3f}, +1 sector = {r_plus:.3f}, -1 sector = {r_minus:.3f}   (GOE 0.531, Poisson 0.386)")
print(f"degree-9 unfolding: mean s = {np.diff(e9).mean():.4f}, Var(s) = {var_unit_mean(np.diff(e9)):.3f}  (surmise {4/np.pi-1:.3f})")
print(f"degree-2 under-fit: Var(s) = {var_unit_mean(np.diff(e2)):.3f}")
print(f"degree-300 Chebyshev fit: Var(s) = {var_unit_mean(np.diff(e300)):.3f}   (gradual over-fit)")
print(f"degree-800 Chebyshev fit: Var(s) = {var_unit_mean(np.diff(e800)):.3f}")
c300, _, rank300, _, _ = np.polyfit(Ec, Nc, 300, full=True)
print(f"nominal degree-300 monomial fit (np.polyfit): Var(s) = {var_unit_mean(np.diff(np.polyval(c300, Ec))):.3f}, solver rank {rank300} of 301 (truncated fit)")
print(f"spline (s = 1) over-fit: Var(s) = {var_unit_mean(np.diff(spl)):.4f}")

assert (len(E_plus), len(E_minus)) == (2080, 2016)
assert abs(r_full - 0.42) < 0.01 and abs(r_plus - 0.54) < 0.01 and abs(r_minus - 0.52) < 0.01
assert abs(np.diff(e9).mean() - 1) < 5e-3 and abs(var_unit_mean(np.diff(e9)) - 0.275) < 0.01
assert abs(var_unit_mean(np.diff(e2)) - 0.36) < 0.02
assert abs(var_unit_mean(np.diff(e300)) - 0.250) < 0.01
assert abs(var_unit_mean(np.diff(e800)) - 0.18) < 0.02
assert rank300 < 100
assert var_unit_mean(np.diff(spl)) < 0.005
print("all checks passed")
