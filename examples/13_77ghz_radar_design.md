# 13 — 77 GHz automotive radar TGV

**User prompt:**

> Design a 50 Ω TGV at 77 GHz (automotive radar band) optimized for flat group delay. AF32 glass.

**Tools the agent should call:**

1. `chipletos_inverse_design`
2. `chipletos_cross_solver_matrix` — verify the BEM/Palace envelope at 77 GHz

**Suggested arguments for step 1:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_hz": 7.7e10,
  "glass_name": "AF32",
  "glass_dk": 5.10,
  "glass_df": 0.005,
  "tolerance_pct": 2.0,
  "include_signoff": true
}
```

**Genesis context:**

- Sprint 39 Bucket 5 ships a multi-solver-verified `golden_mmwave_77ghz` kit
  (Z₀=40.52 Ω at 77 GHz, 3.75:1 pitch:diameter for group-delay flatness)
- Sprint 45 v2-clean MMWAVE regime per-regime cal head: 43 % gap closure
  (Sprint 47 hidden=128 sweep lifts to 79.8 %, near-elite)
- BEM-vs-Palace envelope at 77 GHz: median 17 % spread (Sprint 47 33×6 sweep)

**Honest disclosure to surface to the user:** mmWave regime is where the
BEM-vs-Palace envelope is widest. Cross-solver consensus check is
recommended before tape-out.
