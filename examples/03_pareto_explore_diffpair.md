# 03 — Pareto explore a diff-pair design

**User prompt:**

> Show me a Pareto front of 7 designs targeting 100 Ω differential at 28 GHz on AF32, trading off loss vs crosstalk.

**Tool the agent should call:** `chipletos_pareto_design`

**Suggested arguments:**

```json
{
  "z0_target_ohm": 100.0,
  "freq_ghz": 28.0,
  "glass_name": "AF32",
  "glass_dk": 5.10,
  "glass_df": 0.005,
  "objectives": ["loss", "crosstalk"],
  "n_pareto_points": 7,
  "diameter_min_um": 20,
  "diameter_max_um": 60,
  "pitch_min_um": 60,
  "pitch_max_um": 220,
  "refine_with_solver": true
}
```

**What the agent learns:**

- Pareto-rank=1 points form the actual frontier
- Loss vs crosstalk trade-off curve
- Use C7 differential scaling law (`log(Z0_diff) = 0.338·log(sep/d), R²=0.918`) to translate Z₀_single → Z₀_diff

**Note:** the Pareto route uses a pure-Python coax-proxy hot path; the historical
d/p ∈ [0.4, 0.5] SIGSEGV (see Genesis CLAUDE.md::C38). Pick a different
diameter or pitch range.
