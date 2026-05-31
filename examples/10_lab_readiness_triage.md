# 10 — Score lab readiness for tape-out

**User prompt:**

> Score the lab readiness of a 50 Ω TGV at 28 GHz on Eagle XG. Should I tape out?

**Tool the agent should call:** `chipletos_lab_readiness_score`

**Suggested arguments:**

```json
{
  "target_z0_ohm": 50.0,
  "freq_hz": 2.8e10,
  "glass_name": "EagleXG",
  "tolerance_pct": 2.0
}
```

**What the agent learns:**

- 0-100 composite score across available a recent release gates (BEM stability,
  cross-solver consensus, in-distribution check, signoff route success,
  manufacturability)
- Verdict band: `send_to_lab` (≥95), `send_with_extra_qc` (80-94),
  `hold` (60-79), `reject` (<60)
- `partial_score: true` when some gates lack data — NO fabricated proxies
  per a recent release Chunk 4b
- Geometry + surrogate prediction + convergence

**Follow-up:** If `verdict == hold`, ask the agent for the worst gate and
the suggested remediation; then re-run with the tightened design.
