import asyncio
import json
import time
from aiohttp import web
import websockets
from websockets import ConnectionClosed
from websockets.protocol import State

WS_PORT = 8765
HTTP_PORT = 8766

# Shared WebSocket state and Queue
connected_socket = None
message_queue = asyncio.Queue()  # Queue for processing WebSocket messages


async def handle_connection(websocket):
    """
    Handles WebSocket connections from the browser.
    """
    global connected_socket
    print("Browser connected via WebSocket")
    connected_socket = websocket

    try:
        async for message in websocket:
            print(f"Received from browser extension: {message}")
            # Add message to the queue
            await message_queue.put(message)
    except ConnectionClosed as e:
        print("Browser connection closed:", e)
    finally:
        connected_socket = None
        print("Browser disconnected")


async def send_request_to_browser(request):
    """
    Sends a JSON-serializable request to the browser and waits for a JSON response.
    """
    global connected_socket

    # Check if the connection is active using state
    if not connected_socket or connected_socket.state != State.OPEN:
        return {"status": "error", "message": "No browser connected"}

    try:
        # Send request to the browser
        await connected_socket.send(json.dumps(request))
        print("Request sent to browser:", request)

        # Wait for response from the queue
        response = await message_queue.get()  # Safely get the next message
        response_data = json.loads(response)
        print("Response from browser:", response_data)
        return response_data
    except Exception as e:
        print("Error during communication with browser:", e)
        return {"status": "error", "message": str(e)}


# HTTP API route to handle external requests
async def chat_completions_handler(request):
    payload = await request.json()
    print("Received API request:", payload)

    chat_request = {
        "type": "message",
        "text": payload["text"],
    }

    # Send the request to the browser and await its response
    browser_response = await send_request_to_browser(chat_request)

    # Format response in pseudo-OpenAI API format
    formatted_response = {
        "id": "chatcmpl-" + str(int(time.time() * 1000)),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "pseudo-gpt",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": browser_response.get("content", "")
                },
                "finish_reason": "stop"
            }
        ]
    }
    return web.json_response(formatted_response)


async def main():
    global connected_socket

    # Start WebSocket server
    ws_server = websockets.serve(handle_connection, "localhost", WS_PORT)
    await ws_server
    print(f"WebSocket server running at ws://localhost:{WS_PORT}")

    # Start HTTP server
    app = web.Application()
    app.router.add_post("/v1/chat/completions", chat_completions_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    http_site = web.TCPSite(runner, "localhost", HTTP_PORT)
    await http_site.start()
    print(f"HTTP server running at http://localhost:{HTTP_PORT}/v1/chat/completions")

    # Keep servers running indefinitely
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
