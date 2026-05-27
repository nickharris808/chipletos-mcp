# 06 — Multi-solver disagreement triage

**User prompt:**

> How well does the ChipletOS BEM agree with full-wave solvers like Palace or HFSS?

**Tool the agent should call:** `chipletos_cross_solver_matrix`

**Arguments:** none required (returns the latest cached witness).

**What the agent learns:**

- Pairwise MAE matrix (BEM × Palace × OpenEMS × gprMax)
- `solver_status` block — which solvers have 100/100 coverage on the
  100-geometry sweep
- `honest_caveat` — current Sprint disclosure for partial solver coverage
- `n_geometries` and `content_sha256` for reproducibility

**Heads-up:** Sprint 32 Palace freq extension measured a 6.73 % median
BEM-vs-Palace freq-spread envelope across 25 geoms × 4 freqs; Sprint 47
refined this to ~17.3 % median across 33 geoms × 6 freqs. Sprint 45 v2-clean
per-regime Palace residual cal heads close the gap to ~4.7 % pooled. See
Genesis `CLAUDE.md::C16` and `C20` for the canonical envelope.
