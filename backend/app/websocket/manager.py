"""
WebSocket connection manager for real-time updates.
"""

import logging
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_progress_update(
        self,
        test_run_id: str,
        status: str,
        progress_percentage: float,
        current_step: str,
        total_profiles: int,
        processed_profiles: int
    ):
        """Send a progress update to all connected clients."""
        message = {
            "type": "progress_update",
            "data": {
                "test_run_id": test_run_id,
                "status": status,
                "progress_percentage": progress_percentage,
                "current_step": current_step,
                "total_profiles": total_profiles,
                "processed_profiles": processed_profiles,
                "timestamp": datetime.now().isoformat()
            }
        }
        await self.broadcast(message)
    
    async def send_metrics_update(
        self,
        test_run_id: str,
        metrics: Dict[str, Any]
    ):
        """Send metrics update to all connected clients."""
        message = {
            "type": "metrics_update",
            "data": {
                "test_run_id": test_run_id,
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
        }
        await self.broadcast(message)


# Global connection manager instance
manager = ConnectionManager()







