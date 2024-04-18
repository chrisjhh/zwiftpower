from .jsonrequest import JsonRequest
from typing import TypedDict
from .types.JSONResult import JSONResult


class JSONRiderResult(JSONResult):
    log: int
    lead: int
    sweep: int
    actid: str
    anal: int
    
class JSONRaceStats(TypedDict):
    data: list[JSONRiderResult]

class RaceStatsRequest(JsonRequest):

    def __init__(self, zid: int):
        super().__init__("/results/{}_view.json".format(zid))
        self.zid = zid
        # Races are historic data that never change so always use cache
        self.useCachedResult = True

    def get(self, params=None) -> JSONRaceStats:
        if hasattr(self, "_data"):
            return self._data
        return super().get(params)
    
    def hasCache(self):
        if not super().hasCache():
            return False
        # It's not quite tue that race data never changes if we get the
        # results early before the skill improvements are calculated
        # They will all be zero!
        # In this case treat it as if we don't have a cache!
        data: JSONRaceStats = self.loadFromCache()
        if data is None or not "data" in data:
            return False
        for d in data["data"]:
            if "skill_b" in d and float(d["skill_b"]) > 0.0:
                self._data = data
                return True
        return False

if __name__ == "__main__":
    rs = RaceStatsRequest(4152904)
    data = rs.get()
    print(data)
    print(rs.cacheDate())