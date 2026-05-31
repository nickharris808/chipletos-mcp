# 16 — Photonic waveguide design @ 1550 nm

**User prompt:**

> I'm designing a 1550 nm Si strip waveguide. What width gives me Neff = 2.4? What's the propagation loss?

**Tool the agent should call:** `chipletos_predict_waveguide_mode`

**Suggested arguments (sweep candidate widths):**

```json
{
  "width_nm": 500.0,
  "height_nm": 220.0,
  "wavelength_nm": 1550.0,
  "material": "Si",
  "bend_radius_um": 50.0
}
```

The agent should call the tool a handful of times with `width_nm ∈ {400, 450, 500, 550, 600}` (220 nm SOI standard, λ=1550 nm, Si) and bracket the width that yields Neff ≈ 2.4.

**What the agent learns:**

- Effective index `Neff` and group index `ng` per width
- Propagation loss in `dB/cm` (TMM analytical; 5-15% rel-err vs Meep per a recent release disclosure)
- Bend loss in `dB/90°` for the given `bend_radius_um`
- Envelope flag — manufacturability check vs the alpha primitive envelope (width 200-1500 nm, height 180-400 nm, λ 1260-1670 nm, Si or SiN)
- `method` field indicates whether the prediction is the TMM analytical solver or the trained surrogate (surrogate lands a recent release day 14)

**Follow-up:** "Now run DRC on the final width" → `chipletos_photonic_drc` with the chosen `{width_nm, height_nm, material}` geometry. Then "validate the solver against published references" → `chipletos_photonic_validate_ieee`.

**Honest framing:** the a recent release alpha uses the TMM analytical solver in the hot path; Marcatili-Hocker effective-index approximation. Surrogate v1 (R²≥0.999 vs Meep) lands a recent release day 14 and silently swaps in via `waveguide_surrogate.predict`.
