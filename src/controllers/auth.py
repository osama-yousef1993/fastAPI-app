from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from src.services.auth import Authentication_Services
from src.types.auth import Login, LoginResponse, VerifyAccountResponse, VerifyOTP
from src.types.user import DefaultResponse, Signup

# Create an API router
AuthenticationRouter = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@AuthenticationRouter.post(
    "/signup/", response_model=DefaultResponse, tags=["Authentication"]
)
async def create_user(data: Signup) -> JSONResponse:
    endpoint = "signup"
    try:
        obj_Operations = Authentication_Services(endpoint=endpoint)
        content, status_code = obj_Operations.signup(user=data)
        return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@AuthenticationRouter.get(
    "/verify-account/{token}",
    response_model=VerifyAccountResponse,
    tags=["Authentication"],
)
async def verify_account(token) -> JSONResponse:
    endpoint = "verify-account"
    # try:
    obj_Operations = Authentication_Services(endpoint=endpoint)
    content, status_code = obj_Operations.account_verification(token=token)
    return JSONResponse(status_code=status_code, content=content)


# except Exception:
#     content = {
#         "detail": f"Internal server error occurred in the {endpoint} endpoint."
#     }
#     return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@AuthenticationRouter.post(
    "/login/", response_model=LoginResponse, tags=["Authentication"]
)
async def login(data: Login) -> JSONResponse:
    endpoint = "login"
    try:
        obj_Operations = Authentication_Services(endpoint=endpoint)
        content, status_code = obj_Operations.login(data=data)
        return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@AuthenticationRouter.post(
    "/verify-account-request/", response_model=LoginResponse, tags=["Authentication"]
)
async def verify_account_request(data: Login) -> JSONResponse:
    endpoint = "verify-account-request"
    try:
        obj_Operations = Authentication_Services(endpoint=endpoint)
        content, status_code = obj_Operations.verify_account_request(data=data)
        return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@AuthenticationRouter.post(
    "/verify-otp/", response_model=VerifyAccountResponse, tags=["Authentication"]
)
async def verify_otp(data: VerifyOTP) -> JSONResponse:
    endpoint = "verify-otp"
    obj_Operations = Authentication_Services(endpoint=endpoint)
    content, status_code = obj_Operations.verify_otp(
        email=data.email, user_otp=data.user_otp
    )
    return JSONResponse(status_code=status_code, content=content)


@AuthenticationRouter.get("/refresh-token")
async def refresh_token(token: str = Depends(oauth2_scheme)):
    endpoint = "refresh-token"
    try:
        obj_Operations = Authentication_Services(endpoint=endpoint)
        content, status_code = obj_Operations.refresh_token(token=token)
        return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)
