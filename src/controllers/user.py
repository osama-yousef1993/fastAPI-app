from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.helpers.helpers import get_current_user
from src.services.user import User_Services
from src.types.user import DefaultResponse, ResetPassword, UpdatePassword, User

UserRouter = APIRouter()


@UserRouter.get("/user-info/", response_model=DefaultResponse, tags=["User"])
async def read_info(current_user: dict = Depends(get_current_user)) -> JSONResponse:
    endpoint = "user-info"
    try:
        obj_Operations = User_Services(endpoint=endpoint)
        content, status_code = obj_Operations.UserInfo(email=current_user["sub"])
        return JSONResponse(
            status_code=status_code, content=jsonable_encoder(User(**dict(content)))
        )
    except Exception as e:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint. with error {e}"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@UserRouter.post("/forget-password/", response_model=DefaultResponse, tags=["User"])
async def forget_password(data: ResetPassword) -> JSONResponse:
    endpoint = "forget-password"
    obj_Operations = User_Services(endpoint=endpoint)
    content, status_code = obj_Operations.forget_password(data.email)
    return JSONResponse(status_code=status_code, content=content)


@UserRouter.put("/update-password/", response_model=DefaultResponse, tags=["User"])
async def update_password(
    user_req: UpdatePassword, current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    endpoint = "update-password"
    try:
        obj_Operations = User_Services(endpoint=endpoint)
        content, status_code = obj_Operations.UserInfo(current_user["sub"])
        if status_code == 200:
            content, status_code = obj_Operations.UpdateUserPassword(
                current_user["sub"], user_req
            )
            return JSONResponse(status_code=status_code, content=content)
        else:
            return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@UserRouter.put(
    "/update-password-by-otp/", response_model=DefaultResponse, tags=["User"]
)
async def update_password_by_otp(
    user_req: UpdatePassword, current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    endpoint = "update-password"
    try:
        obj_Operations = User_Services(endpoint=endpoint)
        content, status_code = obj_Operations.UserInfo(current_user["sub"])
        if status_code == 200:
            content, status_code = obj_Operations.UpdateUserPasswordByOTP(
                current_user["sub"], user_req
            )
            return JSONResponse(status_code=status_code, content=content)
        else:
            return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@UserRouter.delete("/delete-account/", response_model=DefaultResponse, tags=["User"])
async def delete_account(
    user_req: ResetPassword, current_user: dict = Depends(get_current_user)
) -> JSONResponse:
    endpoint = "delete-account"
    try:
        obj_Operations = User_Services(endpoint=endpoint)
        content, status_code = obj_Operations.UserInfo(user_req.email)
        if status_code == 200:
            content, status_code = obj_Operations.DeleteUser(user_req.email)
            return JSONResponse(status_code=status_code, content=content)
        else:
            return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {
            "detail": f"Internal server error occurred in the {endpoint} endpoint."
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)


@UserRouter.get("/credit-balance/")
async def credit_balance(current_user: dict = Depends(get_current_user)):
    endpoint = "credit-balance"
    try:
        # Apply the photo enhancer function
        operation_object = User_Services(endpoint=endpoint)
        content, status_code = operation_object.fetch_credit_balance()
        return JSONResponse(status_code=status_code, content=content)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)
