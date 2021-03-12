import asyncio
import websockets
from datetime import datetime
import os

# constants
# 1 = footsteps : 2 = talking : 3 = dropping : >4 = crashing
SOUND_THRESHOLD = 1
PORT = 8765
LOGDIRECTORY = "logs/"


# use a logs object to help with maintainability
class Logs():
    def writeLog(self, text):
        # find current time and save it as variable "timeStamp"
        timeStamp = datetime.now().strftime("%H%M%S")

        # use the timestamp as the file name
        # this can be used in a big data situation to track sound levels over time
        f = open(LOGDIRECTORY + timeStamp + ".log", "w")
        f.write(text)
        f.close()

    # deletes a log file by file name
    # fileName = timestamp which you want to be deleted
    def deleteLog(self, fileName):
        # checks if the file exists to avoid runtime errors
        if os.path.exists(LOGDIRECTORY + fileName):
            os.remove(LOGDIRECTORY + fileName)
        else:
            # ERROR 404, FILE NOT FOUND
            print("ERROR 404, FILE NOT FOUND!")
    
    # reads a log file by file name
    # fileName = timestamp which you want to read
    # returns the contents of the given log
    def readLog(self, fileName):
        if os.path.exists(LOGDIRECTORY + fileName):
            return open(LOGDIRECTORY + fileName, "r").read()
        else:
            # ERROR 404, FILE NOT FOUND
            print("ERROR 404, FILE NOT FOUND!")
            return "ERROR 404, FILE NOT FOUND!"

    def __init__(self):
        pass


class Observer():
    async def websocketServer(self, websocket, path):
        # websocket headers
        self.connectionName = await websocket.recv()
        self.soundState = await websocket.recv()

        # convert string back into array
        self.soundState = self.soundState.replace(",", "")[1:-1:]
        self.soundState = self.soundState.split()

        # print(self.soundState) # debug output

        # convert string array into float array
        for i in range(0, len(self.soundState)):
            self.soundState[i] = float(self.soundState[i])

        # find if threshold is met
        self.soundsHeard = 0
        for i in range(len(self.soundState)):
            if (self.soundState[i] > SOUND_THRESHOLD):
                self.soundsHeard += 1

        # show the output for the current connection
        # shows the connection name (or room) and the amount of microphone states exceding the sound
        print("[" + self.connectionName + "] : " + str(self.soundsHeard))

        # log the result through the Logs object
        logsOBJ.writeLog("[" + self.connectionName + "] : " + str(self.soundsHeard))

    def __init__(self):
        # show output to prove the program is running
        print("Starting websocket server on :" + str(PORT))

        # create websocket listening server
        startServer = websockets.serve(self.websocketServer, "localhost", PORT)

        asyncio.get_event_loop().run_until_complete(startServer)
        asyncio.get_event_loop().run_forever()


# program entry point
logsOBJ = Logs()
environmentalOberserver = Observer()
