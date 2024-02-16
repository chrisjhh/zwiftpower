import requests
import os.path
import json

from .common import userDir, cacheDir, makeCacheDir

class BadResponse(Exception):
    pass

class NoCookie(Exception):
    def __str__(self) -> str:
        return """
------------------------------------------------------------------------------------------------------------------
File Cookie.txt not found
Cookie.txt should contain the authentication cookie set by ZwiftPower and live in the ~/.zwiftpower directory
To get the cookie, use a Browser to go to zwiftpower.com and use the debug pannel Ctrl-Shift-J, Network, Request Headers
------------------------------------------------------------------------------------------------------------------
"""

_cookie: str = None

def getCookie():
    global _cookie
    if _cookie is None:
        dir = userDir()
        cookieFile = os.path.join(dir, "Cookie.txt")
        try:
            with open(cookieFile) as fh:
                _cookie = fh.read()
        except FileNotFoundError:
            raise NoCookie()
    return _cookie

class JsonRequest:

    base_url = "https://zwiftpower.com/cache3"

    def __init__(self, url):
        self.url = self.base_url + url
        self.cacheResult = True
        self.useCachedResult = False

    def get(self, params=None):
        if self.useCachedResult and self.hasCache():
            return self.loadFromCache()
        cookie = getCookie()
        headers = {
            "Cookie": cookie
        }
        response = requests.get(self.url, headers=headers, params=params)
        if response.status_code != 200:
            raise BadResponse("%s %s %d %s" % (self.url, headers, response.status_code, response.text))
        data = response.json()
        if self.cacheResult:
            self.saveToCache(data)
        return data
    
    def cacheFile(self):
        if not hasattr(self, "_cacheFile"):
            dir = cacheDir()
            filename = os.path.basename(self.url)
            self._cacheFile = os.path.join(dir, filename)
        return self._cacheFile
    
    def saveToCache(self, data):
        dir = cacheDir()
        if not os.path.exists(dir):
            makeCacheDir()
        file = self.cacheFile()
        with open(file, "wb") as fh:
            fh.write(str.encode(json.dumps(data)))

    def loadFromCache(self):
        file = self.cacheFile()
        try:
            with open(file) as fh:
                data = fh.read()
            return json.loads(data)
        except:
            return None
        
    def hasCache(self):
        return os.path.isfile(self.cacheFile())
        
    def cacheDate(self):
        return os.path.getmtime(self.cacheFile())