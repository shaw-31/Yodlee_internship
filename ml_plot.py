import csv
from sklearn import svm
import numpy as np
import pickle
from sklearn.metrics import accuracy_score,recall_score,f1_score,confusion_matrix
from random import shuffle
X=[]
out=[]
Y=[]
Y_pred=[]
Y_true=[]
b=[]

###################################################################################################################################
## This script is independent of any other file. Used only for classification and prediction 
## classify () : input = path (training data, either relevant & irrelevant data passed in two steps or combined into one file
##               function = extracts only features from csv file (first 6 columns) to X list and 7th element 0/1 label to Y list
###################################################################################################################################

def classify(path):
    
    with open(path, newline='') as f:
        for line in f:
            out[:]=[]
            
            cells = line.split(" ")
            cells=[x for x in cells if x]  #removing empty strings
            for i in range(0,6):
                out.append(float(cells[i]))      #first 6 elements are the features
            
            Y.append(float(cells[6]))            #7th element is 0/1 depending on the table's relevancy
            X.append(out)            
        f.close() 
    #print(X)
    #print(Y)
    
###################################################################################################################################
## plot () : After the classification part is done, plot() uses arrays X and Y to fit the training data using SVM             
## NOTE : any classifier can be used in place of SVM without changing much code.
###################################################################################################################################
             
def plot():
    print(X)
    print(Y)
    clf=svm.SVC()
    clf.fit(X,Y)
    pickle.dump(clf,open("new_classifier.sav","wb"))
    
###################################################################################################################################
## true_list(): input = path of test data
##              output = Y_true list which has correct values or relevancy (0/1)
## true_list_pickle() : to store the true list in a pickle file for later use
###################################################################################################################################
def true_list(path):
    with open(path,newline='') as f:
        for line in f:
            cells=line.split(" ")
            cells=[x for x in cells if x]
            Y_true.append(float(cells[6]))
    print(Y_true)
    
            
def true_list_pickle():
    with open("new_truelist.txt","wb") as p:
        pickle.dump(Y_true,p)

###################################################################################################################################
## predict(): input = path of test data
##            output = Predicted values in Y_pred 
###################################################################################################################################
def predict(path):
       
    with open(path,newline='') as f:
        for line in f:
            out[:]=[]
            cells = line.split( " " )
            for i in range(0,6):
                out.append(float(cells[i]))
            print(out)
            clf=pickle.load(open("new_classifier.sav","rb"))
            print("Prediction:",clf.predict(out))
            Y_pred.append(float(clf.predict(out))) 
    print(clf)
    #print(Y_pred)
##################################################################################################################################
## result() : After getting Y_true which is loaded in b and Y_pred, print accuracy_score, recall_score and f1_score and 
    ## confusion_matrix for more clarity of true and false cases 
##################################################################################################################################
    
def result():    
    with open("new_truelist.txt","rb") as p:
        b=pickle.load(p)
    print(b) 
    print(Y_pred)
    #print(len(b),len(Y_pred))
    print(confusion_matrix(b,Y_pred))
    print(accuracy_score(b,Y_pred))
    print(recall_score(b,Y_pred))
    print(f1_score(b,Y_pred))
    
##################################################################################################################################
    
classify(r'C:\Users\anusha1\Desktop\jumbled_files.csv') 
plot()
true_list(r'C:\Users\anusha1\Desktop\jumbled_files_test.csv')
true_list_pickle()
predict(r'C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\mixed.csv')
result()