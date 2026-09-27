"""
WebSocket event handlers.
"""

import logging
from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.manager import manager

logger = logging.getLogger(__name__)


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.info(f"Received WebSocket message: {data}")
            # Echo back for now (can be extended for bidirectionality)
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket disconnected")







