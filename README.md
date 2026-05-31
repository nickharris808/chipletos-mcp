# chipletos-mcp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP-compatible](https://img.shields.io/badge/MCP-compatible-success)](https://modelcontextprotocol.io)

**Drive the ChipletOS chiplet-packaging signoff platform from Claude, Cursor, or any MCP-compatible agent.**

Thirty seconds: this is a [Model Context Protocol](https://modelcontextprotocol.io) server that wraps the public ChipletOS / Genesis HTTPS API (`https://nickharris808--genesis-api-fastapi-app.modal.run`) as fourteen tools an LLM can call directly — impedance prediction, Pareto inverse design, DRC validation, fab-coupon generation, literature cross-check, S-parameter library search, silicon-photonic waveguide design, and more.

```bash
pip install chipletos-mcp
```

## Quickstart (Claude Desktop)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "chipletos": {
      "command": "chipletos-mcp",
      "env": {
        "CHIPLETOS_API_URL": "https://nickharris808--genesis-api-fastapi-app.modal.run"
      }
    }
  }
}
```

Restart Claude Desktop and ask:

> *"I need a 50Ω glass-TGV at 28 GHz on Eagle XG. What dimensions?"*

Claude will call `chipletos_inverse_design` and return the recommended diameter / pitch / thickness with surrogate Z₀, confidence interval, and OOD flag.

See [`examples/`](examples/) for 18 worked agent prompts and [`docs/INSTALL.md`](docs/INSTALL.md) for Cursor / GPT setup.

## The 14 tools

### Chiplet packaging signoff (glass-TGV PDK)

| Tool | Wraps | What it does |
|------|-------|--------------|
| `chipletos_predict_impedance` | `POST /v1/glass-pdk/cheapest-50ohm` (public proxy) | Predict Z₀ for a given TGV geometry across glasses. |
| `chipletos_pareto_design` | `POST /v1/glass-pdk/geometry-pareto` | Multi-objective Pareto inverse design across {Z₀, loss, crosstalk, yield}. |
| `chipletos_inverse_design` | `POST /v1/glass-pdk/geometry-from-target` | Differentiable-surrogate inverse design: target Z₀ → geometry. |
| `chipletos_cross_solver_matrix` | `GET /v1/glass-pdk/cross-solver-matrix` | 100-geometry BEM vs Palace vs OpenEMS vs gprMax disagreement witness. |
| `chipletos_drc_validate` | `POST /v1/glass-pdk/drc-validate` | Glass-interposer DRC (IPC/SEMI defect codes). |
| `chipletos_validate_against_measurement` | `POST /v1/glass-pdk/validate-against-measurement` | Surrogate vs literature/measurement cross-check. |
| `chipletos_lab_readiness_score` | `POST /v1/glass-pdk/geometry-from-target` (field extract) | Composite 0–100 lab-readiness score with verdict bands. |
| `chipletos_search_s2p_library` | `GET /v1/library/s2p` | Search 2.27M+ validated Touchstone S2P files. |
| `chipletos_search_defects` | `GET /v1/defects/search` | Search the 33-type IPC/SEMI/ISO defect taxonomy. |
| `chipletos_generate_coupon` | `POST /v1/coupons/export-fab` (API-key gated) | Fab-ready coupon bundle: DRC + stack-up + SOW + cost. |

### Photonic Signoff (alpha)

Sister sub-brand to glass-TGV PDK — silicon-photonic IC design for Marvell SiPh, Intel Foundry, NVIDIA optical, Broadcom, Acacia. Current release: 5 of 6 photonic primitive surrogates (MZI, MMI, ring, grating, photonic crystal) trained on Genesis local FDFD/BPM truth (test R² ≥ 0.99, Gate 18 PASS) with per-prediction 95% conformal CI; waveguide on TMM Marcatili-Hocker analytical fallback (FDFD 50nm-mesh R²=0.93 ceiling). Meep-grade retrain is on the roadmap. See Genesis CLAUDE.md::C39 for the sub-brand plan.

| Tool | Wraps | What it does |
|------|-------|--------------|
| `chipletos_predict_waveguide_mode` | `POST /v1/photonics/predict-waveguide-mode` | Predict Neff, ng, propagation loss, bend loss for a Si or SiN strip waveguide (TMM analytical). |
| `chipletos_photonic_signoff_health` | `GET /v1/photonics/signoff-health` | Capability inventory — primitives, solver stack (Meep / TMM / gprMax), audit gates G18-G22. |
| `chipletos_photonic_drc` | `POST /v1/photonics/drc-photonic` | AIM Photonics-class DRC: min feature 80 nm, min spacing 100 nm, min bend radius per mode-class. |
| `chipletos_photonic_validate_ieee` | `POST /v1/photonics/validate-against-ieee` | Cross-check TMM solver vs 5 IEEE references (Bogaerts 2018, Pavanello 2020, Lim 2014, Selvaraja 2010, Xu 2017). |

Some routes (predict-impedance, export-fab) require an API key issued by the ChipletOS dashboard. The MCP server passes `X-API-Key` from the `CHIPLETOS_API_KEY` env var when set. All photonic routes currently remain public.

## Links

- ChipletOS website: [chipletos.com](https://chipletos.com)
- Live API docs: <https://nickharris808--genesis-api-fastapi-app.modal.run/docs>
- Issues: <https://github.com/nickharris808/chipletos-mcp/issues>

## License

MIT © 2026 Nicholas Harris / ChipletOS
