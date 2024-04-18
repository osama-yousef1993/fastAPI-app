from fastapi import HTTPException


def image_type_validate(image):
    # Validate image format (for this example, we're only allowing JPEGs)
    if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please upload a JPEG, JPG, or PNG image.",
        )
