# 12 — UCIe-Advanced link design

**User prompt:**

> Design a 50 Ω TGV that passes UCIe-Advanced spec at 32 GT/s (≈16 GHz fundamental). Use Eagle XG.

**Tool the agent should call:** `chipletos_inverse_design`

**Suggested arguments:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_hz": 1.6e10,
  "glass_name": "EagleXG",
  "glass_dk": 5.27,
  "glass_df": 0.005,
  "tolerance_pct": 1.5,
  "max_iterations": 600,
  "include_signoff": true
}
```

**Then validate:**

- Call `chipletos_pareto_design` with `objectives: ["z0", "loss"]` and
  `il_max_db: 1.0` to enforce the UCIe insertion-loss budget at 16 GHz.

**Genesis context:** UCIe regime gets 81.6 % gap closure on the a recent release
v2-clean Palace residual cal head; the v3 surrogate is well-calibrated
on UCIe geometries (see CLAUDE.md::C20).

**Follow-up:** "Now generate a MOSIS coupon for this design" →
`chipletos_generate_coupon` with `fab_partner: "mosis"`.
