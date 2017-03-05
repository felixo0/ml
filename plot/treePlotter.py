
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
def plotNode(ax,nodeTxt, centerPt, parentPt, nodeType):
    ax.annotate(nodeTxt, 
            xy=parentPt,xycoords='axes fraction',
            xytext=centerPt,textcoords='axes fraction',
            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops) 
    plotTree.totalW = float(getNumLeafs(inTree)) 
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0; 
    plotTree(createPlot.ax1,inTree, (0.5,1.0), '')
    plt.show()

def getNumLeafs(inputTree):
    numLeafs=0
    firstKey=list(inputTree.keys())[0]
    secondDict=inputTree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

def getTreeDepth(inputTree):
    maxDepth=0
    firstKey=list(inputTree.keys())[0]
    secondDict=inputTree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            depth=1+getTreeDepth(secondDict[key])
        else:
            depth=1
        if depth>maxDepth:
            maxDepth=depth
    return maxDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},{'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(ax,myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(ax,firstStr, cntrPt, parentPt, decisionNode) 
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD 
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(ax,secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(ax,secondDict[key], (plotTree.xOff, plotTree.yOff),cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

