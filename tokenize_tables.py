# -*- coding: utf-8 -*
# -*- coding: ISO-8859-1 -*
from bs4 import BeautifulSoup,NavigableString
import re,sys
from dateutil.parser import parse
import glob, codecs, os, shutil
from shutil import copy
import unicodedata

#############################################################################################################
# Steps:
##############################################################################################################

token_list = []
def read_tokens(filename):
    with open(filename, encoding='utf8') as file:
        for line in file:
            #print(line)
            token_list.append(line.strip())
    return token_list
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def validate_date(text):
    valid = False
    #print(text)
    parse(text)
    try:
        print("in here")
        parse(text)
        valid = True
        print("valid in validate try is:",valid)
    except ValueError as e:
        print(e)
        pass
    print("valid in validate is:",valid)
    return valid


def normalize_text(text):
    ### replace chars with c/C 
    text = smallcase_char_regex.sub("c",text)
    text = capcase_char_regex.sub("C",text)
    ### replace digits with d
    text = digit_regex.sub("d",text)
    ### replace special chars with s
    normalized_text = sp_char_regex.sub("s",text)

    ## strip start and end special chars
    normalized_text = end_sp_char_strip_regex.sub("",begn_sp_char_strip_regex.sub("",normalized_text))

    return normalized_text 

def encode_text(text):
    if len(text) ==0 : 
        return
    char = text[0]
    j=0
    encodedtext=""
    for c in text:
        if c == char:
            j = j +1 
        else:
            #print(j,char)
            encodedtext += str(j)+str(char)
            j = 1
            char = c
    #print(j,char)
    encodedtext += str(j)+str(char)
    return encodedtext


def get_token(encodedtext):

    if encodedtext is not None and encodedtext in token_list:
        return encodedtext
    return "OTHER"        


def tokenize(text):
    words = text.split()
    tokenized_text=""
    for word in words:
        normalized_text = normalize_text(word)
        #print("token text:",word,"normalized text:",normalized_text)
        encodedtext = encode_text(normalized_text)
        #print("encoded text:",encodedtext)

        if encodedtext is not None:
            ### piece to convert [0-9] s-->s, [0-9] d-->d
            text = multiple_digit_replace_regex.sub("d",encodedtext)
            encodedtext = multiple_spchar_replace_regex.sub("s",text)
            ### piece to convert [0-9] c-->c, [0-9] C-->C
            #text = multiple_char_replace_regex.sub("c",encodedtext)
            #encodedtext = multiple_upchar_replace_regex.sub("C",text)

        #print("encoded text:",encodedtext)
        token=get_token(encodedtext)
        tokenized_text+=str(token)+" "

    return tokenized_text.strip()

def tokenize_table_text(table):
    #rows=table.findAll('tr')
    rows=table.findAll(lambda tag:tag.name=="tr" and not tag.has_attr('hidden'))
    #print(table.text)
    #print("#rows:",len(rows))
    for row in rows:
        #print("row")
        #inner_tags = row.findAll(['td','th'])
        inner_tags = row.findAll(lambda tag:(tag.name=="th" or tag.name=="td")  and not tag.has_attr('hidden'))
        #print("#inner_tags:",len(inner_tags))
        #inner_tags = row.findAll()
        for tag in inner_tags:
            #print('current tag is:',tag,"tag text is:",tag.string,"text is:",tag.text)
            if len(tag.text)!=0:
                #print('tag content',tag.text)
                for tag1 in tag.findAll():
                    if tag1.has_attr('hidden'):
                        tag1.extract()
                tokentext = tag.text.replace("\n"," ").replace("&nbsp;","").replace(",","")
                tokentext = " ".join(tokentext.split())
                #print(tokentext)
                tokentext = strip_accents(tokentext)
                tokentext = tokenize(tokentext)
                #print("tokentext:",tokentext,"previous_text:",tag.string)#"content text:",tag.contents[0].replace("\n",""))
                if tokentext is not None and tokentext.strip()!="":
                    #print(tag.contents[0])
                    tag['token'] = tokentext
                #print('modified tag is:',tag)

def extract_tables(files,dumppath,token_dumppath):
    '''with open(table_details_csv, encoding='utf8') as file:
         headerline=next(file)
         for line in file:
              fields = line.replace("\n","").split(",")
              if fields[4]=="Yes":'''
    token_list = read_tokens(tokenfile)
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
        if table.has_attr('hidden'):
            continue
        tokenize_table_text(table)
        #print(table)
        #print("tokenized:",os.path.basename(filename))
        file = codecs.open(token_dumppath+"/"+os.path.basename(filename), "w", "utf-8")
        file.write(table.prettify())
        file.close()


sp_char_regex = re.compile("[^c|^d|^C|^ ]")
smallcase_char_regex = re.compile("[a-z]")
capcase_char_regex = re.compile("[A-Z]")
digit_regex = re.compile("[0-9]")
begn_sp_char_strip_regex = re.compile("^s+")
end_sp_char_strip_regex = re.compile("s+$")
multiple_digit_replace_regex = re.compile("[0-9]+d")
multiple_spchar_replace_regex = re.compile("[0-9]+s")
multiple_char_replace_regex = re.compile("[0-9]+c")
multiple_upchar_replace_regex = re.compile("[0-9]+C")
#tokenfile = "xs_xd_xc_xC_tokens_gt100freq.txt"
tokenfile = "1s_1d_xc_xC_tokens_gt100freq.txt"
#tokenfile = "xs_xd_1c_1C_tokens_gt100freq.txt"
#tokenfile = "1s_1d_1c_1C_tokens_gt100freq.txt"

if __name__ =='__main__':
    if len(sys.argv)==1:
        print("Enter location of table dump files and location for tokenized dump files")
        exit(0)
    elif len(sys.argv)==2:
        print("You either did not enter location of table dump files or location for tokenized dump files")
        exit(0)
    else:
        dumppath = sys.argv[1:(len(sys.argv) - 1)][0]
        token_dumppath = sys.argv[len(sys.argv) - 1]
    files = glob.glob(dumppath+"/*")
    #table_csvfile="table_details_150_allusers_with_xmlmatches.csv"
    #table_csvfile="table_details.csv"

    extract_tables(files,dumppath,token_dumppath);
