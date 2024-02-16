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

class RaceStats(JsonRequest):

    def __init__(self, zid: int):
        super().__init__("/results/{}_view.json".format(zid))
        self.zid = zid
        # Races are historic data that never change so always use cache
        self.useCachedResult = True

    def get(self, params=None) -> JSONRaceStats:
        return super().get(params)

if __name__ == "__main__":
    rs = RaceStats(4152904)
    data = rs.get()
    print(data)
    print(rs.cacheDate())