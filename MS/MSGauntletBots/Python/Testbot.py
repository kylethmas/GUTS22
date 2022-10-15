
import socket
import time
import random
 

msgFromClient       = "requestjoin:Niamh!!!"
name = "Niamh!!!"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024
walls = []
#bunch of timers and intervals for executing some sample commands
moveInterval = 1
timeSinceMove = time.time()

fireInterval = 5
timeSinceFire = time.time()

stopInterval = 30
timeSinceStop = time.time()

directionMoveInterval = 15
timeSinceDirectionMove = time.time()

directionFaceInterval = 9
timeSinceDirectionFace = time.time()

directions = ["n","s","e","w","nw","sw","ne","se"]
north_or_south = ["n","s"]
directionMoveMessage = "movedirection:n"

# Create a UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

visited_floor_x = []
visited_floor_y = []



def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)



while True:

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    
    ##uncomment to see message format from server
    #print(msgFromServer)
    
    if "playerupdate" in msgFromServer:
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        posx = float(posSplit[0])
        posy = float(posSplit[1])


    now = time.time()

    #every few seconds, request to move to a random point nearby. No pathfinding, server will 
    #attempt to move in straight line.
    #this is what we need to fix - include memoisation
    if "nearbywalls" in msgFromServer:
        wallPositions = msgFromServer.split(":")[1]
        wallSplit = wallPositions.split(",")
        for each in wallSplit:
            if each not in walls and each != "":
                walls.append(each)
    #print("WALLS")
    #print(walls)   
        
    if (now - timeSinceMove) > moveInterval:
        for xCoord in walls[::2]:
            #print("x  " + xCoord)
            #print("my x")
            print(posx)
            if (float(xCoord) - posx) < 4 and directionMoveMessage == "movedirection:e" :
                directionMoveMessage = "movedirection:w"
                SendMessage(directionMoveMessage)
            if (posx - float(xCoord)) < 4 and directionMoveMessage == "movedirection:w" :
                directionMoveMessage = "movedirection:e"
                SendMessage(directionMoveMessage)
            #if (posx - float(xCoord)) < 4 and (float(xCoord) - posx) < 4:
             #   directionMoveMessage = random.choice(north_or_south)
              #  SendMessage(directionMoveMessage)
            #need to check where we are in comparison to x coord
            
        for yCoord in walls[1::2]:
            
            if (float(yCoord) - posy) < 4 and directionMoveMessage == "movedirection:n":
                print(yCoord)
                directionMoveMessage = "movedirection:s"
                SendMessage(directionMoveMessage)
            if (posy - float(yCoord)) < 4 and directionMoveMessage == "movedirection:s":
                directionMoveMessage = "movedirection:n"
                SendMessage(directionMoveMessage)
        print(posx)
        print(posy)
        print(directionMoveMessage)
        
        visited_floor_x.append(posx)
        visited_floor_y.append(posy)
        
        randomX = random.randrange(-50,50)
        randomY = random.randrange(-50,50)
        posx += randomX
        posy += randomY

        timeSinceMove = time.time()
        requestmovemessage = "moveto:" + str(posx)  + "," + str(posy)
        SendMessage(requestmovemessage)
        print(requestmovemessage)

    #let's fire
    if (now - timeSinceFire) > fireInterval:
        timeSinceFire = time.time()
        fireMessage = "fire:"
        SendMessage(fireMessage)
        print(fireMessage)
       
        

    if(now - timeSinceStop) > stopInterval:
        stopMessage = "stop:"
        SendMessage(stopMessage)
        timeSinceStop = time.time()
        print(stopMessage)


    if(now - timeSinceDirectionMove) > directionMoveInterval:

        randomDirection = random.choice(directions)
        directionMoveMessage = "movedirection:" + randomDirection
        SendMessage(directionMoveMessage)
        timeSinceDirectionMove = time.time()
        print(directionMoveMessage)

    #if(now - timeSinceDirectionFace) > directionFaceInterval:

     #   randomDirection = random.choice(directions)
      #  directionFaceMessage = "facedirection:" + randomDirection
       # SendMessage(directionFaceMessage)
        #timeSinceDirectionFace = time.time()
        #print(directionFaceMessage)



