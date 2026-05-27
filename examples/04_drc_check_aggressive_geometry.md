# 04 — DRC validation of an aggressive tight-pitch geometry

**User prompt:**

> Will d=15 µm, p=35 µm, t=200 µm pass DRC on a glass interposer? What about d=10 µm, p=30 µm?

**Tool the agent should call:** `chipletos_drc_validate`

**Suggested arguments:**

```json
{
  "via_geometries": [
    {"d_um": 15.0, "p_um": 35.0, "t_um": 200.0},
    {"d_um": 10.0, "p_um": 30.0, "t_um": 200.0}
  ]
}
```

**What the agent learns:**

- Per-violation IPC/SEMI defect codes
- Severity (error / warning / info)
- Suggested fix per violation (loosen pitch, deepen wall, etc.)
- `passed: bool` for fast triage

**Follow-up:** "Look up the defect code for the first violation" →
`chipletos_search_defects` with `q: "<defect_code>"`.
