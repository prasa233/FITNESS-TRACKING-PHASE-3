
from datetime import datetime, timedelta, timezone
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret")
ALGORITHM = "HS256"
TOKEN_MINUTES = 60

security = HTTPBearer()


def hash_password(password: str) -> str:
    from passlib.context import CryptContext

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    from passlib.context import CryptContext

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
