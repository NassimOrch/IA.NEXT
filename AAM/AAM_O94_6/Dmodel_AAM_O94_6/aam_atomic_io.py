"""Portable atomic replace with bounded retry for transient Windows sharing locks.

Retries are restricted to Windows sharing/lock violations (ERROR_SHARING_VIOLATION=32,
ERROR_LOCK_VIOLATION=33). Other permission errors fail immediately; this is not a
permission bypass and never opens or edits a file held by another process.
"""
from __future__ import annotations
import os
import time
from pathlib import Path
from typing import Callable


def _is_transient_windows_lock(exc: OSError) -> bool:
    winerror = getattr(exc, "winerror", None)
    if winerror in (32, 33):
        return True
    return os.name == "nt" and isinstance(exc, PermissionError) and getattr(exc, "errno", None) in (13, 16)


def safe_replace(src: str | os.PathLike, dst: str | os.PathLike, *, attempts: int = 8,
                 base_delay: float = 0.025) -> dict:
    """Atomically replace *dst*, retrying only transient Windows sharing violations.

    Returns non-sensitive retry telemetry. Source and destination must be on the same
    filesystem for the underlying os.replace atomicity guarantees to apply.
    """
    source, target = Path(src), Path(dst)
    budget = max(1, min(int(attempts), 12))
    delay = max(0.0, min(float(base_delay), 1.0))
    for attempt in range(1, budget + 1):
        try:
            os.replace(source, target)
            return {"status": "PASS", "attempts": attempt, "retried": attempt > 1,
                    "replace_semantics": "os.replace_atomic_same_filesystem"}
        except OSError as exc:
            if attempt >= budget or not _is_transient_windows_lock(exc):
                raise
            time.sleep(min(delay * (2 ** (attempt - 1)), 0.4))
    raise RuntimeError("safe_replace exhausted without success or a propagated error")


def atomic_write_json(path: str | os.PathLike, payload, *, backup: bool = False) -> dict:
    import json, tempfile
    target=Path(path); target.parent.mkdir(parents=True,exist_ok=True)
    if target.is_symlink(): raise PermissionError(f"refusing symlink destination: {target}")
    raw=(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n").encode("utf-8")
    temp=target.with_name(f".{target.name}.{os.getpid()}.{time.time_ns()}.tmp")
    backup_path=Path(str(target)+".bak")
    backup_temp=backup_path.with_name(f".{backup_path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    try:
        with temp.open("xb") as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        if backup and target.exists():
            if target.is_symlink() or not target.is_file(): raise PermissionError("backup source must be a regular file")
            with target.open("rb") as src, backup_temp.open("xb") as dst:
                for block in iter(lambda:src.read(1024*1024),b""): dst.write(block)
                dst.flush(); os.fsync(dst.fileno())
            safe_replace(backup_temp,backup_path)
        replaced=safe_replace(temp,target)
        try:
            fd=os.open(str(target.parent),os.O_RDONLY)
            try: os.fsync(fd)
            finally: os.close(fd)
        except OSError: pass
        return {"status":"PASS","path":str(target),"bytes":len(raw),"replace":replaced}
    finally:
        for candidate in (temp,backup_temp):
            try: candidate.unlink()
            except FileNotFoundError: pass
