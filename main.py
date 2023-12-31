import requests
import time
import csv
import sys

url = 'http://apis.data.go.kr/B551177/StatusOfParking/getTrackingParking'
params ={'serviceKey' : 'enter your own service key', 'numOfRows' : '10', 'pageNo' : '1', 'type' : 'json' }
draftList = []
newList = []
recentTime = "N/A"
limit_number = 10000
sys.setrecursionlimit(limit_number)

def getData(): 
  response = requests.get(url, params=params)
  global draftList
  global newList
  currentDate = str(time.strftime("%D"))
  currentTime = str(int(time.strftime("%H"))+ 9)+":"+str(time.strftime("%M")) #strfttime returns with GMT time
  newList = [currentDate,currentTime]
  draftList = str(response.content).split("parking\":\"")
  del draftList[0]
  for longItem in draftList:
    newList.append(longItem.split("\"")[0])
  #print(newList) #Debugging mode
  #print(response.content) #Debugging mode
    

#getData() #Debugging mode

def timecheck():
  global recentTime
  if (int(time.strftime("%M")) % 10) == 0: #Make sure this value is 0 when published
    if not recentTime == time.strftime("%H:%M"):
      try:
        getData()
        f = open('C:/Users/Administrator/Desktop/Incheon_Airport_Parking/parkingstatus.csv','a', newline='')
        wr = csv.writer(f)
        wr.writerow(newList)
        f.close()
        print("Confirmed @ " + str(time.strftime("%H:%M")))
        recentTime = time.strftime("%H:%M")
      except:
        print("Error!")
    # time.sleep(30) # Sleep for 30 seconds
    # timecheck()
  else:
    print("Waiting @ " + str(time.strftime("%H:%M")))
    # time.sleep(30) # Sleep for 30 seconds
    # timecheck()

while True:
  timecheck()
  time.sleep(30) # Sleep for 30 seconds
