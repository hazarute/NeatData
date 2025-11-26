from pathlib import Path
import uuid
from typing import Optional
from fastapi import UploadFile


BASE_UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads"


def ensure_uploads_dir() -> Path:
    """Ensure the uploads directory exists and return its Path."""
    BASE_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return BASE_UPLOADS_DIR


async def save_upload_file(file: UploadFile) -> str:
    """Save an incoming `UploadFile` to disk with a UUID name.

    Returns the absolute path to the saved file as a string.
    """
    uploads_dir = ensure_uploads_dir()
    suffix = Path(file.filename).suffix or ""
    filename = f"{uuid.uuid4().hex}{suffix}"
    dest = uploads_dir / filename

    # stream write to avoid loading whole file into memory
    with dest.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            buffer.write(chunk)

    return str(dest)


def get_uploads_dir() -> str:
    """Return uploads dir path as string."""
    return str(ensure_uploads_dir())
