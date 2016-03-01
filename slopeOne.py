

#python3.5  mac osx
#a simple implementation of slope one
#2016.2.1
#manggobada@163.com
'''
collabrative filtering based on slopeone algorithm


'''

import numpy as np

class Slope_One():

    def __init__(self):
        self.diffs={}
        self.freqs={}

    def update(self, data):
        for user,prefs in data.items():
            for item,rating in prefs.items():
                self.freqs.setdefault(item, {})
                self.diffs.setdefault(item, {})
                for item2, rating2 in prefs.items():
                    self.freqs[item].setdefault(item2,0)
                    self.diffs[item].setdefault(item2, 0.0)
                    self.freqs[item][item2] += 1
                    self.diffs[item][item2] += (rating - rating2)
        for item, ratings in self.diffs.items():
            for item2,rating in ratings.items():
                ratings[item2] /= self.freqs[item][item2]

    def predict(self, userprefs):
        preds={}
        freqs={}
        for item,rating in userprefs.items():
            for diffitem,diffratings in self.diffs.items():
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)
                freqs[diffitem] += freq
        result=[]
        for item,value in preds.items():
            if item not in userprefs and freqs[item]>0:
                result.append((item,value/freqs[item]))
        #result=[(item,value/freqs[item]) for item,value in preds.items if item not in userprefs and freqs[item]>0]
        result=dict(result)
        return result
