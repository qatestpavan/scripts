import requests
import csv
import argparse
import multiprocessing
import time

parser = argparse.ArgumentParser()
parser.add_argument("--input", help = "This option is for entering input file", type=str)
parser.add_argument("--output", help  = "Output File path need to be added, y default current directory is taken", type=str)
parser.add_argument("--namecol",help = "The ouput filename in the given CSV file", type=str)
parser.add_argument("--urlcol",help = "The url column in the given CSV file", type=str)
parser.add_argument("--threadcount",help="This option activates multi threading",type=int)
args = parser.parse_args()
inputFile = args.input
nameColumn = args.namecol
urlColumn = args.urlcol
threadCount = args.threadcount
if threadCount == None: threadCount = 1
outPath = ''
if args.output:
    outPath = args.output


def download(name,url):
    response = requests.get(url)
    extension = response.headers["Content-Type"].split("/")[-1]
    fileName = outPath+"\\"+name+"."+extension
    with open(fileName,"wb") as imageFile:
        imageFile.write(response.content)
        print(f"[+] Created the file {fileName}")
    
    response.close()
    return True

def reader(dataFile):
    
    with open(dataFile,"r") as csvFile:
        csvData = csv.reader(csvFile)
        headings = csvData.__next__()
        itemList = []
        for row in csvData:
            itemList.append(dict(zip(headings,row)))
        
    return itemList

def multiproc(data):
    for i in data:
        download(i[nameColumn],i[urlColumn])

def main():

    playersData = reader(inputFile)
    percount = int(len(playersData)/threadCount)
    if percount == 0: percount = 1
    workPerProcessor = []
    count = 0
    processes = []
    startTime = time.time()
    while (count<len(playersData)):
        workPerProcessor = playersData[count:(count+percount)]
        count +=percount
        workProcess = multiprocessing.Process(target=multiproc , args=(workPerProcessor,))
        processes.append(workProcess)
        workProcess.start()

    for i in processes:
        i.join()


    print(f"--------------------------\nIt took {time.time()-startTime} seconds.")

    
    

    """
    for i in playersData:
        download(i[nameColumn],i[urlColumn],outPath)

    """
    exit()


if __name__=="__main__":
    main()
