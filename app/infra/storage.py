from __future__ import annotations

import json
import mimetypes
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path("data")
BLOB_DIR = DATA_DIR / "blobs"
INDEX_PATH = DATA_DIR / "index.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
BLOB_DIR.mkdir(parents=True, exist_ok=True)


# super simple "db": a json dict {id: record}
def _load_index() -> dict:
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text("utf-8"))


def _save_index(idx: dict) -> None:
    tmp = INDEX_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(idx, indent=2, sort_keys=True), "utf-8")
    os.replace(tmp, INDEX_PATH)


def new_id() -> str:
    # short-ish, URL-safe
    return uuid4().hex[:10]


@dataclass
class BlobRecord:
    id: str
    original_name: str
    stored_name: str
    bytes: int
    content_type: str


def save_bytes(
    filename: str, content: bytes, content_type: str | None = None
) -> BlobRecord:
    blob_id = new_id()
    suffix = Path(filename).suffix if filename else ""
    stored_name = f"{blob_id}{suffix}"
    dest = BLOB_DIR / stored_name
    dest.write_bytes(content)

    ct = (
        content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    )  # noqa: E501

    rec = BlobRecord(
        id=blob_id,
        original_name=filename or stored_name,
        stored_name=stored_name,
        bytes=len(content),
        content_type=ct,
    )

    idx = _load_index()
    idx[blob_id] = asdict(rec)
    _save_index(idx)

    return rec


def get_record(blob_id: str) -> BlobRecord | None:
    idx = _load_index()
    rec = idx.get(blob_id)
    if not rec:
        return None
    return BlobRecord(**rec)


def get_path(rec: BlobRecord) -> Path:
    return BLOB_DIR / rec.stored_name
