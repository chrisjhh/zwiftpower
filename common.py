import os.path

_cacheDir: str = None
_userDir: str = None

def userDir():
    global _userDir
    if _userDir is None:
        home = os.path.expanduser("~")
        _userDir = os.path.join(home, ".zwiftpower")
    return _userDir

def cacheDir():
    global _cacheDir
    if _cacheDir is None:
        _cacheDir = os.path.join(userDir(), "cache")
    return _cacheDir

def makeUserDir():
    dir = userDir()
    if not os.path.isdir(dir):
        os.mkdir(dir)

def makeCacheDir():
    makeUserDir()
    dir = cacheDir()
    if not os.path.isdir(dir):
        os.mkdir(dir)