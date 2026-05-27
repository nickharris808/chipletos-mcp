# 01 — Predict 50 Ω geometry on Eagle XG @ 28 GHz

**User prompt:**

> I need a 50 Ω glass-TGV at 28 GHz on Eagle XG. What dimensions should I use?

**Tool the agent should call:** `chipletos_inverse_design`

**Suggested arguments:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_hz": 2.8e10,
  "glass_name": "EagleXG",
  "glass_dk": 5.27,
  "glass_df": 0.005,
  "tolerance_pct": 2.0,
  "include_signoff": true
}
```

**What the agent learns:**

- Recommended `diameter_um`, `pitch_um`, `glass_thickness_um`
- Surrogate Z₀ with confidence interval
- OOD flag + regime
- Optional BEM refinement and route-backed signoff
- Composite `lab_readiness_score`

**Follow-up:** "Now run DRC on that geometry" → calls `chipletos_drc_validate`.
