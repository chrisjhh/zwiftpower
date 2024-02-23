from datetime import datetime
from .rider import RiderStatsRequest, JSONRiderStats, JSONRaceResult

def getRiderStats(timestamp=None):
    rs = RiderStatsRequest(timestamp=timestamp)
    data = rs.get()
    return RiderStats(data)


class RaceResult:

    def __init__(self, data: JSONRaceResult) -> None:
        self.data = data

    @property
    def name(self):
        return self.data["event_title"]
    
    @property
    def timestamp(self):
        return self.data["event_date"]
    
    @property
    def date(self):
        return datetime.fromtimestamp(self.timestamp)
    
    @property
    def category(self):
        return self.data["category"]
    
    @property
    def zid(self):
        return int(self.data["zid"])
    
    @property
    def position(self):
        return self.data["position_in_cat"]
    
    @property
    def overallPosition(self):
        return self.data["pos"]
    
    @property
    def score(self):
        return float(self.data["skill"])
    
    @property
    def ratingBefore(self):
        return float(self.data["skill_b"])
    
    @property
    def skillGain(self):
        return float(self.data["skill_gain"])
    
    @property
    def ratingAfter(self):
        before = self.ratingBefore
        if before == 0:
            before = 600
        return before - self.skillGain

class RiderStats:

    def __init__(self, data: JSONRiderStats) -> None:
        self.data = data['data']

    def races(self):
        res = [x for x in self.data if "TYPE_RACE" in x["f_t"]]
        res.sort(key = lambda x : x["event_date"])
        res.reverse()
        return [RaceResult(r) for r in res]
    
    def findRide(self, timestamp: int):
        for r in self.data:
            ts = r["event_date"]
            if abs(timestamp - ts) < 200:
                return RaceResult(r)
        return None

    
if __name__ == "__main__":
    from .RaceStats import getRaceStats
    stats = getRiderStats()
    res = stats.races()
    for r in res:
        dt = r.date
        date = dt.strftime("%d/%m/%y")
        before = r.ratingBefore
        zid = r.zid
        cat = r.category
        rstats = getRaceStats(zid)
        num = rstats.numberOfRiders(cat)
        pos = "{}/{}".format(r.position, num)
        print("{} {} {} ({}) {} {} {} -> {:.2f}".format(date, r.timestamp,r.name, cat, r.score, pos, zid, r.ratingAfter))

