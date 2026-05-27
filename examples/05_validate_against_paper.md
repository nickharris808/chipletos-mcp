# 05 — Cross-check surrogate vs Sukumaran 2014

**User prompt:**

> Pull the closest matching geometry from Sukumaran 2014 and compare the surrogate prediction.

**Tool the agent should call:** `chipletos_validate_against_measurement`

**Suggested arguments (typical Sukumaran 2014 geometry):**

```json
{
  "diameter_um": 50.0,
  "pitch_um": 100.0,
  "glass_thickness_um": 300.0,
  "freq_ghz": 10.0,
  "glass_name": "EagleXG",
  "metric": "Z0_ohm",
  "geometry_match_tolerance_pct": 20.0
}
```

**What the agent learns:**

- Matched reference ID + source_type (`measurement` or `simulation`)
- Surrogate-vs-reference absolute error %
- `within_tolerance` verdict
- Honest framing: most Z₀ literature entries are HFSS-coaxial simulations,
  not VNA measurements — the queued $200-500K wet-lab campaign is the
  unlock for true measured-truth.

**Source:** Sukumaran et al., "Through-Package-Via Formation and Metallization
of Glass Interposers," IEEE TCPMT 2014 (Z₀ ≈ 50.3 Ω at 10 GHz on this
geometry per Genesis literature corpus).
