"""
Dependency injection for FastAPI routes.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


def get_database() -> Generator[Session, None, None]:
    """Get database session dependency."""
    yield from get_db()


def require_admin():
    """
    Dependency factory to require admin role.
    Returns a dependency that raises 403 Forbidden if user is not an admin.
    
    Note: Uses lazy import to avoid circular dependency with auth.py
    """
    # Lazy import to avoid circular dependency - import inside function
    from app.api.routes.auth import get_current_user
    from fastapi import Depends as FastAPIDepends
    
    async def _require_admin(current_user: User = FastAPIDepends(get_current_user)) -> User:
        if current_user.role.lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required. Only administrators can view mitigation logs."
            )
        return current_user
    
    return FastAPIDepends(_require_admin)

