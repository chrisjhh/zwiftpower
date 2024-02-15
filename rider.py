from .jsonrequest import JsonRequest
import os.path

class NoZwidFile(Exception):
    def __str__(self) -> str:
        return """
------------------------------------------------------------------------------------------------------------------
File zwid.txt not found
zwid.txt should contain the ZwiftPower id for the user and live in the root directory of this module
To get the zwid, vist zwiftpower.com in a browser and select "Profile". The zwid will be the z= param of the url
------------------------------------------------------------------------------------------------------------------
"""

_zwid: str = None

def getZwid():
    global _zwid
    if _zwid is None:
        thisDir = os.path.dirname(__file__)
        zwidFile = os.path.join(thisDir, "zwid.txt")
        try:
            with open(zwidFile) as fh:
                _zwid = fh.read()
        except FileNotFoundError:
            raise NoZwidFile
    return _zwid

class RiderStats(JsonRequest):

    def __init__(self, zwid=None, timestamp=None):
        if zwid is None:
            zwid = getZwid()
        super().__init__("/profile/{}_all.json".format(zwid))
        self.zwid = zwid
        self.timestamp = timestamp
        if timestamp is not None:
            self.useCachedResult = True

    def hasCache(self):
        if not super().hasCache():
            return False
        if self.timestamp is not None and self.cacheDate() < self.timestamp:
            # We have a cache but it is out of date
            # Return false so it is refreshed
            return False
        return True 

if __name__ == "__main__":
    rs = RiderStats(timestamp=1707984600)
    data = rs.get()
    print(data)
    print(rs.cacheDate())