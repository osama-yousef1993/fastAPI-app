import base64
import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.utils.check_file import check_file_exist


class User(BaseModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    profiles: Optional[str] = None


class ResetPassword(BaseModel):
    email: EmailStr = None


class UpdatePassword(BaseModel):
    re_password: str = Field(min_length=8, description="At least 8 characters")
    old_password: str = Field(min_length=8, description="At least 8 characters")
    new_password: str = Field(min_length=8, description="At least 8 characters")
    otp: int

    @field_validator("re_password")
    def password_complexity(cls, value):
        # Ensures password has at least one digit, one uppercase and one lowercase character
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one digit, one uppercase and one lowercase character"
            )
        return value

    @field_validator("old_password")
    def password(cls, value):
        # Ensures password has at least one digit, one uppercase and one lowercase character
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one digit, one uppercase and one lowercase character"
            )
        return value

    @field_validator("new_password")
    def new_password_c(cls, value):
        # Ensures password has at least one digit, one uppercase and one lowercase character
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one digit, one uppercase and one lowercase character"
            )
        return value


class Signup(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, description="At least 8 characters")
    profiles: Optional[str] = None

    @field_validator("password")
    def password_complexity(cls, value):
        # Ensures password has at least one digit, one uppercase and one lowercase character
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one digit, one uppercase and one lowercase character"
            )
        return value

    # =>> Add validator email
    @field_validator("email")
    def validate_email(cls, value):
        if not value.endswith("@caesarfamilies.info"):
            raise ValueError("Email must belong to caesar domain")
        return value

    # # ToDo Check Build
    @field_validator("profiles", mode="after", check_fields=True)
    def validate_image_url(cls, value):
        # Validates if the profiles URL is a valid URL and points to an image (.jpg, .jpeg, .png, etc.)
        if value is not None:
            # Simple regex for URL validation
            # pattern = re.compile(
            #     r"^(?:http|ftp)s?://"  # http:// or https://
            #     r"(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
            #     r"(?:\.(?:jpg|jpeg|png|gif))$",
            #     re.IGNORECASE,
            # )
            image_data_pattern = re.compile(
                r"data:image\/(.?:jpg|jpeg|png|gif);base64,(.*)"
            )
            image_type = value.split("/", 1)[1].split(";", 1)[0]
            match = image_data_pattern.match(value)
            image_base64 = match.group(2)
            image_bin = base64.b64decode(image_base64)
            path = "src/static/profiles"
            check_file_exist(path)
            image_url = f"{path}/uploaded_image.{image_type}"
            with open(image_url, "wb") as f:
                f.write(image_bin)
            pattern = re.compile(
                r"data:image\/(jpeg|jpg|png|gif);base64",
                re.IGNORECASE,
            )
            if not pattern.match(value):
                raise ValueError(
                    "Profiles must be a valid image URL ending with .jpg, .jpeg, .png, or .gif"
                )
        return image_url


class DefaultResponse(BaseModel):
    detail: str
