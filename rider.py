from .jsonrequest import JsonRequest
from .common import cacheDir
import os.path
from typing import TypedDict


class NoZwidFile(Exception):
    def __str__(self) -> str:
        return """
------------------------------------------------------------------------------------------------------------------
File zwid.txt not found
zwid.txt should contain the ZwiftPower id for the user and live in the ~/.zwiftpower directory
To get the zwid, vist zwiftpower.com in a browser and select "Profile". The zwid will be the z= param of the url
------------------------------------------------------------------------------------------------------------------
"""

_zwid: str = None

def getZwid():
    global _zwid
    if _zwid is None:
        userDir = cacheDir()
        zwidFile = os.path.join(userDir, "zwid.txt")
        try:
            with open(zwidFile) as fh:
                _zwid = fh.read()
        except FileNotFoundError:
            raise NoZwidFile
    return _zwid

class JSONResult(TypedDict):
    DT_RowId: str
    ftp: str
    friend: int
    pt: str
    label: str
    zid: str
    pos: int
    position_in_cat: int
    name: str
    cp: int
    zwid: int
    res_id: str
    lag: int
    uid: str
    time: list[float]
    time_gun: float
    gap: int
    vtta: str
    vttat: int
    male: int
    tid: str
    topen: str
    tname: str
    tc: str
    tbc: str
    tbd: str
    zeff: int
    category: str
    height: list[float]
    flag: str
    avg_hr: list[int]
    max_hr: list[int]
    hrmax: list[int]
    hrm: int
    weight: list[float]
    power_type: int
    display_pos: int
    src: int
    age: str
    zada: int
    note: str
    div: int
    divw: int
    skill: str
    skill_b: str
    skill_gain: str
    np: list[int]
    hrr: list[float]
    hreff: list[str]
    avg_power: list[int]
    avg_wkg: list[str]
    wkg_ftp: list[str]
    wftp: list[int]
    wkg_guess: int
    wkg1200: list[str]
    wkg300: list[str]
    wkg120: list[str]
    wkg60: list[str]
    wkg30: list[str]
    wkg15: list[str]
    wkg5: list[str]
    w1200: list[str]
    w300: list[str]
    w120: list[str]
    w60: list[str]
    w30: list[str]
    w15: list[str]
    w5: list[str]
    is_guess: int
    upg: int
    penalty: str
    reg: int
    fl: str
    pts: str
    pts_pos: str
    info: int
    info_notes: list[str]
    strike: int
    event_title: str
    f_t: str
    distance: int
    event_date: int
    rt: str
    laps: str
    dur: str
class JSONRiderStats(TypedDict):
    data: list[JSONResult]

class RiderStats(JsonRequest):

    def __init__(self, zwid=None, timestamp=None):
        if zwid is None:
            zwid = getZwid()
        super().__init__("/profile/{}_all.json".format(zwid))
        self.zwid = zwid
        self.timestamp = timestamp
        if timestamp is not None:
            self.useCachedResult = True

    def get(self, params=None) -> JSONRiderStats:
        return super().get(params)

    def hasCache(self):
        if not super().hasCache():
            return False
        if self.timestamp is not None and self.cacheDate() < self.timestamp:
            # We have a cache but it is out of date
            # Return false so it is refreshed
            return False
        return True 

if __name__ == "__main__":
    rs = RiderStats(timestamp=1708074526)
    data = rs.get()
    print(data["data"])
    print(rs.cacheDate())