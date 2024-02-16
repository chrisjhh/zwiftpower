import os.path

_cacheDir: str = None

def cacheDir():
    global _cacheDir
    if _cacheDir is None:
        home = os.path.expanduser("~")
        _cacheDir = os.path.join(home, ".zwiftpower")
    return _cacheDir