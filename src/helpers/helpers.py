from typing import Any, Dict

from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from src.utils.config import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Security(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # Or load user from payload data, e.g., email or user ID


# Helper function to convert Pydantic models to dictionaries
def model_to_dict(obj: BaseModel) -> Dict[str, Any]:
    result = obj.__dict__
    for key, value in result.items():
        if isinstance(value, BaseModel):
            result[key] = model_to_dict(value)

        elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
            result[key] = [model_to_dict(item) for item in value]

    return result
