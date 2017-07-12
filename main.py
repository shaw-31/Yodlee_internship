from __future__ import division
from bs4 import BeautifulSoup
from tokenize_tables import *
from get_table_consistency_geometric import *
import sys
import re
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from get_final_val import *
import csv
import pickle

##################### Paths for training data and test data ##################################

path=r"C:\project\Priyanka\Testing data\Non Relevant Tables"
#path = r"C:\project\Priyanka\Training data\irrelevant"
path1 = r"C:\project\Priyanka\Training data\relevant"
path2= r"C:\project\Priyanka\Training data\irrelevant"

###############################################################################################
## Relevant wordlist : function in get_final_val.py that forms the dictionary of {word : freq} 
##   and stores it in a pickle file. The total word count is returned as denominator. 
##  This function is called only once. Once the dictionary is created we need not call it again.

#d1=relevant_wordlist(path1)
#d2=relevant_wordlist(path2)

###############################################################################################

################ Getting denominator from the stored pickle file ##############################
with open('dict1.pickle', 'rb') as handle:
    dict1 = pickle.load(handle)
with open('dict2.pickle', 'rb') as handle:
    dict2 = pickle.load(handle)

d1=0
d2=0
for key in dict1:
    d1+=dict1[key]

for key2 in dict2:
    d2+=dict2[key2]

###############################################################################################



interactive = ['input','button','option','menu','menuitem','optgroup','select']


############## Parse through each file in the disk by specifying full path ####################
for fname in os.listdir(path): 
    
    s="\\"
    seq=(path,fname)            
    url=s.join(seq)                #file name added to the path
    page = open(url)
    soup = BeautifulSoup(page.read(),'html.parser')
    tags=0
    #print(soup.prettify())
    performance=[]
    try:
        #to avoid exception in case of a page with no table
        #('table')[0] specifies the first table in the file. If there's only 1 table in every file '[0]' can be removed.
        
        tables = soup.find_all('table')[0]   
    except:    
        #print("IR")
        performance.append(0.0)
        with open(r"C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\Irrel_zeroes.txt","a") as f:
            f.write(url)
            f.write("\n")
        print("0.0",url)
        continue
        
    
    y=tables.text
    re.sub("\s+",'',y)    #empty tables
    if(len(y)==0):
        #print("IR")
        performance.append(0.0)
        with open(r"C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\Irrel_zeroes.txt","a") as f:
            f.write(url) 
            f.write("\n")
        print("0.0",url)
        
    else:
        #print("Process further..")
        tot=0.0
        alpha=0                                 #alphanumeric characters
        final_list=[]                           #six features
        the_value=0.0                           #final value for a table
        result=0.0
        name=""                                 #tagname  
        d={}                                    #{tagname : frequency}
        num=0.0                                 #number of interactive tags
        den=0.0                                 #total number of tags
        wl=tables.text.strip()                  #wordlist
        #print(wl)
        if len(wl)==0:
            final_list.append(float("0.0"))     #alpha value
        else:
            for w in wl:
                tot+=1
                if(w.isalnum()):
                    alpha+=1            
            final_list.append(float(alpha/tot))
            for tag in tables.find_all():
                name=tag.name
                if name in d:
                    d[name]+=1
                else:
                    d[name]=1
        for key in d:
            den+=d[key]
            if key in interactive:
                num+=d[key]
        
        #print(d)
        #print(num,den)
        if(den==0.0):
            print("No tags in table")
            final_list.append(0.0)
        else:
            #print(1-(num/den))
            final_list.append(1-(num/den))        #Non-interactive elements > interative -> More relevant 
    
        tokenize_table_text(tables)
        #File Name, Column consistency (space seperated), Column Tokens, Arithmatic mean, Row consistency (space separated), Row tokens, Arithmatic mean 
        
        tables=get_table_consistency(tables,"abc","xyz")
        tables=tables.split(",")
        #print("tokenized:",tables,"len:",len(tables))
        col_consistency=tables[3]
        row_consistency=tables[6]
        if(row_consistency==' '):
            row_consistency=0.5
        if(col_consistency==' '):
            col_consistency=0.5
        #print(row_consistency)
        #print(col_consistency)
        
        final_list.append(1.0-float(row_consistency))
        final_list.append(1.0-float(col_consistency))
        

        #print(d1,d2)
        #print(dict1)
        #print(dict2)
        prob1=0.0
        prob2=0.0
        counter1=0
        counter2=0        
        for w in wl:
            w=w.lower()
            if w in dict1:
                prob1+=(dict1[w]/d1)
                counter1+=1
            else:
                prob1+=0.0
                
            if w in dict2:
                prob2+=(dict2[w]/d2)
                counter2+=1
            else:
                prob2+=0.0
        #print(prob1,prob2)
        if(counter1==0):
            prob1=0.0
            final_list.append(prob1)
        else:
            final_list.append(float(prob1)/counter1)
            
        if(counter2==0):
            prob2=0.0
            final_list.append(prob2)
        else:
            final_list.append(float(prob2)/counter2)
            
        
        for value in final_list:
            result+=value
        
        
        
############## NOTE : To store values for relevant and irrelevant tables separately the following changes have to be made in few lines that follow ################
                ## Relevant tables :- "final_list.append(1)", irrelevant tables :- "final_list.append(0)" 
                ## Change the csv file name accordingly
              
        final_list.append(0)
        print(final_list,url) #alpha,interactive-tag based prob, row consistency, col consistency, class1 (relevant), class2 (irrelevant),relevant/irrelavant(1/0)
        with open(r'C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\Irrel_info.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows([final_list+list(url)])
            
        the_value=result/6.0 
        performance.append(the_value)
 
        
        
############# A separate list of final values are stored in a text file. Change the path for relevant and irrelevant tables ######################################
        with open(r"C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\Irrel_values.txt","a") as f:
            f.write(str(the_value))
            f.write("\n")        
        print(the_value)
        final_list[:]=[]
            



