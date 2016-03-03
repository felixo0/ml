#Python3.5 Mac OS X
#2015.2.12
#mangobada@163.com

'''
implement of decision tree algorithm  C4.5
changed by ID3 in choose best feature to split 
from info_gain  to info_gain_ratio
to avoid choose the feature which has too many values
'''

from math import log
import operator
import numpy as np

#a small data set to verify the correction of program
def create_dataset():
    dataset = [[1, 1, 'yes'],
    [1, 1, 'yes'],
    [1, 0, 'no'],
    [0, 1, 'no'],
    [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataset, feature_names 

#
def pre_process(dataset): 
    pass

#transform the text file to matrix
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
         matrix[index,:]=words_list[0:-2]
         class_labels.append(words_list[-1])
         index+=1
     return matrix,class_labels,feature_names

#partiton  dataset to trainset and testset
def partition_dataset(dataset,ratio):
    l=len(dataset)
    len_test=l*ratio
    test_set=dataset[:len_test]
    train_set=dataset[len_test:]
    return train_set,test_set

#calculate entropy
def entropy(dataset):
    length=len(dataset)
    labels={}
    for feature_vec  in dataset:
        label=feature_vec[-1]
        if label not in labels.keys():
            labels[label]=0
        labels[label]+=1
    entropy=0.0
    for item  in labels:
        prob=labels[item]/length
        entropy-=prob*log(prob,2)
    return entropy

#return the splitted dataset where feature equal to value 
#and remove the feature_axis
def split_dataset(dataset,index,value):
    result=[]
    for feature_vec in dataset:
        if feature_vec[index]==value:
            reduced_vec=feature_vec[:index]
            reduced_vec.extend(feature_vec[index+1:])
            result.append(reduced_vec)
    return result

#discretize continues value by choose proper center-value
#the axis is the column need to discretize 
def discretize(dataset,feature_values,axis):
    base_entropy=entropy(dataset)
    best_info_gain_ratio=0.0
    split_entropy=0
    split_info=0.0
    best_discret_split=[]
    sorted_values=sorted(set(feature_values))
    for i in range(len(sorted_values)-1):
        cen=(sorted_values[i]+sorted_values[i+1])/2
        discret_values=[ 'L'+str(cen) if (value<cen) else 'H'+str(cen) for value in feature_values]
        unique_values=set(discret_values)
        tmp_data=dataset.copy()
        for index in range(len(discret_values)):
            tmp_data[index][axis]=discret_values[index]
        for value in unique_values:
            sub_dataset=split_dataset(tmp_data, axis,value)
            prob=len(sub_dataset)/float(len(tmp_data))
            split_entropy+=prob*entropy(sub_dataset)
            split_info-=prob*log(prob,2)
        info_gain_ratio = (base_entropy - split_entropy)/split_info
        if info_gain_ratio > best_info_gain_ratio:
            best_info_gain_ratio=info_gain_ratio
            best_discret_split=discret_values
    return best_discret_split



#the best feature is the one that has largest infoGain
def choose_best_feature_split(dataset):
    base_entropy=entropy(dataset)
    num_of_features=len(dataset[0])-1
    best_gain_ratio=0.0  #it's info gain in ID3
    best_feature=-1
    for i in range(num_of_features):
        feature_values=[x[i] for x in dataset]
        uni_feature_values=set(feature_values)
        new_entropy=0.0
        split_info=0.0
        for value in uni_feature_values:
            sub_dataset=split_dataset(dataset,i,value)
            D=len(dataset)
            Dj=len(sub_dataset)
            prob=Dj/D
            split_info -= (Dj/D)*log(Dj/D,2)
            new_entropy+=prob*entropy(sub_dataset)
        gain_ratio=(base_entropy-new_entropy)/split_info
        if gain_ratio>best_gain_ratio:
            best_gain_ratio=gain_ratio
            best_feature=i
    return best_feature

#get the majority count label of a set to represent the set
def majority(label_list):
    label_count={}
    for vote in label_list:
        if vote not in label_count.keys():
            label_count[vote] = 0
        label_count[vote] += 1
        sorted_label_count = sorted(label_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_label_count[0][0]

#equal to create_tree
def train(dataset,features):
    tree=create_tree(dataset,features)
    return tree

#recursively create a tree based on entropy
def create_tree(dataset,features):
    label_list=[x[-1] for x in dataset]
    #process special case
    if label_list.count(label_list[0])==len(label_list):
        return label_list[0]
    if len(dataset[0])==1:
        return majority(label_list)
    index=choose_best_feature_split(dataset)
    best_feature=features[index]
    my_tree = {best_feature:{}}
    del(feature[index])
    feature_values = [row[index] for row  in dataset] 
    unique_values = set(feature_values)
    for value in unique_values:
        sub_features = features[:]
        my_tree[best_feature][value] = create_tree(split_dataset(dataset, index, value),sub_features)
    return my_tree


def prune(tree):
    first_key=tree.keys()[0]
    subtree=tree[first_key]
    #all of subtree[key] is leaf node
    tree_bottom = all(type(subtree[key]).__name__ != 'dict' for key in subtree.keys())
    if tree_bottom==True:
        weighted_sum_error=0
        subtree_cases=0
        subtree_e=0
        subtree_classlist=[]
        for key in subtree.keys():
            classl_list


#classify the test sample by the input tree
def classify(tree, test, test_features):
    first_key=list(tree.keys())[0]
    value_dict=tree[first_key]
    #print(firstKey)
    #print(featureNames)
    feature_index=test_features.index(first_key)
    for key in value_dict.keys():
        if test[feature_index]==key:
            if type(value_dict[key]).__name__=='dict':
                class_label= classify(value_dict[key],test,test_features)
            else:
                class_label=value_dict[key]
    return class_label

#based on inputTree and features, classify tests and compare the result with class labels
def test(tree, testset, test_features):
    error_count=0.0
    num_of_tests=len(testset)
    for i in range(num_of_tests):
        result=classify(tree,test[i],test_features)
        if result != labels[i]:
            error_count+=1
    error_rate=error_count/num_of_tests
    return error_rate
