# 18 — Photonic solver validation vs IEEE references

**User prompt:**

> What's the agreement between ChipletOS's analytical photonic waveguide solver and published silicon-photonic reference values?

**Tools the agent should call:** `chipletos_photonic_validate_ieee` (primary) + `chipletos_photonic_signoff_health` (for context on which solver is in the hot path)

**Suggested arguments:**

```json
{}
```

(Both endpoints take no parameters.)

**What the agent learns:**

- Per-paper measured Neff/ng vs TMM-predicted Neff/ng for 5 published silicon-photonic references:
  - Bogaerts 2018 (J. Lightwave Tech.)
  - Pavanello 2020 (IEEE Photonics J.)
  - Lim 2014 (IEEE JSTQE)
  - Selvaraja 2010 (J. Lightwave Tech.)
  - Xu 2017 (Opt. Lett.)
- Relative error % per paper
- Pooled MAE across all 5 references
- PASS / FAIL verdict against the 10 % threshold
- From `chipletos_photonic_signoff_health`: which solver is currently in the hot path (Sprint 50 alpha = TMM analytical; Sprint 50 day 14 swaps in surrogate v1 with R² ≥ 0.999 vs Meep)

**Why this matters:** the answer is a key buyer-DD reviewer question — "how accurate is the solver?" The IEEE cross-check is the truth-lane equivalent of the chiplet-side `chipletos_validate_against_measurement` tool. Honest framing: Sprint 50 ships the cross-check at the alpha-TMM level; Meep cross-check lands once the surrogate trains.

**Follow-up:** "Now design a waveguide on top of that solver" → `chipletos_predict_waveguide_mode`. Or: "What other photonic primitives are supported?" — the `signoff_health` response already lists waveguide (alpha) + MZI / MMI / ring / grating / photonic-crystal (queued S51-S55).
