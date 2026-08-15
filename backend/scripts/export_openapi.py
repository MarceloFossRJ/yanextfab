"""Writes the FastAPI app's OpenAPI schema to disk without starting a live server.

Used by CI's drift-check: regenerate the schema and diff it against the committed
frontend client's source. Can also be run manually:
`uv run python scripts/export_openapi.py [output_path]` (defaults to `openapi.json`).

During local development, the schema is instead (re-)written automatically by the app's
startup hook on every `uvicorn --reload` restart — see app.main.lifespan. See design.md's
"API client sync mechanism" decision for why there's no separate backend-side watcher.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.main import app, export_openapi_schema  # noqa: E402

if __name__ == "__main__":
    output_path = sys.argv[1] if len(sys.argv) > 1 else "openapi.json"
    written_path = export_openapi_schema(app, output_path)
    print(f"Wrote OpenAPI schema to {written_path}", file=sys.stderr)
