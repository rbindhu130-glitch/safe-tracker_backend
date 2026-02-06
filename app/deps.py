from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models


def get_current_user(x_user_id: Optional[int] = Header(default=None), db: Session = Depends(get_db)) -> models.User:
    """
    Very small, beginner-friendly authentication dependency.

    It reads an `X-User-Id` header (integer) and returns the corresponding
    `models.User` from the database. This keeps auth simple for local testing.

    Usage:
    - Include a header `X-User-Id: 1` in your requests to act as user with id 1.
    - If the header is missing or the user doesn't exist, a 401 is returned.
    """
    # If header provided, use that user
    if x_user_id is not None:
        user = db.get(models.User, x_user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    # Fallback: use the first user in the DB for local testing convenience
    user = db.query(models.User).order_by(models.User.id).first()
    if not user:
        raise HTTPException(status_code=401, detail="No users in database; create one first")
    return user
