# Tools reference

`chipletos-mcp` exposes 14 tools across two sub-brands: chiplet packaging
signoff (glass-TGV PDK, 10 tools) + Photonic Signoff (silicon-photonic
design, 4 tools — a recent release/51 alpha). Each is a thin wrapper around a public
(or API-key-gated) route on the ChipletOS / Genesis Modal API at
`https://nickharris808--genesis-api-fastapi-app.modal.run`.

This page documents the canonical mapping. For full request / response
schemas, see the live API at
<https://nickharris808--genesis-api-fastapi-app.modal.run/docs>.

## Chiplet packaging signoff (glass-TGV PDK)

| Tool | Method + Path | Public | Notes |
|------|--------------|--------|-------|
| `chipletos_predict_impedance` | `POST /v1/glass-pdk/cheapest-50ohm` | yes | Public-demo proxy; routes through cheapest-50ohm sweep. For single-point precise prediction with CI, use the API-key-gated `/v1/glass-pdk/predict-impedance` directly. |
| `chipletos_pareto_design` | `POST /v1/glass-pdk/geometry-pareto` | yes | Runs a pure-Python coax-proxy hot path (no BEM in the inner loop); returns 200. |
| `chipletos_inverse_design` | `POST /v1/glass-pdk/geometry-from-target` | yes | Includes optional route-backed signoff and `lab_readiness_score`. |
| `chipletos_cross_solver_matrix` | `GET /v1/glass-pdk/cross-solver-matrix` | yes | Read-only witness; updated on every Genesis cross-solver run. |
| `chipletos_drc_validate` | `POST /v1/glass-pdk/drc-validate` | yes | IPC/SEMI defect codes for each violation. |
| `chipletos_validate_against_measurement` | `POST /v1/glass-pdk/validate-against-measurement` | yes | Honest source_type disclosure (measurement vs HFSS simulation). |
| `chipletos_lab_readiness_score` | `POST /v1/glass-pdk/geometry-from-target` (field extract) | yes | Extracts the composite 0-100 score block; verdict bands send_to_lab / send_with_extra_qc / hold / reject. |
| `chipletos_search_s2p_library` | `GET /v1/library/s2p` | yes | 2.27M+ asset registry; paginated. |
| `chipletos_generate_coupon` | `POST /v1/coupons/export-fab` | NO — API key | Coupon bundles include 12-layer stack-up + SOW + cost; gated for security. |

## Photonic Signoff (alpha)

Sub-brand under ChipletOS for photonic IC design + signoff (Marvell SiPh,
Intel Foundry SiPh, NVIDIA optical, Broadcom, Acacia). Sister to glass_pdk
for chiplet packaging. a recent release/51 alpha — waveguide primitive shipped;
MZI / MMI / ring / grating / photonic-crystal queued S52-S55. See Genesis
CLAUDE.md::C39 for the sub-brand plan.

| Tool | Method + Path | Public | Notes |
|------|--------------|--------|-------|
| `chipletos_predict_waveguide_mode` | `POST /v1/photonics/predict-waveguide-mode` | yes | Returns Neff, ng, propagation_loss_dB_cm, bend_loss_dB_per_90. TMM analytical (5-15% rel-err vs Meep); surrogate v1 lands S50 day 14. Envelope: width 200-1500 nm, height 180-400 nm, λ 1260-1670 nm, material Si or SiN. |
| `chipletos_photonic_signoff_health` | `GET /v1/photonics/signoff-health` | yes | Capability inventory — supported primitives + alpha/queued status, solver-stack availability (Meep / TMM / gprMax planned), surrogate training status, audit gate roster (G18-G22). Use for capability discovery before kicking off a session. |
| `chipletos_photonic_drc` | `POST /v1/photonics/drc-photonic` | yes | AIM Photonics-class rule set: min feature 80 nm, min spacing 100 nm, min bend radius per mode-class, max width for single-mode. Geometry dict shape is primitive-dependent (waveguide / ring / grating / etc.); override individual rules via `design_rules`. |
| `chipletos_photonic_validate_ieee` | `POST /v1/photonics/validate-against-ieee` | yes | Cross-check TMM solver against 5 published Si-photonic Neff references: Bogaerts 2018 (JLT), Pavanello 2020 (IEEE Photonics J.), Lim 2014 (JSTQE), Selvaraja 2010 (JLT), Xu 2017 (Opt. Lett.). Returns per-paper relative error + pooled MAE + 10%-threshold PASS/FAIL. |

## "Public" column

- **yes** — in Modal's `DEMO_PUBLIC_POSTS` (for POST) or the equivalent
  read-only allowlist (for GET). Anyone can call without an API key.
  Per-IP rate-limited to ~30 req/min.
- **NO — API key** — gated by `X-API-Key` header. Set `CHIPLETOS_API_KEY`
  in the MCP server env.

## Per-tool schema details

Each tool's input schema is encoded as JSON Schema and served to the LLM
via the MCP `list_tools` response. To inspect:

```python
import asyncio
from chipletos_mcp.tools import ALL_TOOLS

for t in ALL_TOOLS:
    print(t.tool_name, "→", t.input_schema)
```

## Honest framing surfaced in tool responses

The Genesis API attaches `honest_caveat`, `_chipletos_mcp_note`, or
`notes` fields to most responses. These exist because the production
posture is "no fabricated proxy values" (a recent release Chunk 4b). The MCP
server passes them through verbatim; encourage the agent to surface them
to the user when verdicts are partial or OOD.
