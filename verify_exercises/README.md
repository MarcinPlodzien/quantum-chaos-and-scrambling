# Verification scripts

Standalone, dependency-light Python scripts (`numpy` / `scipy` only) that
**numerically reproduce the key result of each exercise**. They are the ground
truth behind the notebooks and the worked solutions: if a formula in the tutorial
is right, the matching script here confirms it by Monte Carlo or exact linear
algebra.

## Run them

```bash
# one script
python solution_ch3_page_formula.py

# all of them
for f in solution_*.py; do echo "=== $f ==="; python "$f"; done
```

Each script prints its checks and exits `0` on success (most contain `assert`
statements). A few that sample large Haar-random unitaries
(`ch3_page_formula`, `ch3_purity_concentration`, `ch6_tripartite_mi`,
`ch4_syk_symmetry`) take a couple of minutes.

## What each script proves

### Chapter 1 — Mathematical Foundations
| Script | Verifies |
|---|---|
| `solution_ch1_fubini_study.py` | Fubini–Study geodesic distance between qubit states |
| `solution_ch1_entanglement_parametric.py` | Entanglement entropy of a parametric two-qubit state ($S_{\max}=\ln 2$) |
| `solution_ch1_depolarizing_channel.py` | Depolarizing channel is CPTP; entanglement fidelity $F_e = 1-\tfrac{3p}{4}$ |
| `solution_ch1_dla_closure.py` | A dynamical Lie algebra closes under commutators; its dimension |
| `solution_ch1_schur_weyl.py` | Schur–Weyl ($k{=}2$) symmetric/antisymmetric subspace dimensions |
| `solution_ch1_choi_amplitude_damping.py` | Choi matrix of amplitude damping; spectrum $\{2-\gamma,\gamma,0,0\}$ |
| `solution_ch1_dim_lie_algebra.py` | $\dim\mathfrak{su}(2^N) = 4^N-1$ |
| `solution_ch1_exp_surjectivity.py` | Every $U(D)$ element is the exponential of a skew-Hermitian generator |
| `solution_ch1_haar_u1.py` | Haar measure on $U(1)$ is uniform (KS test, vanishing Fourier modes) |
| `solution_ch1_quantum_speed_limit.py` | Geodesic length saturates the Mandelstam–Tamm quantum speed limit |
| `solution_ch1_sectional_curvature.py` | Sectional curvature of $SU(2)\cong S^3(\sqrt2)$ equals $\tfrac12$ |

### Chapter 2 — Random Matrix Theory
| Script | Verifies |
|---|---|
| `solution_ch2_goe_spacing.py` | GOE nearest-neighbour spacings follow the Wigner surmise ($\langle s\rangle=\sqrt\pi$) |
| `solution_ch2_semicircle_moments.py` | Even moments of the Wigner semicircle are Catalan numbers ($m_2{=}1,m_4{=}2,\dots$) |
| `solution_ch2_cue_eigenphase.py` | $2\times2$ CUE eigenphase-spacing density peaks at $\pi$ with value $1/\pi$ |

### Chapter 3 — Haar Measure & Weingarten Calculus
| Script | Verifies |
|---|---|
| `solution_ch3_weingarten_first_moment.py` | First Haar moment (twirl): $\mathbb{E}[UXU^\dagger]=\tfrac{\mathrm{Tr}X}{D}\,\mathbb{I}$ |
| `solution_ch3_swap_trick.py` | The SWAP trick: $\mathrm{Tr}(\rho^2)=\mathrm{Tr}[(\rho\otimes\rho)\,\mathbb{F}]$ |
| `solution_ch3_haar_overlap.py` | Overlap law $\mathrm{Beta}(1,D{-}1)$: $\mathbb{E}=1/D$, $\mathrm{Var}=\tfrac{D-1}{D^2(D+1)}$ |
| `solution_ch3_fourth_moment_trace.py` | $\mathbb{E}\,|\mathrm{Tr}\,U|^4 = 2$ for all $D\ge2$ |
| `solution_ch3_third_moment.py` | $\mathbb{E}\,|\mathrm{Tr}\,U|^6 = 6$ via the full $S_3$ Weingarten sum (exact for $D\ge3$) |
| `solution_ch3_page_formula.py` | Average entanglement entropy matches the Page formula |
| `solution_ch3_purity_concentration.py` | Subsystem purity concentrates at $(d_A+d_B)/(d_Ad_B+1)$ |

### Chapter 4 — Quantum Dynamics & Chaos
| Script | Verifies |
|---|---|
| `solution_ch4_cf_identity.py` | Squared-commutator / OTOC identity $C(t)=2\,(1-\mathrm{Re}\,F(t))$ |
| `solution_ch4_sff_plateau.py` | Spectral form factor plateau equals $D$ |
| `solution_ch4_krylov_complexity.py` | Krylov complexity $\mathcal{C}_K(t)=\sinh^2(\alpha t)$ from linear Lanczos coefficients |
| `solution_ch4_syk_symmetry.py` | Majorana SYK (Jordan–Wigner) realizes GOE/GUE/GSE by $N_M \bmod 8$ |

### Chapter 5 — Designs & Clifford Ensembles
| Script | Verifies |
|---|---|
| `solution_ch5_clifford_otoc.py` | Clifford OTOC takes only the values $0$ or $4$ |
| `solution_ch5_stabilizer_renyi.py` | Stabilizer Rényi entropy: Haar mean $\mathbb{E}[\Xi_P]=\tfrac{4}{D+3}$, $M_2\approx N-2$ |

### Chapter 6 — Applications of Scrambling
| Script | Verifies |
|---|---|
| `solution_ch6_shadow_channel.py` | Single-qubit shadow inverse $\mathcal{M}^{-1}(\tau)=3\tau-\mathrm{Tr}(\tau)\mathbb{I}$ is exact |
| `solution_ch6_numerical_shadows.py` | Classical-shadow estimator converges as $1/\sqrt T$ to the true value |
| `solution_ch6_numerical_rb.py` | Randomized-benchmarking decay $F(m)=A\,\alpha^m+B$ recovers $\alpha$ |
| `solution_ch6_tripartite_mi.py` | Tripartite mutual information $I_3\to -2\ln d$ for scrambled states |
| `solution_ch6_ghz_fragility.py` | GHZ Fisher information $\mathcal{F}_Q=N^2$ collapses to $0$ after one qubit is lost |

### Chapter 7 — Quantum Machine Learning
| Script | Verifies |
|---|---|
| `solution_ch7_barren_plateau.py` | Gradient variance $\sim N/(D+1)\sim 2^{-N}$ (barren plateau) |
| `solution_ch7_local_vs_global_cost.py` | Local cost variance $\sim 1/(N2^N)$ vs global $\sim 2^{-2N}$ |
| `solution_ch7_qelm_concentration.py` | QELM feature variance $\tfrac{D-1}{D^2(D+1)}$; shot budget $\nu\gtrsim D$ |
| `solution_ch7_qrc_injection.py` | Reservoir injection map is contractive; restart overhead $\nu\,T(T{+}1)/2$ |
| `solution_ch7_born_machine.py` | Born-machine entropy deficit $\to 1-\gamma_E\approx0.423$ (Porter–Thomas) |

> The notebooks in `source_notebooks/` present the same results with full
> derivations and plots; these scripts are the minimal, assertion-backed checks.
