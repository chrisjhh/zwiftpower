from .race import JSONRaceStats, RaceStatsRequest
from .rider import getZwid

def getRaceStats(zid: int):
    rs = RaceStatsRequest(zid)
    data = rs.get()
    return RaceStats(data)

class RaceStats:

    def __init__(self, data: JSONRaceStats) -> None:
        self.data = data["data"]
        self.zwid = getZwid()

    def categories(self):
        cats = set([x["category"] for x in self.data])
        res = list(cats)
        res.sort()
        return res
    
    def myCategory(self):
        r = self._riderResult(self.zwid)
        if r is not None:
            return r["category"]
        return None
    
    def myCategoryPosition(self):
        r = self._riderResult(self.zwid)
        if r is not None:
            return r["position_in_cat"]
        return None
    
    def myScore(self):
        r = self._riderResult(self.zwid)
        if r is not None:
            return r["skill"]
        return None
    
    def _riderResult(self, zid: int):
        res = [x for x in self.data if x["zwid"] == int(zid)]
        if len(res) == 1:
            return res[0]
        return None
    
    def numberOfRiders(self, cat=None):
        if cat is None:
            return len(self.data)
        return len([x for x in self.data if x["category"] == cat])
    
    def quality(self, cat=None):
        if cat is None:
            finishers = self.data
        else:
            finishers = [x for x in self.data if x["category"] == cat]
        if len(finishers) < 10:
            top10 = finishers
        else: 
            top10 = finishers[0:10]
        scores = [float(x["skill_b"]) for x in top10 if float(x["skill_b"]) != 0.0]
        scores.sort()
        if len(scores) < 5:
            return 0
        best5 = scores[0:5]
        av = sum(best5) / 5.0
        qual = 0.9 * av
        return qual
    
    def averageScore(self, cat=None):
        if cat is None:
            finishers = self.data
        else:
            finishers = [x for x in self.data if x["category"] == cat]
        scores = [float(x["skill_b"]) for x in finishers if float(x["skill_b"]) != 0.0]
        return sum(scores) / len(scores)
    
    def pointsPerPlace(self, cat=None):
        if cat is None:
            finishers = self.data
        else:
            finishers = [x for x in self.data if x["category"] == cat]
        num = len(finishers)
        if num < 2:
            return 0
        qual = self.quality(cat)
        if qual == 0:
            return 0
        avg = self.averageScore(cat)
        if avg < qual:
            qual = 0.9 * avg
        return (avg - qual) * 2 / (num - 1)
    
    def scoreForFinisher(self, pos:int, cat=None):
        qual = self.quality(cat)
        if qual == 0:
            return 0
        ppp = self.pointsPerPlace(cat)
        if pos < 1:
            raise Exception("Position must be 1 or greater")
        return qual + (pos - 1) * ppp
    
if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) > 0:
        zid = args[0]
    else:
        from .RiderStats import getRiderStats
        rs = getRiderStats()
        races = rs.races()
        zid = races[0].zid
    stats = getRaceStats(zid)
    print("Categories: {}".format(stats.categories()))
    myCat = stats.myCategory()
    print("My Category: {}".format(myCat))
    print("Num riders: {} {} Category: {}".format(stats.numberOfRiders(), myCat, stats.numberOfRiders(myCat)))
    print("Quality of {} race: {:.2f}".format(myCat, stats.quality(myCat)))
    print("Average score of {} race: {:.2f}".format(myCat, stats.averageScore(myCat)))
    print("Points per place of {} race: {:.2f}".format(myCat, stats.pointsPerPlace(myCat)))
    myPos = stats.myCategoryPosition()
    print("My Position in {} race: {}".format(myCat, myPos))
    score = stats.scoreForFinisher(myPos, myCat)
    print("Score for {} place = {:.2f}".format(myPos, score))
    print("My score for this race: {}".format(stats.myScore()))
