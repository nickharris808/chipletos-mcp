# Contributing

## Adding a new tool wrapper

ChipletOS adds new public routes regularly. To wrap one as a new MCP tool:

1. **Create the tool module** under `src/chipletos_mcp/tools/`. Copy an
   existing one (e.g. `drc_validate.py`) and edit:

   - `INPUT_SCHEMA` — JSON Schema for the input. Mirror the FastAPI
     pydantic model in the Genesis router; include `minimum` / `maximum`
     bounds so the LLM gets validation feedback before the call.
   - `async def _run(client, args)` — call `client.get(...)` or
     `client.post(...)`. Don't transform the response unless absolutely
     necessary; the agent benefits from raw witness data.
   - `TOOL = ChipletosTool(...)` — name, description (1–2 sentences,
     LLM-friendly), input_schema, run.

2. **Register it** in `src/chipletos_mcp/tools/__init__.py`:

   - Add `from .my_new_tool import TOOL as my_new_tool` to the imports.
   - Append it to `ALL_TOOLS`.

3. **Write an example** under `examples/NN_your_use_case.md` and link from
   `docs/EXAMPLES.md`.

4. **Write a test** in `tests/test_tools.py` — at minimum, schema validity
   and a mocked-response happy path.

5. **Bump the version** in `src/chipletos_mcp/__init__.py` and
   `pyproject.toml`.

## Tool description style

Keep it to **1-2 sentences** explaining when an LLM should pick this tool
over the others. Start with a verb. Examples:

- Good: "Run glass-interposer DRC on a list of TGV geometries. Returns
  per-violation entries with IPC/SEMI defect codes."
- Bad: "This tool wraps the DRC route on the Genesis API. It takes via
  geometries as input." (too implementation-focused)

## Testing

```bash
pip install -e ".[dev]"
pytest -q
```

Tests use `respx` to mock httpx; no live Genesis API calls in CI.

## Releasing

(Operator handles this — do not bump versions / cut tags without coordination.)

1. Update `__version__` in `src/chipletos_mcp/__init__.py`
2. Update `version` in `pyproject.toml` and `manifest.json`
3. Tag: `git tag v0.X.Y`
4. Push: `git push --tags`
5. Operator runs `python -m build && twine upload dist/*`

## Repo layout reminder

- This repo is the **MCP server**. The physics engine lives in the
  private `genesis` monorepo and is exposed via the public Modal API.
- Never embed physics code here — it would defeat the "tiny shim"
  architecture and make the security posture leaky.
