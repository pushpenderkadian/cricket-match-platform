from fastapi import APIRouter, WebSocket
from backend.database import live_collection
import asyncio
from backend.scraper import fetch_match_data

router = APIRouter()
connected_clients = {}
# WebSockets

 

@router.websocket("/live-updates/{match_id}")
async def websocket_endpoint(websocket: WebSocket, match_id: str):
    await websocket.accept()
    connected_clients[websocket] = match_id

    try:
        while True:
            match_data = live_collection.find_one({"match_id": match_id},{"_id": 0})
            if match_data:
                await websocket.send_json(match_data)
            else:
                await websocket.send_json(fetch_match_data(match_id))
            await asyncio.sleep(5)  # Fetch data every 5 seconds
    except Exception as e:
        print("WebSocket Disconnected:", e)
    finally:
        del connected_clients[websocket]