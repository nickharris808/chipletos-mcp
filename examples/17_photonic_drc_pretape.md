# 17 — Photonic DRC pre-tape-out

**User prompt:**

> Before I send this PIC layout to fab, run DRC against AIM Photonics rules. I have three primitives:
> 1. A 450 nm wide Si strip waveguide
> 2. A ring resonator with radius 8 µm, coupler gap 200 nm, width 500 nm
> 3. A grating coupler with 630 nm period, duty cycle 0.5, width 10 µm

**Tool the agent should call:** `chipletos_photonic_drc`

**Suggested arguments:**

```json
{
  "geometries": [
    {"type": "waveguide", "width_nm": 450.0, "height_nm": 220.0, "material": "Si"},
    {"type": "ring", "radius_um": 8.0, "coupler_gap_nm": 200.0, "width_nm": 500.0},
    {"type": "grating", "period_nm": 630.0, "duty_cycle": 0.5, "width_nm": 10000.0}
  ]
}
```

**What the agent learns:**

- Per-violation entries with `rule_id`, `severity` (error / warning / info), `message`, `value`, `limit`, and `suggestion`
- `passed: bool` for fast triage — `false` if any errors fire
- `n_errors / n_warnings / n_info` counts
- `rules_applied` echoes the AIM Photonics-class rule set that was used (min feature 80 nm, min spacing 100 nm, min bend radius per mode-class, max width for single-mode)

**Override individual rules** (e.g. for a custom foundry):

```json
{
  "geometries": [...],
  "design_rules": {
    "min_feature_nm": 120,
    "min_spacing_nm": 150
  }
}
```

**Follow-up:** "What does that defect code mean?" → `chipletos_search_defects` with `q: "<rule_id>"`. Then "is the solver trustworthy here?" → `chipletos_photonic_validate_ieee`.
