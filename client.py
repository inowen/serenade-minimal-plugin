import asyncio as async_io
import json
import websockets
import random

id = str(random.random())
websocket = None


async def send(message, data):
    if not websocket:
        return
    await websocket.send(json.dumps({"message": message, "data": data}))


# send a heartbeat to serenade every few seconds to keep the connection alive
# (only if there is a connection)
async def send_heartbeat():
    while True:
        if websocket:
            # print("Sending heartbeat")
            await send("heartbeat", {"id": id})
        await async_io.sleep(5)



async def message_handler():
    global websocket

    async_io.create_task(send_heartbeat())
    while True:
        try:
            async with websockets.connect("ws://localhost:17373") as ws:
                websocket = ws
                print("Connected")

                # send an active message to tell Serenade we're running. since this is running from a terminal,
                # use "term" as the match regex, which will match iTerm, terminal, etc.
                await send(
                    "active",
                    {"id": id, "app": "minimal_client", "match": "client"},
                )

                while True:
                    try:
                        message = await websocket.recv()
                        print(message)
                    except:
                        print("Disconnected")
                        websocket = None
                        break
        except OSError:
            websocket = None
            await async_io.sleep(1)


if __name__ == "__main__":
    print("minimal client is running")
    async_io.get_event_loop().run_until_complete(message_handler())