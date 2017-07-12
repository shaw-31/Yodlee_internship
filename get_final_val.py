
import os
from bs4 import BeautifulSoup
import sys
import re
import unicodedata
from collections import Counter
import string
import pickle

#------ Specify the paths for the condition check later ------#
path1 =r"C:\project\Priyanka\Training data\relevant"
path2= r"C:\project\Priyanka\Training data\irrelevant"
#-------------------------------------------------------------#


stop_words = ["'ll","'s","'m","a","about","above","after","again","against","all","am","an","and","-","--","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's",
"itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should",
"shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was",
"wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","###","arent","cant","couldnt","didnt","doesnt","dont","hadnt","hasnt","havent","hes","heres","hows","im","isnt","us","+","its","lets","mustnt","shant","shes","shouldnt","thats","theres","theyll","theyre","theyve","wasnt","were","werent","whats","whens","wheres","whos","whys","wont","wouldnt","youd","youll","youre","youve"]


##########################################################################################################
## relevant_wordlist() : input = path for which dict has to be created
## function = removes stop words, special characters, spaces and digits using regex
##########################################################################################################
    
def relevant_wordlist(path):  
    relevant_words = []
    wordcount={}
    denominator=0.0
    prob=0.0
    digits_regex="[0-9]+"
    special_char_regex="[\\,!@#$%&*(){}'<,>\.|//:;-_]+" #all special characters other than (space)
    re.compile(digits_regex)
    re.compile(special_char_regex)
    for fname in os.listdir(path):  #path1 instead of path for relevant, path2 for irrelevant words
        s="\\"
        seq=(path,fname)
        url=s.join(seq)
        #print(url)
        page=open(url)
        soup = BeautifulSoup(page.read(),'html.parser')
        try:
            table = soup.findAll('table')[0]
        except:
            continue
        
        words=table.text.strip()
        words=words.lower()
        words=re.sub('\n+',' ',words)
        words=re.sub(digits_regex,"1d",words)        
        words=re.sub(special_char_regex,"?",words)
        words1=words.replace("1d","")   #eliminate digits
        words2=words1.replace("?","")   #eliminate special characters
        relevant_words=words2.split()  #keep adding elements to relevant list in each iteration
        for word in relevant_words:
            if word in stop_words:
                relevant_words.remove(word)
            else:
                word=word.strip(string.punctuation)
                if word:
                    if word in wordcount:
                        wordcount[word] += 1
                    else:
                        wordcount[word] = 1
    print(wordcount)
    if(path==path1):
        with open('dict1.pickle', 'wb') as handle:                                        #store the relevant words in dict1
            pickle.dump(wordcount, handle, protocol=pickle.HIGHEST_PROTOCOL)  
    if(path==path2):                                                                      #store irrelevant words in dict2
        with open('dict2.pickle', 'wb') as handle:
            pickle.dump(wordcount, handle, protocol=pickle.HIGHEST_PROTOCOL)        
    #proper_list=[]        
    #print(relevant_words)
    #proper_list= [item for item in relevant_words if item not in stop_words]
    #print(proper_list)
    #dict=Counter(proper_list) #prints dictionary of words with their frequency        
    #print(dict)
    for key in wordcount:
        denominator+=wordcount[key]
    print(denominator)
    return denominator
