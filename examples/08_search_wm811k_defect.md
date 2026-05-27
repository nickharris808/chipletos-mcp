# 08 — Look up a defect code

**User prompt:**

> What is IPC-A-610 defect code "wafer scratch" and how is it detected?

**Tool the agent should call:** `chipletos_search_defects`

**Suggested arguments:**

```json
{
  "q": "scratch",
  "limit": 10
}
```

**What the agent learns:**

- Per-defect entry: code, family, severity tier, detection method,
  glass-TGV relevance, source standard (IPC / SEMI / ISO)
- Wafer-occurrence count + top CAPA codes (links to corrective action
  database)

**Follow-up:** "Filter to tier-1 critical only" — re-call with
`severity_tier: "tier_1_critical"`.

**Note:** This tool searches the **defect taxonomy** (33 types) for code
lookup. For WM-811K wafer-map *classification* (the 9-class CNN headline
from Genesis CLAUDE.md::C6), use the dashboard's wafer-map upload — the
classifier is not exposed as a public POST.
