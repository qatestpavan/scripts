import requests
import csv
import sys
import argparse
import time

def download(name,url,outPath):
    
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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help = "This option is for entering input file", type=str)
    parser.add_argument("--output", help  = "Output File path need to be added, y default current directory is taken", type=str)
    parser.add_argument("--namecol",help = "The ouput filename in the given CSV file", type=str)
    parser.add_argument("--urlcol",help = "The url column in the given CSV file", type=str)
    args = parser.parse_args()

    #global inputFile , nameColumn , urlColumn ,outPath

    inputFile = args.input
    nameColumn = args.namecol
    urlColumn = args.urlcol
    outPath = ''
    if args.output:
        outPath = args.output
    
    playersData = reader(inputFile)
    startTime = time.time()
    for i in playersData:
        download(i[nameColumn],i[urlColumn],outPath)

    print(f"--------------------------\nIt took {time.time()-startTime} seconds.")

    exit()


if __name__=="__main__":
    main()
