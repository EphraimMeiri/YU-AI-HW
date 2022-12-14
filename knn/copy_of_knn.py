import pandas
import numpy as np
from collections import Counter

# -*- coding: utf-8 -*-
"""Copy of knn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rcO24Ut8_AKB9wGcG3k2aM42IKaAOqFS

# Background

Import the libraries math (for square root and absolute value) and pandas and numpy for reading csv files.
"""

import math
import pandas as pd
import numpy as np

"""Make an untagged vector, point, and two tagged vectors, data1 and data2:"""

point = [1, 0, 0, '?'] #(an unknown tag)
data1 = [1, 1, 1, 'M']
data2 = [1, 3, 0, 'F']

"""Write code to separate the data (X) from the tag (Y).  Your output should be:

The vector [1, 1, 1] has tag M

The vector [1, 3, 0] has tag F

"""

print("The vector " , data1[0:-1], " has tag ", data1[-1])

"""Now let's classify the point as either M or F.  We'll do this by setting k = 1 and using the Euclidean distance.  We'll define that as: """

def euclideanDistance(instance1, instance2, length):
   distance = 0
   for x in range(length):
         #print ('x is ' , x)
         num1=float(instance1[x])
         num2=float(instance2[x])
         distance = distance + pow(num1-num2, 2)
   return math.sqrt(distance)

#Add code with functions that implement Hamming and Manhattan distances and test
#what the label will be for k=1 and k=3 for all possibilities
#(6 total: 2 Euclidean, 2 Hamming and 2 Manhattan)

def manhattanDistance(instance1, instance2, length):
   distance = 0
   for x in range(length):
         distance = distance + abs(instance1[x]-instance2[x])
   return distance


def hammingDistance(instance1, instance2, length):
  distance=0
  for x in range(length):
    if instance1[x]!=instance2[x]:
      distance+=1
  return distance


def knn(dataset,unknown,k,dist_func):
  length= len(unknown)
  distances = [[dist_func(dataset[x],unknown,length),dataset[x][-1]] for x in range(len(dataset))] # list of distances, will hold objects of type distClass
  distances.sort(key=lambda x: x[0])
  k_nearest_labels= [ls[1] for ls in distances[:4]]
  data = Counter(k_nearest_labels)
  return data.most_common(1)[0][0]

"""Up until here is a simplified version of the homework.
Below here is the work for the part we will be checking as the basis of your grade:

# The actual HW

Now let's look at some bigger files:

1. mytrain.csv (for training the model)
2. mytest.csv (for testing)
"""

url = 'mytrain.csv'
train_data = np.array(pd.read_csv(url,  header=0, error_bad_lines=False))
url = 'mytest.csv'
test_data = np.array(pd.read_csv(url,  header=0, error_bad_lines=False))

print(train_data.shape)# number of records and features
print(train_data)

print(test_data.shape)# number of records and features
print(test_data)

"""I hope by now you understand where we are going with this :)

Now implement the knn code with 3 different values for k:
1. k = 1
2. k = 7
3. k = 15

and at first use the Euclidean distance.
Classify each of the vectors in the test_data dataset using the training data from train_data.  Which value for k did the best?  What accuracy did it give you?

Now see if using Hamming or Manhattan distance give any better results for the same values of k.

Once you are done, you should have a total of 9 different results:

1. Three results for the different value of k using the Euclidean Distance
2. Three results for the different value of k using the Hamming Distance
3. Three results for the different value of k using the Manhattan Distance

Hint: I strongly suggest you base yourself on the code you've seen until this point so you don't have to reinvent the wheel!
"""



#Add code here
from collections import Counter
def knn(dataset,unknown,k,dist_func):
  length= len(unknown)
  distances = [[dist_func(dataset[x],unknown,length),dataset[x][-1]] for x in range(len(dataset))] # list of distances, will hold objects of type distClass
  distances.sort(key=lambda x: x[0])
  k_nearest_labels= [ls[1] for ls in distances[:k]]
  data = Counter(k_nearest_labels)
  return data.most_common(1)[0][0]


def test_knn(k,dist_func):
  score=0
  for test in test_data:
    result= knn(train_data,test[:-1],k,dist_func)
    if result==test[-1]:
      score+=1
  return score

print("K=1, Dist= Euclidian")
print("\t",test_knn(1,euclideanDistance))
print("K=7, Dist= Euclidian")
print("\t",test_knn(7,euclideanDistance))
print("K=15, Dist= Euclidian")
print("\t",test_knn(15,euclideanDistance),"\n")

print("K=1, Dist= Manhattan")
print("\t",test_knn(1,manhattanDistance))
print("K=7, Dist= Manhattan")
print("\t",test_knn(7,manhattanDistance))
print("K=15, Dist= Manhattan")
print("\t",test_knn(15,manhattanDistance),"\n")

print("K=1, Dist= Hamming")
print("\t",test_knn(1,hammingDistance))
print("K=7, Dist= Hamming")
print("\t",test_knn(7,hammingDistance))
print("K=15, Dist= Hamming")
print("\t",test_knn(15,hammingDistance))



"""Grade Basis:

80% for correct answers (and yes, there are possibilities that multiple answers are correct-- especially for cases of ties).

20% : Documentation and easily readable code

Please publish your final Notebook in your Github directory.

The homework assignment is due by November 30th.

"""