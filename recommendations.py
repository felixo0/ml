#!/usr/bin/env python3
# _*_encoding=utf-8_*_
#Author@ LogicWang
#A dictionary of movie critics and their rating of a small set of movies


from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def sim_distance(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    if len(si)==0:
        return 0

    sum_of_squares= sum([pow(prefs[person1][item] - prefs[person2][item],2) 
            for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squares)

#return the Pearson correlation coefficient for p1 and p2
#the code was copied from book ,but i wonder Pearson correlation written as
#Cov(x,y)/(s(x)*s(y)) in textbook where s(x) is standard deviation,Cov(x,y) is covariance
def sim_pearson(prefs,p1,p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1

    n=len(si)
    if n==0:
        return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n) * (sum2Sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    return num/den

def sim_pearson2(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1

    n=len(si)
    if n==0:
        return 0

    p1_mean = sum([prefs[p1][it] for it in si])/n
    p2_mean = sum([prefs[p2][it] for it in si])/n

    #standard deviation 
    s_p1 = sqrt(sum([pow(prefs[p1][it]-p1_mean,2) for it in si])/n)
    s_p2 = sqrt(sum([pow(prefs[p2][it]-p2_mean,2) for it in si])/n)
    
    #covariation
    cov_p1p2 = sum([(prefs[p1][it]-p1_mean)*(prefs[p2][it]-p2_mean) for it in si])/n

    return cov_p1p2/(s_p1*s_p2)

#simple matching coefficient
def sim_smc(prefs,p1,p2):
    pass

#jaccard coefficient
def sim_jaccard(prefs,p1,p2):
    pass

#cosine

def sim_cos(prefs,p1,p2):
    pass

#extention jaccard

def sim_ej(prrefs,p1,p2):
    pass


def topMatches(prefs,person, n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other)
            for other in prefs if other!=person]

    scores.sort()
    scores.reverse()
    return scores[0:n]


#gets recommendations for a person by using a weighted average 
#of every other user's rankings

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person:
            continue
        sim=similarity(prefs,person,other)

        if sim<=0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings = [(total/simSums[item],item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()

    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person]=prefs[person][item]

    return result

def calculateSimilarItems(prefs,n=10):
    result={}
    itemPrefs = transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        c+=1
        if c%100==0:
            print("%d / %d" %(c,len(itemPrefs)))
        scores = topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores

    return result

def  getRecommendedItems(prefs,itemMatch,user):
    userRatings = prefs[user]
    scores={}
    totalSim={}

    for (item,rating) in userRatings.items():
        for (similarity,item2) in itemMatch[item]:
            if item2 in userRatings:
                continue
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    rankings=[(scores/totalSim[item],item) for item,scores in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

