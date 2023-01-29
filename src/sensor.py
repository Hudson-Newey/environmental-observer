from util.constants import PORT, SERVER, MONITOR_SEGMENT_LENGTH

import asyncio
import websockets
import sounddevice as sd
import numpy as np

class SoundClassifier():
    def __init__(self):
        pass

class SoundListener():
    soundState = []

    def getSoundState(self, inData, outData, frames, time, status):
        volumeNorm = np.linalg.norm(inData)*10

        print("*" * int(volumeNorm))  # debug output
        self.soundState.append(volumeNorm.round(4))

    async def websocketConnection(self):

        # get connection name, this can also be called the room
        print("Connection Name:")
        # we are converting input to string to reduce type errors
        self.connectionName = str(input())

        # send the state of the microphone through a websocket
        while (True):
            self.soundState = []

            # gets the microphone state for the next 10 seconds
            # the state is stored inside the soundState[] variable
            # get microphone state outside of websocket
            with sd.Stream(callback=self.getSoundState):
                sd.sleep(MONITOR_SEGMENT_LENGTH)

            async with websockets.connect(SERVER + ":" + str(PORT)) as self.websocket:
                # first header should always be the connection (machine) name
                # second .send is sending the microphone state from the last 10 seconds
                await self.websocket.send(self.connectionName)
                await self.websocket.send(str(self.soundState))

    def __init__(self):
        asyncio.get_event_loop().run_until_complete(self.websocketConnection())

# program entry point
# convert monitorTime variable to milliseconds
MONITOR_SEGMENT_LENGTH *= 1000

# start the main program
SoundListenerOBJ = SoundListener()
