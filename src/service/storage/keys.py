from pathlib import PurePosixPath


class UnsafeStorageKey(ValueError):
    """Raised when a client-supplied filename cannot be used as a storage key."""

    def __init__(self, filename: str):
        super().__init__(f"Unsafe storage key: {filename!r}")
        self.filename = filename


def safe_key(filename: str) -> str:
    """Normalize a client-supplied filename into a safe relative storage key.

    Guards against path traversal: rejects empty names, absolute paths (POSIX or
    Windows drive/UNC), and any key that still contains a '..' segment after
    normalization. Returns a forward-slash relative key usable by every backend.
    """
    if not filename or not filename.strip():
        raise UnsafeStorageKey(filename)

    # Normalize separators so a Windows-style '..\\..' is caught too.
    candidate = filename.replace("\\", "/").strip("/")
    if not candidate:
        raise UnsafeStorageKey(filename)

    pure = PurePosixPath(candidate)
    if pure.is_absolute() or any(part == ".." for part in pure.parts):
        raise UnsafeStorageKey(filename)

    # Reject Windows drive/UNC prefixes (e.g. 'C:/x') that PurePosixPath treats as a name.
    if ":" in pure.parts[0]:
        raise UnsafeStorageKey(filename)

    return pure.as_posix()
