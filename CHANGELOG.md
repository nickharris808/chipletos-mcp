# Changelog

All notable changes to `chipletos-mcp` are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [0.2.0] — 2026-05-31

### Changed
- Tool docs refreshed to reflect current capabilities: inverse design returns a calibrated
  pass-probability + named dominant risk + honest reachability; the multi-fidelity sim-to-real
  calibration and the measured-truth / pre-registered-prediction posture are surfaced.
- Corrected a stale note on `chipletos_pareto_design`: the historical LAPACK SIGSEGV is fixed
  (pure-Python coax-proxy hot path; the route returns 200).
- Version-neutral wording throughout (no internal release-cadence labels).

All tools remain thin clients over the gated `/v1` API — no solver, corpus, or weights ship here.

## [0.1.0] — 2026-05-26

Initial public release.

### Added
- 15 MCP tools over the audited ChipletOS `/v1` API:
  - **Chiplet glass-TGV signoff (10):** predict_impedance, pareto_design, inverse_design,
    cross_solver_matrix, drc_validate, validate_against_measurement, lab_readiness_score,
    search_s2p_library, search_defects, generate_coupon.
  - **ChipletOS Photonic Signoff, alpha (4):** predict_waveguide_mode, photonic_signoff_health,
    photonic_drc, photonic_validate_ieee.
  - **Open benchmark (1):** leaderboard — the public Glass-TGV Z₀ signoff benchmark standings.
- Claude.ai skills packs (glass_tgv_designer, pareto_explorer, chiplet_signoff_assistant).
- respx-mocked smoke tests for all 15 tools.

### Honest disclosure
- The surrogate headline (R²=0.9999966) is **surrogate-vs-BEM**, NOT VNA-measured.
  The open benchmark publishes a **public-glass subset** (5 of 25 corpus glasses) with the
  number recomputed on that public split. See the benchmark README + the ChipletOS trust page.
- 13/15 tools hit public demo endpoints; `generate_coupon` requires `CHIPLETOS_API_KEY`.
