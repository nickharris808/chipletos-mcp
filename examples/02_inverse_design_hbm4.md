# 02 — HBM4 channel inverse design

**User prompt:**

> Inverse-design a 50 Ω HBM4 channel TGV at 6.4 GHz, EagleXG, with ±1% tolerance and route-backed signoff.

**Tool the agent should call:** `chipletos_inverse_design`

**Suggested arguments:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_hz": 6.4e9,
  "glass_name": "EagleXG",
  "glass_dk": 5.27,
  "tolerance_pct": 1.0,
  "max_iterations": 600,
  "include_signoff": true,
  "initial_diameter_um": 25,
  "initial_pitch_um": 55
}
```

**What the agent learns:**

- HBM4 regime is the tightest tolerance band in PROV 7
- v2-clean cal head gives 90.3% gap closure on HBM4 (Genesis CLAUDE.md::C20)
- Lab readiness verdict band is critical for HBM4 — design must pass on first tape-out

**Follow-up:** "Compare this geometry to the closest literature reference" →
`chipletos_validate_against_measurement`.
