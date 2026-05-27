# 11 — Full signoff pipeline (predict → DRC → coupon)

**User prompt:**

> Run the full signoff pipeline for a 50 Ω TGV at 28 GHz on Eagle XG: predict the geometry, validate DRC, and generate an Amkor coupon if it passes.

**Tools the agent should chain (in order):**

1. `chipletos_inverse_design` — get the recommended geometry
2. `chipletos_drc_validate` — using the geometry from step 1
3. `chipletos_generate_coupon` — only if step 2 returns `passed: true`

**Example chained payload:**

Step 1:
```json
{"target_z0_ohm": 50.0, "freq_hz": 2.8e10, "glass_name": "EagleXG", "tolerance_pct": 2.0, "include_signoff": true}
```

Step 2 (substitute the diameter / pitch / thickness from step 1):
```json
{"via_geometries": [{"d_um": 40.0, "p_um": 80.0, "t_um": 300.0}]}
```

Step 3 (only if step 2 passed):
```json
{
  "target_z0_ohm": 50.0,
  "freq_ghz": 28.0,
  "via_diameter_um": 40.0,
  "via_pitch_um": 80.0,
  "glass_thickness_um": 300.0,
  "fab_partner": "amkor",
  "n_coupons": 10
}
```

**What the agent learns:**

- How to chain MCP tools without manual intervention
- Conditional execution (skip coupon generation on DRC fail)
- The lab_readiness_score embedded in steps 1 and 3 lets you stop early
  if the verdict is `reject` even before DRC

**Heads-up:** Step 3 requires `CHIPLETOS_API_KEY`.
