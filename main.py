#!/usr/bin/env python3
"""Entry point for make.fun bounty news-image-20261119.

Copies the entry image (entry.png, next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only,
no network: the same input always produces the same output bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024


def png_dims(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        raise FileNotFoundError("missing entry image: " + src)
    size = os.path.getsize(src)
    if size == 0 or size > MAX_BYTES:
        raise ValueError("entry.png size %d out of range (max %d)"
                         % (size, MAX_BYTES))
    dims = png_dims(src)
    if dims is None:
        raise ValueError("entry.png is not a PNG file")
    if dims[0] > MAX_DIM or dims[1] > MAX_DIM:
        raise ValueError("entry.png dimensions %dx%d exceed %d"
                         % (dims[0], dims[1], MAX_DIM))

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    if sha256(dst) != sha256(src):
        raise ValueError("copied file hash does not match source")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, dims[0], dims[1], size, sha256(dst)[:16]))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - surface any failure loudly
        print("error:", exc, file=sys.stderr)
        raise
