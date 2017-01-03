#MAC OS X  Python3.5
#2016.1.15
#mangobada@163.com

'''
apply of kNN(k nearst neighbor)

'''
import operator
import os
import numpy as np
import kNN
import pymongo

#
def createDataSet():
	group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels=['A','A','B','B']
	return group,labels

def datingClassTest():
    testTrainRatio=0.1
    datingMat,labels=file2matrix('datingTestSet2.txt')
    normDataSet,ranges,minValue=autoNorm(datingMat)
    m=normDataSet.shape[0]
    numOfTest=int(m*testTrainRatio)
    errorCount=0.0
    for i in range(numOfTest):
        #choose the first 10% as test example, others as trainning dataset
        result=classify0(normDataSet[i,:],normDataSet[numOfTest:m,:],labels[numOfTest:m],3)
        print("the classifier come with %d, the real answer is %d" %(int(result),int(labels[i])))
        if int(result)!=int(labels[i]):
            errorCount+=1.0
    print(errorCount)
    errorRate=errorCount/numOfTest
    print("the error rate is %f" %errorRate)

#classify a new person input by user
def classifyPerson():
    resultList = ['not at all','in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games?")) 
    ffMiles = float(input("frequent flier miles earned per year?")) 
    iceCream = float(input("liters of ice cream consumed per year?")) 
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt') 
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = np.array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("You will probably like this person: ",resultList[int(classifierResult) - 1])

def image2Vec(filename):
    resultVec=np.zeros((1,1024))
    fr=open(filename,'r')
    
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            resultVec[0,32*i+j]=lineStr[j]
    fr.close()
    return resultVec

def handwritingClassTest():
    hwLabels = []
    trainingFileList = os.listdir('trainingDigits') 
    m = len(trainingFileList)
    trainingMat = np.zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = image2Vec('trainingDigits/%s'  %fileNameStr)
    testFileList = os.listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = image2Vec('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d"% (classifierResult, classNumStr))
        if (classifierResult != classNumStr):
            errorCount += 1.0
        print("\nthe total number of errors is: %d" % errorCount)
        print("\nthe total error rate is: %f" % (errorCount/float(mTest)))

