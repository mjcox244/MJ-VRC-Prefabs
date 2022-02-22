import argparse, requests, time
from datetime import datetime, timezone
from pythonosc import udp_client

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",)
  parser.add_argument("--port", type=int, default=9000,)
  args = parser.parse_args()
  client = udp_client.SimpleUDPClient(args.ip, args.port)

#Get IP
r = requests.get("http://api.ipify.org")
IP = r.text

try:
    #Get Coordinates
    r = requests.get("https://ipapi.co/"+IP+"/json/")
    Offset = int(r.json()["utc_offset"])/100
    Lat = r.json()["latitude"]
    Long = r.json()["longitude"]

    Parrams = {'lat': Lat, 'lng':Long}
    r = requests.get("https://api.sunrise-sunset.org/json", params=Parrams)

    #Night
    DStart = r.json()["results"]["nautical_twilight_begin"].split(" ")[0].split(":")
    NStart = r.json()["results"]["nautical_twilight_end"].split(" ")[0].split(":")

    NStart = [(int(NStart[0])+Offset),int(NStart[1])+Offset,int(NStart[2])+Offset]
    DStart = [(int(DStart[0])+Offset),int(DStart[1])+Offset,int(DStart[2])+Offset]
    if "PM" in r.json()["results"]["nautical_twilight_end"]:
        NStart[0] += 12
        NStart[0] = NStart[0] % 24
    if "PM" in r.json()["results"]["nautical_twilight_begin"]:
        DStart[0] += 12
        DStart[0] = DStart[0] % 24

    if NStart[0] < 0: 
        NStart[0] = NStart[0]+24
    print(NStart)
    print(DStart)

except:
    UtcT = int(datetime.now(timezone.utc).strftime('%H'))
    LocalT = int(datetime.now(timezone.utc).strftime('%H'))
    Offset = int(LocalT - UtcT)

    DStart = [7,0,0]
    NStart = [19,0,0]


while True:
    T = datetime.now(timezone.utc).strftime('%H:%M:%S').split(":")
    T = [(int(T[0])+Offset) % 24,int(T[1]),int(T[2])]

    #After Sunrise And Before Sunset
    if T[0] < NStart[0] and T[0] > DStart[0]:
        client.send_message("/avatar/parameters/IsNight", 0)
        print(0)
    elif T[0] == NStart[0] or T[0] == DStart[0]:
        if T[1] < NStart[1] and T[1] > DStart[1]:
            client.send_message("/avatar/parameters/IsNight", 0)
            print(0)
        elif T[1] == NStart[1] or T[1] == DStart[1]:
            if T[2] < NStart[2] and T[2] > DStart[2]:
                client.send_message("/avatar/parameters/IsNight", 0)
                print(0)
            else: 
                client.send_message("/avatar/parameters/IsNight", 1)
                print(1)
        else: 
            client.send_message("/avatar/parameters/IsNight", 1)
            print(1)
    else:
        client.send_message("/avatar/parameters/IsNight", 1)
        print(1)

    time.sleep(1)
    #client.send_message("/avatar/parameters/IsNight", 1)

