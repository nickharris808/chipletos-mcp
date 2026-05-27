# 07 — Find a similar S2P in the library

**User prompt:**

> Find me 20 S2P files on Eagle XG with pitch between 60 and 100 µm.

**Tool the agent should call:** `chipletos_search_s2p_library`

**Suggested arguments:**

```json
{
  "glass": "EagleXG",
  "pitch_min": 60,
  "pitch_max": 100,
  "limit": 20,
  "offset": 0
}
```

**What the agent learns:**

- 2.27M+ asset registry (per Genesis CLAUDE.md::C9)
- Per-asset metadata: glass, thickness, pitch, asset_id, relative_path
- Pagination via `limit` + `offset`
- Files import directly into Cadence Sigrity, ANSYS HFSS, Keysight ADS

**Follow-up:** "Download asset XYZ" — point the user to the Genesis
`/v1/library/s2p/download?id=XYZ` direct endpoint (the MCP server can return
the URL; binary download is out of scope for MCP text tools).
