import asyncio as async_io
import json
import websockets
import random


# listen and respond to serenade messages
# and handle the websocket connection
class CommandHandler:
    def __init__(self, editor_state: dict):
        self.editor_state = editor_state
        self.id = str(random.random())
        self.websocket = None
        # register the handlers for each type of message
        message_handlers = {}

    # The serenade protocol defines that every message has a string message and data (any)
    async def send(self, message: str, data: any):
        if not self.websocket:
            return
        await self.websocket.send(json.dumps({'message': message, 'data': data}))

    # send a heartbeat to serenade every few seconds to keep the connection alive
    # (only if there is a connection)
    async def send_heartbeat(self):
        try:
            while True:
                if self.websocket:
                    await self.send('heartbeat', {'id': self.id})
                await async_io.sleep(5)
        except async_io.CancelledError:
            print('heartbeat was cancelled') 

    
    
    def start_listening(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.heartbeat_task = async_io.create_task(self.send_heartbeat())
        async_io.get_event_loop().run_until_complete(self._listen())



    def stop_listening(self):
        self.is_listening = False
        self.websocket = None
        # cancel the heartbeat
        self.heartbeat_task.cancel()
    
    
    async def _listen(self):
        while self.is_listening:
            try:
                async with websockets.connect("ws://localhost:17373") as ws:
                    print("connected")
                    self.websocket = ws
                    # initial activation message
                    await self.send(
                        "active",
                        {"id": id, "app": "minimal_client", "match": "client"},
                    )
                    while self.is_listening:
                        try:
                            message = await self.websocket.recv()
                            print(f'message: {message}')
                            # if a handler was registered to respond to this type of message, call it
                            # otherwise cause the default handler
                        except Exception as e:
                            print(e)
                            self.websocket = None
                            break
            except:
                async_io.sleep(1)
                self.websocket = None


