import matplotlib.pyplot as plt
import numpy as np
l1=[]
l=[0,0,0,0,0,0,0,0,0,0]
r=0.0

######################################################################################################################
## This code is indepedent of the others. 
## It considers a text file with values and plots a graph for Analysis 
######################################################################################################################

with open(r"C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\New Text Data\Irrel_table_values.txt","r") as f:
    s=f.read()
    l1=s.split()
    for i in range(len(l1)):
        l1[i]=float(l1[i])
        r=l1[i]
        if(r>=0.0 and r<0.1):
            l[0]=l[0]+1
        elif(r>=0.1 and r<0.2):
            l[1]=l[1]+1
        elif(r>=0.2 and r<0.3):
            l[2]=l[2]+1
        elif(r>=0.3 and r<0.4):
            l[3]=l[3]+1
        elif(r>=0.4 and r<0.5):
            l[4]=l[4]+1
        elif(r>=0.5 and r<0.6):
            l[5]=l[5]+1
        elif(r>=0.6 and r<0.7):
            l[6]=l[6]+1
        elif(r>=0.7 and r<0.8):
            l[7]=l[7]+1
        elif(r>=0.8 and r<0.9):
            l[8]=l[8]+1
        else:
            l[9]=l[9]+1
#print(l1)  performance values (x-axis)
print(l)   #count 
tot=sum(l)
norm_list=[]
for v in l:
    norm_list.append(v/tot)
print(norm_list) #normalised count (y-axis)
x=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
print(len(x),len(norm_list))
plt.xlabel('performance')
plt.ylabel('normalised count')
plt.title('Analysis of Irrelevant tables')
plt.plot(x,norm_list,'-o')
plt.legend()
plt.show()
