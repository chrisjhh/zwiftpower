from .rider import RiderStatsRequest, JSONRiderStats

def getRiderStats():
    rs = RiderStatsRequest()
    data = rs.get()
    return RiderStats(data)

class RiderStats:

    def __init__(self, data: JSONRiderStats) -> None:
        self.data = data['data']

    def races(self):
        res = [x for x in self.data if "TYPE_RACE" in x["f_t"]]
        res.sort(key = lambda x : x["event_date"])
        res.reverse()
        return res
    
if __name__ == "__main__":
    from datetime import datetime
    from .RaceStats import getRaceStats
    stats = getRiderStats()
    res = stats.races()
    for r in res:
        dt = datetime.fromtimestamp(r["event_date"])
        date = dt.strftime("%d/%m/%y")
        before = float(r["skill_b"])
        if before == 0:
            before = 600
        zid = r["zid"]
        cat = r["category"]
        rstats = getRaceStats(zid)
        num = rstats.numberOfRiders(cat)
        pos = "{}/{}".format(r["position_in_cat"], num)
        print("{} {} ({}) {} {} {} -> {:.2f}".format(date, r["event_title"], cat, r["skill"], pos, zid, before - float(r["skill_gain"])))

