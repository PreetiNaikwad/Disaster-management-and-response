import asyncio
import websockets

async def handle_client(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Server received: {message}")
    except:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()