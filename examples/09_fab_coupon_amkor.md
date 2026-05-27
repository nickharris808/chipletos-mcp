# 09 — Generate an Amkor fab coupon bundle

**User prompt:**

> Generate a 10-coupon RFQ bundle for Amkor: 50 Ω target at 28 GHz, Eagle XG 300 µm, 40 µm / 80 µm vias.

**Tool the agent should call:** `chipletos_generate_coupon`

**Suggested arguments:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_ghz": 28.0,
  "glass_name": "EagleXG",
  "glass_thickness_um": 300,
  "via_diameter_um": 40,
  "via_pitch_um": 80,
  "fab_partner": "amkor",
  "n_coupons": 10,
  "include_test_per_coupon": true
}
```

**What the agent learns:**

- DRC verdict + violation list
- 12-layer Amkor lithography stack-up
- Per-foundry SOW in JSON + Markdown form (paste straight into RFQ)
- Cost estimate (typical band $55K–$165K for an Amkor 10-coupon run)
- Optional `lab_readiness_score` verdict — if `hold` or `reject`,
  `partial=True` and `partial_failure_reasons` is populated

**Heads-up:** This route is API-key-gated. Set `CHIPLETOS_API_KEY` in
the MCP server env (issued from the ChipletOS dashboard) or the call
returns 401 with a setup hint.
