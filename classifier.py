from sklearn import DecisionTreeClassifier

dataset=[[no_of_actual_cols,howmanycols u want,what u think the thresholdis],[],[],[]]
label=[1,0,1]

dt=tree.DecisionTreeClassifier
dt=dt.fit(dataset,label)

dt.predict([n,w,th])

from sklearn import tree
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
female=0
male=1
sample=[]
for i in range(0,12):
    sample.append(i)
S=np.array(sample)    
X=[[5.0,46,6],[5.4,46,6],[5.2,43,7],[5.1,44,5],[5.9,65,8],[5.6,56,7],[6.1,71,9],[5.9,67,9],[5.4,52,6],[5.0,40,5],[6.2,77,10],[5.7,61,8]]
Y=[female,female,female,female,male,male,male,male,female,female,male,male]
X=np.array(X)
Y=np.array(Y)

clf=tree.DecisionTreeClassifier()
clf=clf.fit(X,Y)
predict=clf.predict([5.4,62,6])

if(predict==0):
    print('FEMALE')
else:
    print('MALE')
