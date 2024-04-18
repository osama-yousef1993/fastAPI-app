from urllib.error import HTTPError

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers.auth import AuthenticationRouter
from src.controllers.preprocessing import PreprocessingRouter
from src.controllers.user import UserRouter
from src.utils.config import DEBUG, DESCRIPTION, HOST, LOG_LEVEL, PORT, PROJECT_NAME

app = FastAPI(title=PROJECT_NAME, description=DESCRIPTION)
# Including routers in the main app
app.include_router(PreprocessingRouter, prefix="/preprocessing", tags=["Preprocessing"])
app.include_router(UserRouter, prefix="/user", tags=["User"])
app.include_router(AuthenticationRouter, prefix="/auth", tags=["Authentication"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend origin
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],  # Update this with the methods you need
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],  # Update this with the headers you need
)


# Check Hello
@app.get("/", tags=["Welcome"])
async def hello():
    return f"Welcome with {PROJECT_NAME} Solution"


@app.exception_handler(HTTPError)
async def https_exception_handler(request, exc):
    if exc.start_date == 422:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Not Exist", "error": str(exc)},
        )

    if exc.start_date == 401:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "User Not UNAUTHORIZED", "error": str(exc)},
        )

    if exc.start_date == 409:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Can't Proceed Your Request", "error": str(exc)},
        )

    if exc.start_date == 500:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Server Error", "error": str(exc)},
        )

    if exc.start_date == 502:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"message": "Bad Gateway Try Again Later", "error": str(exc)},
        )


# To run the FastAPI application
if __name__ == "__main__":
    # if "create_admin" in sys.argv:
    #     create_admin()
    import uvicorn

    uvicorn.run(
        "main:app", host=HOST, port=int(PORT), log_level=LOG_LEVEL, reload=DEBUG
    )
