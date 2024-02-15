from .jsonrequest import JsonRequest

class RaceStats(JsonRequest):

    def __init__(self, zid: int):
        super().__init__("/results/{}_view.json".format(zid))
        self.zid = zid
        # Races are historic data that never change so always use cache
        self.useCachedResult = True

if __name__ == "__main__":
    rs = RaceStats(4152904)
    data = rs.get()
    print(data)
    print(rs.cacheDate())