# -*- coding: utf-8 -*
# -*- coding: ISO-8859-1 -*
from bs4 import BeautifulSoup,NavigableString
import re,sys
from dateutil.parser import parse
import glob, codecs, os, shutil
from shutil import copy
import unicodedata
#from scipy.stats.mstats import gmean

#############################################################################################################
# Steps: 
## Input: path of tokenized table location
## 1. get tables
## 2. extract column wise tokens 
## 3. calculate column consistency
## 4. calculate table consistency
##############################################################################################################


##############################################################################################################
### Get number of columns in the table
### Input: html table extracted using beautifulsoup
### Output: # of columns in the table
##############################################################################################################
def get_no_of_cols(table):
    rows = table.findAll('tr')
    col_count=[]
    for row in rows:
        ths = row.findAll(['th','td'])
        col_count.append(len(row.findAll(['th','td'])))
    #print(col_count)
    col_freq_dict={}
    for col in col_count:
        if col in col_freq_dict:
            col_freq_dict[col]+=1
        else:
            col_freq_dict[col]=1
    maxFreq=0
    colmaxFreq=0
    #print(col_freq_dict)
    for colval,count in col_freq_dict.items():
        if(count>maxFreq):
            maxFreq=count
            colmaxFreq=colval
    return colmaxFreq

##############################################################################################################
### Get column wise tokens
### Input: html table extracted using beautifulsoup, filename for log purpose
### Output: List of tokens for each column (list of list) and header token list
##############################################################################################################

def get_column_data(table,filename):
    no_of_cols = get_no_of_cols(table)
    #print(no_of_cols)
    rows = table.findAll('tr')
    column_data =[]
    header =[]
    i = 0
    #print("COL NUMS:",no_of_cols)
    while i <= no_of_cols:
        #print("i",i)
        cols = ''
        thheader=''
        try:
            cols = [ td['token'].strip(' \t\n') for td in table.select('tr > td:nth-of-type('+str(i)+')')]
             #print(i,"th column",cols)
        except:
            pass
        try:
            thheader =[ th['token'].strip(' \t\n') for th in table.select('tr > th:nth-of-type('+str(i)+')')][0]
            #print("th header is",thheader)
            #print(header)
        except:
            pass
        column_data.append(cols)
        header.append(thheader)
        i = i+1

    #print("num headers",len(header),"***",header)
    #print("num columns data",len(column_data),"***",column_data)
    return column_data,header

def get_row_data(table,filename):
    rows = table.findAll('tr')
    row_data = []
    header = []
    for row in rows:
        rowtags=[]
        tags = row.findAll('td')
        try:
            rowtags = [ tag['token'].strip(' \t\n') for tag in tags]
             #print(i,"th column",cols)
        except:
            pass
        row_data.append(rowtags)
    return row_data,header
    
##############################################################################################################
### Get consistency for input column
### Input: list of column tokens
### Output: consistency value
##############################################################################################################

def compute_consistency(in_list = ["string", "date", "string", "STR", "String","string"]):
    uniq_strings = {}
    for thstr in in_list:
        uniq_strings[thstr] = uniq_strings.get(thstr,0)+1
    max_val = max([uniq_strings[x] for x in uniq_strings.keys()])
    consistency_value = max_val*1.0/len(in_list)
    #diagnostic_print(uniq_strings,0),    print("consistency-value is %.2f" %(consistency_value))
    rev_dict = dict((v, k) for k, v in uniq_strings.items())

    return consistency_value, rev_dict[max_val]

##############################################################################################################
def get_rowcolumn_consistency(table,filename,cons_file,column_data):
    ### Print column wise data
    #for i in range(0,len(column_data)):
        #print("i is",i)
        #print("FILE:",filename,"Column header:",header[i],"Column data:",column_data[i])
    
    val = 0
    col_consist=[]
    token_list=[]
    #print(column_data)
    ## for each column calculate the consistency
    #print(len(column_data)) 
    
    if len(column_data)==0:
         colcon = "|".join([str(i) for i in col_consist])
         strcons=colcon + ", , 0.0"
         return strcons
    for col in column_data:
         if col is not None and len(col)!=0:
              val, token = compute_consistency(col)
              col_consist.append(val)
              token_list.append(token)
    #print(col_consist) 
    if len(col_consist)==0:
         colcon = "|".join([str(i) for i in col_consist])
         strcons=colcon + ", , 0.0"
         return strcons
    
    colcon = "|".join([str(i) for i in col_consist])
    tokencon = "|".join(token_list)
    colcon_float = col_consist
    arith_mean = sum(col_consist)/len(col_consist)
    #gmean_val = gmean(colcon_float)
    strcons=colcon + "," + tokencon + "," + str(arith_mean) #+ "," + str(gmean_val) 

    return strcons
##############################################################################################################
### Get table consistency
### Input: html table extracted using beautifulsoup, filenames for log purpose
### Output: consistency of the table
##############################################################################################################
def get_table_consistency(table,filename,cons_file):
    column_data,header = get_column_data(table,filename)
    #print(column_data,header)
    col_cons_details = get_rowcolumn_consistency(table,filename,cons_file,column_data)
    row_data,header = get_row_data(table,filename)
    row_cons_details = get_rowcolumn_consistency(table,filename,cons_file,row_data)

    #cons_file.write(strcons)
    return filename+","+col_cons_details+","+row_cons_details +"\n"

    
##############################################################################################################
### Extract tables from all the tokenized files and calculate consistency
### Input: tokenized files
##############################################################################################################

def extract_tables(files, consistency_file):
    file = codecs.open(consistency_file, "w", "utf-8")
    file.write("File Name, Column consistency (space seperated), Column Tokens, Arithmatic mean, Geometric mean, Row consistency (space separated), Row tokens, Arithmatic mean, Geometric mean\n")
    for filename in files:
         #filename = dumppath+"/"+fields[0]
         #copy(filename,token_dumppath)
         try:
             file1 = open(filename,'r').read()
         except:
             file1 = open(filename, 'r', encoding="utf-8").read()

         print('File : '+ filename)
         soup = BeautifulSoup(file1 ,'html.parser', from_encoding="utf8")
         table=soup('table')[0]
         #consistency = get_table_consistency(table,filename,file)
         #print(table)
         strcons= get_table_consistency(table,filename,file)
         file.write(strcons)
    file.close()



if __name__ =='__main__':
    if len(sys.argv) < 3:
        print("Enter location for tokenized dump tables and Name of the csv file to store the consistency values")
        exit(0)
    else:
        token_dumppath = sys.argv[1].strip()
        consistency_file = sys.argv[2].strip()
    files = glob.glob(token_dumppath+"/*")
    extract_tables(files, consistency_file);

