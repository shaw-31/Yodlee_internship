import csv
from random import shuffle

############################################################################################################
## jumble(): takes a path of csv file and reorders the rows in the file and stores it in another file
############################################################################################################
def jumble(path):
    
    with open(path, newline='') as f:
        reader=csv.reader(f)
        l=list(reader)
        #print(l)
        shuffle(l)
        print(l)
        with open(r'C:\Users\anusha1\Desktop\jumbled_files_test.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerows([i for i in l])  
            

#jumble(r'C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Training data info\mixed.csv')
jumble(r'C:\Users\anusha1\AppData\Local\Programs\Python\Python36-32\Test data info\mixed.csv')
