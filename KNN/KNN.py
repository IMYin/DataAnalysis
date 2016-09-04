#-*-coding=utf-8-*-

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels
group,labels = createDataSet()

def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)   #行与行之间的和 ，当axis=0时，计算的是列之间的和

    distances = sqDistances ** 0.5

    #argsort函数返回的是数组值从小到大的【索引值】
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]   #第一次循环取最小值的索引值，也就是取距离最小的label
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1

#下面这句话代表将结果进行排序，按照第二个元素的次序对元组进行排序（key的作用），reverse = True 表示将结果倒序输出
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse = True)
   
#classCount.iteritems() 是字典的迭代器。详情请查看 http://www.iplaypython.com/jinjie/items-iteritems.html
   return sortedClassCount[0][0]
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()  #截掉回车字符
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

#数据归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges ,minVals

#测试数据
def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('/home/sunnyin/data_ml/datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]  #取行数
    numTestVecs = int(m*hoRatio)  #取测试集的行数
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],7)
#         print("the classifier came back with:" + str(classifierResult) + " ,the real answer is : "+ str(datingLabels[i]))
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
    print("the total error rate is : "+ str(errorCount/float(numTestVecs)) )

def classifyPerson():
    resultList = ['一点也不适合','有点适合','非常适合']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    datingDataMat,datingLabels = file2matrix('/home/sunnyin/data_ml/datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr - minVals)/ranges,normMat,datingLabels,3)
    print("You will probably like this person: ",resultList[classifierResult - 1])



# datingClassTest()
classify0([0,0],group,labels,3)
