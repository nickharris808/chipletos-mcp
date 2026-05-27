# 15 — Compare Eagle XG vs AF32 vs Borofloat33

**User prompt:**

> Compare Eagle XG, AF32, and Borofloat33 for a 50 Ω TGV at 10 GHz. Same diameter and pitch. Which gives the lowest loss and is it manufacturable?

**Tools the agent should call (in order):**

1. `chipletos_predict_impedance` (sweeps all glasses for that geometry)
2. `chipletos_drc_validate` (sanity-check the recommended geometry)
3. `chipletos_validate_against_measurement` (per glass, ideally)

**Step 1 args:**

```json
{
  "diameter_um": 50,
  "pitch_um": 120,
  "glass_thickness_um": 300,
  "freq_ghz": 10.0,
  "tolerance_pct": 5.0
}
```

The response contains a per-glass ranking. The agent can present a comparison
table: glass | Z₀ achieved | cost index | Dk | Df | converged.

**Follow-up:** For each glass, optionally also call
`chipletos_validate_against_measurement` with that glass + geometry to
cross-check the surrogate prediction against the literature corpus
(EN-A1, Eagle XG, AF32, Borofloat33 all have published Z₀ entries).

**Genesis context:** Eagle XG is the baseline (cost index 1.00); Borofloat33
is the cheapest public glass (0.70); Fused Silica is the lowest-loss but
most expensive (1.50–1.55).
