import requests
import csv
import sys

inputFile = sys.argv[1]

def download(name,url):
    
    response = requests.get(url)
    extension = response.headers["Content-Type"].split("/")[-1]
    fileName = ".\\Output\\"+name+"."+extension
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

    playersData = reader(inputFile)
    for i in playersData:
        download(i["Player Name"],i["Image URL"])
        
    exit()


if __name__=="__main__":
    main()
