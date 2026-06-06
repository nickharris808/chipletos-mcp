# Example prompts

Each file under [`examples/`](../examples/) is a self-contained worked
example: user prompt, the tool the agent should call, suggested arguments,
and what the agent should learn.

| # | Title | Primary tool |
|---|-------|--------------|
| 01 | Predict 50 Ω geometry on Eagle XG @ 28 GHz | `chipletos_inverse_design` |
| 02 | HBM4 channel inverse design | `chipletos_inverse_design` |
| 03 | Pareto explore a diff-pair design | `chipletos_pareto_design` |
| 04 | DRC validation of an aggressive tight-pitch geometry | `chipletos_drc_validate` |
| 05 | Cross-check surrogate vs Sukumaran 2014 | `chipletos_validate_against_measurement` |
| 06 | Multi-solver disagreement triage | `chipletos_cross_solver_matrix` |
| 07 | Find a similar S2P in the library | `chipletos_search_s2p_library` |
| 09 | Generate an Amkor fab coupon bundle | `chipletos_generate_coupon` |
| 10 | Score lab readiness for tape-out | `chipletos_lab_readiness_score` |
| 11 | Full signoff pipeline (predict → DRC → coupon) | (3 tools chained) |
| 12 | UCIe-Advanced link design | `chipletos_inverse_design` + `chipletos_pareto_design` |
| 13 | 77 GHz automotive radar TGV | `chipletos_inverse_design` |
| 14 | Ultra-low-loss substrate exploration | `chipletos_predict_impedance` |
| 15 | Compare Eagle XG vs AF32 vs Borofloat33 | `chipletos_predict_impedance` + others |
| 16 | Photonic waveguide design @ 1550 nm | `chipletos_predict_waveguide_mode` |
| 17 | Photonic DRC pre-tape-out | `chipletos_photonic_drc` |
| 18 | Photonic solver validation vs IEEE refs | `chipletos_photonic_validate_ieee` + `chipletos_photonic_signoff_health` |

## Suggested onboarding path

If you're new to ChipletOS MCP, walk through them in this order:

1. **01** — single-tool happy path; verify install
2. **04** — single-tool DRC; verify response shape
3. **11** — chained pipeline; verify the agent can stitch tools
4. **10** — composite verdict; understand the lab-readiness band
5. **05** — surrogate vs literature; understand the truth hierarchy
6. **15** — comparison query; show off the agent's reasoning

The rest demonstrate specialty use cases (HBM4, UCIe, mmWave, multi-objective
exploration).
