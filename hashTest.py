import sys
import hashlib
from os.path import exists
#BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  #lets read stuff in 64kb chunks!
CSV_FILE = 'HASH_DATABASE.csv'
CATEGORIES = ['real_image', 'fake_image']

def hashFunc(file,type = 0):
    global BUF_SIZE
    hash = ''
    if (type == 0):
        hash = hashlib.md5()
    elif (type ==1 ):
        hash = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

def writeHashToCsv(hash = ''):
    if hash == '':
        return
    if exists(CSV_FILE) == 0:
        with open(CSV_FILE, 'x') as file:
            file.close()
    else:
        with open(CSV_FILE, 'r') as file:
            compare = file.read()
            if hash in compare:
                file.close()
                return
    with open(CSV_FILE, 'a') as file:
        file.writelines(str(hash)+'\n')
        file.close()
        
def writeHashToCsvWithValues(hash = '',valueList = []):
    if hash == '' or valueList == []:
        return
    if exists(CSV_FILE) == 0:
        with open(CSV_FILE, 'x') as file:
            file.close()
    else:
        with open(CSV_FILE, 'r') as file:
            compare = file.read()
            if hash in compare:
                file.close()
                return
    #typo? changes from ea to a, ea invalid mode 
    with open(CSV_FILE, 'a') as file:
        line  = str(hash)
        for value in valueList:
            value = CATEGORIES[value]
            #print(value)
            line = line + ',' + value
        file.writelines(line+'\n')
        file.close()

def hashAndWriteToCSV(file = '', valueList = []):
    if file == '' or valueList == []:
        return
    #sha1 hash change if wanted
    hash = hashFunc(file,0)
    #print(hash)
    writeHashToCsvWithValues(hash,valueList)