import asyncio
import websockets
import json

async def receive_data(websocket, path):
    print(f"New connection established: {websocket.remote_address}")
    print("\n")
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)
    except websockets.exceptions.ConnectionClosed:
        print("\n")
        print(f"Connection closed: {websocket.remote_address}")

if __name__ == "__main__":
    start_server = websockets.serve(receive_data, "localhost", 8765)

    print("WebSocket server started. Waiting for connections...")
    print("\n")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
