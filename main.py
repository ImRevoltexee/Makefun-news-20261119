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


def jpeg_dims(path):
    """Read width/height from a JPEG SOF0/SOF2 segment (stdlib only)."""
    with open(path, "rb") as fh:
        data = fh.read(1 << 20)
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    n = len(data)
    while i + 1 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0x00, 0xFF):
            i += 2
            continue
        if marker == 0xD9:  # EOI: no SOF found
            return None
        if marker in (0xC0, 0xC2):  # SOF0 / SOF2
            if i + 9 > n:
                return None
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker == 0xDA:  # SOS: scan data follows, SOF is before it
            return None
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2  # standalone marker, no length field
            continue
        if i + 4 > n:
            return None
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        if seg_len < 2:
            return None
        i += 2 + seg_len
    return None


def image_dims(path):
    """Width/height of a PNG or JPEG image, else None (stdlib only)."""
    dims = png_dims(path)
    if dims is not None:
        return dims
    return jpeg_dims(path)


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
    dims = image_dims(src)
    if dims is None:
        raise ValueError("entry.png is not a PNG or JPEG file")
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
