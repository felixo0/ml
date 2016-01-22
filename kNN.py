#MAC OS X  Python3.5
#2016.1.15
#mangobada@163.com

'''
a simple implement of kNN(k nearst neighbor)

'''
import operator
import os
import numpy as np


#a small dataset to verify the correction of syntax and algorithm
def create_dataset():
	data_matrix=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	class_labels=['A','A','B','B']
	return data_matrix,class_labels

#add code to process text 
def pre_process():
    pass

def train():
    #kNN do not need to train.
    pass

#k nearest neighbor, where input_vec is the data waitting for classify, dataSet is trainning example
# labels is the label of the dataSet ,k is the number of nearest neighbors to voting
def classify(input_vec,dataset,class_labels,k):
    dataset_size = dataset.shape[0]
    #tile is a function in numpy, to make inX has same length with dataSet
    diff_matrix=np.tile(input_vec, (dataset_size,1))-dataset
    #use euclide distance,
    squ_diff_mat=diff_matrix**2
    squ_distances=squ_diff_mat.sum(axis=1)
    distances=squ_distances**0.5
    sorted_distances=distances.argsort()
    class_count={}
    for i in range(k):
        #select majority label of top k class
        vote_label=class_labels[sorted_distances[i]]
        class_count[vote_label]=class_count.get(vote_label,0)+1
    sorted_class_count=sorted(class_count.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_class_count[0][0]

#transform the text file to matrix,
#assume first row is feature name, last column is class label
def file_to_matrix(filename):
    fr=open(filename)
    num_of_lines=len(fr.readlines())
    matrix=np.zeros((num_of_lines,3))
    class_labels=[]
    feature_names=[]
    fr=open(filename)
    feature_names=fr.readline().split('\t')[:-1]
    index=0
    for line in fr.readlines():
        line=line.strip()
        words_list = line.split('\t')
        matrix[index,:]=words_list[0:-1]
        class_labels.append(words_list[-1])
        index+=1
    return matrix,class_labels,feature_names

#normalize the data  new=(old-min)/(max-min)
def normalize(dataset):
    #get max and min value of each row
    min_value=dataset.min(0)
    max_value=dataset.max(0)
    ranges=max_value-min_value
    norm_dataset=np.zeros(np.shape(dataset))
    m=dataset.shape[0]
    norm_dataset=dataset-np.tile(min_value,(m,1))
    norm_dataset=norm_dataset/np.tile(ranges,(m,1))
    return norm_dataset, ranges, min_value

# split dataset to test set and train set,then test the error rate
def test(dataset,class_labels):
    test_train_ratio=0.2
    norm_dataset,ranges,min_value=normalize(dataset)
    #norm_testset=normalize(testset)
    l=norm_dataset.shape[0]
    num_of_test=int(l*test_train_ratio)
    error_count=0.0
    for i in range(num_of_test):
        result=classify(norm_dataset[i,:],norm_dataset[num_of_test:l,:],class_labels[num_of_test:l],4)
        if result != class_labels[i]:
            error_count+=1.0
    error_rate=error_count/num_of_test
    #print("the error rate is %f" %error_rate)
    return error_rate


#later are applies of the kNN--------------------------
def datingClassTest():
    dating_matrix,labels,feature_names=file_to_matrix('./dataset/datingTestSet2.txt')
    error_rate=test(dating_matrix,labels)
    print("the error rate is %f" %error_rate)

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

