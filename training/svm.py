#smo implementation of svm
#refer to platt's paper
#2016.2.15
#mangobada@163.com

import numpy as np
import random

class Args:
    def __init__(self, data_matrix,class_labels, C, toler, k_tuple):
        self.data=data_matrix
        self.label=class_labels
        self.C = C
        self.t=toler
        self.m=np.shape(data_matrix)[0]
        self.a=np.mat(np.zeros((self.m,1)))   #alphas
        self.b=0
        self.error=np.mat(np.zeros((self.m,2)))    #error cache
        self.K=np.mat(np.zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i]=kernel(self.data, self.data[i,:], k_tuple)

#k_tuple save the kernel (eg. linear,radial  bias function) and  parameter of kernel
def kernel(data, A, k_tuple):
    m,n=np.shape(data)
    K=np.mat(np.zeros((m,1)))
    if k_tuple[0]=='lin':
        K=data*A.T
    elif k_tuple[0]=='rbf':
        for j in range(m):
            tmp_row=data[j,:]-A
            K[j]=tmp_row * tmp_row.T
        K=np.exp(K/(-1*k_tuple[1]**2))
    #add other kernel method
    else:
        raise NameError('unrecognized kernel')
    return K

def load_data(filename):
    matrix=[]
    class_labels=[]
    feature_names=[]
    fr=open(filename,'r')
    #feature_names=fr.readline().split()[:-1]
    for line in fr.readlines():
        word_list=line.strip().split()
        matrix.append([float(word_list[0]), float(word_list[1])])
        class_labels.append(float(word_list[2]))
        #matrix.append([1.0,float(words_list[0]),float(words_list[1])])
        #class_labels.append(words_list[-1])
    return matrix,class_labels,feature_names

def calc_error(args, k):
    fxk=float(np.multiply(args.a, args.label).T * args.K[:,k]) + args.b
    error_k = fxk - float(args.label[k])
    return error_k

#
def select_random_j(i,m):
    j=i
    while(j==i):
        j=random.uniform(0,m)
    return j

#heuristic select j
#select j to get largest error_i-error_j
def select_j(i, args, error_i):
    max_k = -1
    max_delta_k=0
    error_j=0
    args.error[i]= [1, error_i]
    valid_cache_list=np.nonzero(args.error[:,0].A)[0]
    if len(valid_cache_list) > 1:
        for k in valid_cache_list:
            if k==i:
                continue
            error_k = calc_error(args, k)
            delta_k=abs(error_i - error_k)
            if(delta_k > max_delta_k):
                max_delta_k = delta_k
                max_k = k
                error_j = error_k
        return max_k, error_j
    else:
        j=select_random_j(i, args.m)
        error_j=calc_error(args,j)
        return j, error_j

def clip_alpha(alpha_j,L,H):
    if alpha_j>H:
        alpha_j=H
    if alpha_j<L:
        alpha_j=L
    return alpha_j

def update_error(args, k):
    error_k = calc_error(args, k)
    args.error[k] = [1, error_k]

def take_step(i,j, args):
    if i1==i2:
        return 0
    if(args.label[i] != args.label[j]):
        L = max(0, args.a[j]-args.a[i])
        H = min(args.C , args.C+args.a[j]-args.a[i])
    else:
        L = max(0, args.a[j]+args.a[i]-args.C)
        H = min(args.C, args.a[j]+args.a[i])
    if L==H:
        print("L==H")
        return 0





def inner_loop(i, args):
    error_i = calc_error(args, i )
    if ((args.label[i] *error_i < -args.t) and (args.a[i] < args.C)) or ((args.label[i] * error_i > args.t ) and (args.a[i] > 0)):
        j, error_j = select_j(i, args, error_i)
        alphas_i_old = args.a[i].copy()
        alphas_j_old = args.a[j].copy()
        if(args.label[i] != args.label[j]):
            L = max(0, args.a[j]-args.a[i])
            H = min(args.C , args.C+args.a[j]-args.a[i])
        else:
            L = max(0, args.a[j]+args.a[i]-args.C)
            H = min(args.C, args.a[j]+args.a[i])
        if L==H:
            print("L==H")
            return 0
        eta = 2.0*args.K[i,j] - args.K[i,i] - args.K[j,j]
        #eta = 2.0*args.data[i,:]*args.data[j,:].T - args.data[i,:]*args.data[i,:].T - args.data[j,:]*args.data[j,:].T
        if eta>=0:
            print("eta>=0")
            return 0
        args.a[j] -= args.label[j]*(error_i - error_j)/eta
        args.a[j] = clip_alpha(args.a[j],L,H)
        update_error(args, j)
        if abs(args.a[j] - alphas_j_old) < 0.00001:
            print(" j not moving enough")
            return 0
        args.a[i] += args.label[j] * args.label[i] * (alphas_j_old - args.a[j])
        update_error(args, i)
        b1 = args.b - error_i - args.label[i]*(args.a[i] - alphas_i_old)*args.K[i,i]\
                - args.label[j]*(args.a[j]-alphas_j_old)*args.K[i,j]
        b2 = args.b - error_j - args.label[j]*(args.a[j] - alphas_j_old)*args.K[j,j]\
                - args.label[i]*(args.a[i]-alphas_i_old)*args.K[i,j]
        if args.a[i] > 0  and args.a[i] < args.C:
            args.b=b1
        elif args.a[j]>0 and args.a[j] < args.C:
            args.b=b2
        else:
            args.b=(b1+b2)/2.0
        return 1
    else:
        return 0

def smo(data_matrix, class_labels, C, toler, max_iter, k_tup=('lin',0)):
    args = Args(np.mat(data_matrix),np.mat(class_labels).transpose(), C, toler, k_tup)
    itera=0
    entire_set = True
    alpha_pairs_changed=0
    while (itera < max_iter)  and  ((alpha_pairs_changed>0) or entire_set):
        alpha_pairs_changed=0
        if entire_set:
            for i in range(args.m):
                alpha_pairs_changed+=inner_loop(i,args)
                print("fullset, iter: %d i:%d, pairs changed %d" %(itera, i,alpha_pairs_changed))
            itera+=1
        else:
            non_bound_i = np.nonzero((args.a.A>0) * (args.a.A<C))[0]
            for i in non_bound_i:
                alpha_pairs_changed+=inner_loop(i, args)
                print("non-bound iter: %d,i:%d, pair changed %d" %(itera,i,alpha_pairs_changed))
            itera+=1
        if entire_set:
            entire_set=False
        elif alpha_pairs_changed == 0:
            entire_set=True
        print("iteration number %d" %itera)
    return args.b,args.a

def calc_w(alphas, data_matrix, class_labels):
    data=np.mat(data_matrix)
    labels=np.mat(class_labels).transpose()
    m,n = np.shape(data)
    w=np.zeros((n,1))
    for i in range(m):
        w+=np.multiply(alphas[i]*labels[i], data[i,:].T)
    return w

def test(sigma=1.3):
    data_matrix,class_labels,feature_names=load_data('./dataset/Ch06/testSetRBF.txt')
    b,alphas=smo(data_matrix,class_labels,200, 0.0001,10000,('rbf',sigma))
    data=np.mat(data_matrix)
    labels=np.mat(class_labels).transpose()
    indice_sv=np.nonzero(alphas.A>0)[0]
    support_vectors=data[indice_sv]
    label_of_sv=labels[indice_sv]
    print("there are %d support vectors" %np.shape(support_vectors)[0])
    m,n = np.shape(data)
    error_count=0
    for i in range(m):
        ker=kernel(support_vectors, data[i,:],('rbf',sigma))
        #print(np.shape(ker.T))
        #print(np.shape(label_of_sv),np.shape(alphas[indice_sv]))
        predict=ker.T * np.multiply(label_of_sv,alphas[indice_sv])+b
        if np.sign(predict) != np.sign(labels[i]):
            error_count+=1
    training_error_rate=float(error_count/m)
    print("the training error rate is %f"%training_error_rate)

    data_matrix_test, class_labels_test, feature_names=load_data('./dataset/Ch06/testSetRBF2.txt')
    error_count_test=0
    data_test=np.mat(data_matrix_test)
    labels_test=np.mat(class_labels_test).transpose()
    m_t,n_t=np.shape(data_test)
    for i in range(m_t):
        ker=kernel(support_vectors, data_test[i,:],('rbf',sigma))
        #print(np.shape(ker))
        #print(np.shape(labels_of_sv),alphas[indice_sv])
        predict_test=ker.T * np.multiply(label_of_sv,alphas[indice_sv])+b
        if np.sign(predict_test) != np.sign(labels_test[i]):
            error_count_test+=1
    test_error_rate=(error_count_test/m_t)
    print("the test error rate is %f" %test_error_rate)
