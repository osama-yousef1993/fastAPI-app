from io import BytesIO

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from src.helpers.helpers import get_current_user
from src.services.preprocessing import Preprocessing_Services
from src.services.validate import image_type_validate

PreprocessingRouter = APIRouter()


@PreprocessingRouter.post("/enhance-photo/")
async def enhance_photo(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "enhance-photo"
    try:
        # Validate Image type
        image_type_validate(image)

        # Read the image data
        image_data = await image.read()

        # Apply the photo enhancer function
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        enhanced_image_data = operation_object.photo_enhancer()

        # Return the enhanced image
        return StreamingResponse(
            BytesIO(enhanced_image_data), media_type=image.content_type
        )
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/remove-background/")
async def remove_background(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "remove-background"
    # try:
    # Validate Image type
    image_type_validate(image)
    # Read the image data
    image_data = await image.read()
    # Apply the remove background function
    operation_object = Preprocessing_Services(endpoint=endpoint, image_bytes=image_data)
    content = operation_object.remove_background()

    # Return the image
    return StreamingResponse(BytesIO(content), media_type=image.content_type)


# except Exception:
#     content = {"detail": f"Error in {endpoint} endpoint."}
#     return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/photo-colorizer/")
async def photo_colorizer(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "photo-colorizer"
    try:
        # Validate Image type
        image_type_validate(image)
        # Read the image data
        image_data = await image.read()
        # Apply the photo colorizer function
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        content = operation_object.photo_colorizer()
        # Return the image
        return StreamingResponse(BytesIO(content), media_type=image.content_type)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/face-extraction/")
async def face_extraction(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "face-extraction"
    try:
        # Validate Image type
        image_type_validate(image)
        # Read the image data
        image_data = await image.read()
        # Apply the face extraction function
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        content = operation_object.segment_face_and_hair()
        # Return the image
        return StreamingResponse(BytesIO(content), media_type=image.content_type)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/photo-color-correction/")
async def photo_color_correction(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "photo-color-correction"
    try:
        # Validate Image type
        image_type_validate(image)
        # Read the image data
        image_data = await image.read()
        # Apply the photo color correction function
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        content = operation_object.photo_color_correction()
        # Return the image
        return StreamingResponse(BytesIO(content), media_type=image.content_type)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/create-mask-image/")
async def create_mask_image(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "create-mask-image"
    try:
        # Validate Image type
        image_type_validate(image)
        # Read the image data
        image_data = await image.read()
        # Apply the create mask function
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        content = operation_object.create_mask_image()
        # Return the image
        return StreamingResponse(content, media_type=image.content_type)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)


@PreprocessingRouter.post("/enhance-photo-local/")
async def enhance_image_local(
    image: UploadFile = File(...), current_user: dict = Depends(get_current_user)
):
    endpoint = "enhance-photo-local"
    try:
        # Validate Image type
        image_type_validate(image)
        # Read the image data
        image_data = await image.read()
        # Get image
        operation_object = Preprocessing_Services(
            endpoint=endpoint, image_bytes=image_data
        )
        content = operation_object.enhance_image_local()
        # Return the image
        return StreamingResponse(content, media_type=image.content_type)
    except Exception:
        content = {"detail": f"Error in {endpoint} endpoint."}
        return JSONResponse(content=content, status_code=status.HTTP_409_CONFLICT)
