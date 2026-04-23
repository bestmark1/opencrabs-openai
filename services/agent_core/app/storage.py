import json
from datetime import datetime, timezone
from pathlib import Path

from services.agent_core.app.contracts import ParserRun


ARTIFACTS_ROOT = Path("artifacts/parses")


def build_parser_artifact_path(*, peer: str, source_kind: str) -> Path:
    safe_peer = peer.strip().replace("@", "").replace("/", "_") or "unknown"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return ARTIFACTS_ROOT / f"{stamp}-{safe_peer}-{source_kind}.json"


def save_parser_run(run: ParserRun) -> str:
    path = build_parser_artifact_path(
        peer=run.source.peer,
        source_kind=run.source.source_kind,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(run.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
