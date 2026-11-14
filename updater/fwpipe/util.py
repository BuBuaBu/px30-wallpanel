"""Small helpers shared by the fwpipe modules."""
import hashlib, json, os, re, subprocess, sys, time


def log(msg):
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {msg}', flush=True)


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def text_hash(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p if isinstance(p, bytes) else str(p).encode())
        h.update(b"\0")
    return h.hexdigest()


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def version_key(v):
    """'9.1.1.1' / 'v4.5.1' / 'gsdk-4.4.6' -> tuple of ints (empty when none)."""
    return tuple(int(p) for p in re.findall(r"\d+", str(v or "")))


def version_code(version, revision=1):
    """One integer that orders builds: the first four numbers of the version
    (major * 10^9 + minor * 10^6 + patch * 10^3 + special), times 100, plus the
    revision. 9.1.1.1 -> 900100100100 + 1; 7.5.1.0-r2 -> 700500100000 + 2.
    Fits a JSON number and an int64. A client computes the same code for the
    version the radio reports (revision 1 when it has no -rN; the radio only
    reports the stack version, so a revision of it is not a downgrade) and
    offers a build only when its code is higher."""
    first, *rest = (list(version_key(version)) + [0, 0, 0, 0])[:4]
    code = first                      # unbounded: 2026.6.1 still sorts right
    for p in rest:
        code = code * 1000 + min(p, 999)
    return code * 100 + min(int(revision or 0), 99)


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9._+-]+", "_", str(s)).strip("_")


def run(argv, cwd=None, check=True, capture=False, env=None, timeout=None, quiet=False):
    """Run a command; the argv is logged with secrets (Authorization headers) masked."""
    if not quiet:
        shown = " ".join(re.sub(r"(Authorization: \w+ )\S+", r"\1***", a) for a in argv)
        log(f"$ {shown}")
    r = subprocess.run(argv, cwd=cwd, env=env, timeout=timeout, text=True,
                       stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.STDOUT if capture else None)
    if check and r.returncode != 0:
        tail = (r.stdout or "")[-2000:] if capture else ""
        raise RuntimeError(f"{argv[0]} {argv[1] if len(argv) > 1 else ''} failed (rc {r.returncode})"
                           + (f":\n{tail}" if tail else ""))
    return r


def die(msg, rc=1):
    print(f"fwpipe: {msg}", file=sys.stderr)
    sys.exit(rc)
