# 14 — Ultra-low-loss substrate exploration

**User prompt:**

> I need the lowest-loss substrate for an mmWave 50 Ω TGV at 60 GHz. Sweep all available glasses.

**Tool the agent should call:** `chipletos_predict_impedance`

**Suggested arguments:**

```json
{
  "diameter_um": 40,
  "pitch_um": 100,
  "glass_thickness_um": 300,
  "freq_ghz": 60.0,
  "tolerance_pct": 5.0
}
```

(Note: this routes through `/v1/glass-pdk/cheapest-50ohm` which sweeps every
glass in the material DB.)

**What the agent learns:**

- Per-glass Z₀-achieved + relative cost
- Lowest-loss public glass at mmWave: Fused Silica (Dk≈3.80, Df≈0.0005 —
  10× lower loss tangent than Eagle XG)
- Cost trade-off: Fused Silica index 1.50–1.55 vs Eagle XG baseline 1.00

**Follow-up:** "Now Pareto-explore loss vs cost across the top 3 glasses" —
call `chipletos_pareto_design` 3 times (one per glass), then assemble the
agent-side comparison.
