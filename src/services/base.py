import smtplib
import uuid
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from passlib.context import CryptContext
from PIL import Image

from src.utils.config import (
    EMAIL_SENDER_ADDRESS,
    EMAIL_SENDER_PASSWORD,
    EMAIL_SMTP_PORT,
    EMAIL_SMTP_SERVER,
)


class Base_Services:
    def __init__(
        self,
    ):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Function to send email (customize with your SMTP settings)

    def send_email(self, recipient_email, subject, html_content=None, body=""):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER_ADDRESS
        msg["To"] = recipient_email

        # Attach HTML content using MIMEText
        if html_content:
            msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER_ADDRESS, EMAIL_SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

    def read_image(image_path) -> Image:
        """
        Reads an image from the specified path and returns the image object.
        Parameters:image_path (str): The path to the image file.
        Returns: PIL.Image.Image: The image object.
        """
        try:
            img = Image.open(image_path)
            return img
        except IOError:
            print(
                f"Error opening the image file at {image_path}. Please check the file path and try again."
            )
            return None

    def copy_image(img, copy_path) -> None:
        """
        Creates a copy of the given image object and saves it to the specified path.
        Parameters:
            img (PIL.Image.Image): The image object to be copied.
            copy_path (str): The path where the copy of the image will be saved.
        """
        if img is not None:
            img.save(copy_path)
            print(f"Image successfully copied to {copy_path}.")
        else:
            print("No image to copy.")

    def save_image(self, folder: str, image_data, image_name: str):
        """
        Saves an image to a specified folder.
        Parameters:
        - folder: The target folder ('inputs' or 'outputs').
        - image_data: The binary content of the image to be saved.
        - image_name: The name under which the image should be saved.
        Returns:
        - The path to the saved image or None if the operation fails.
        """
        try:
            # Ensure the target directory exists
            target_path = Path(folder)
            target_path.mkdir(parents=True, exist_ok=True)
            # Define the full path for the new image
            image_path = target_path / image_name
            # Write the image data to a file
            with open(image_path, "wb") as image_file:
                image_file.write(image_data)
            print(f"Image saved successfully to {image_path}")
            return str(image_path)
        except Exception as e:
            print(f"Failed to save the image. Error: {e}")
            return None

    def generate_image_name_uuid(extension: str = ".jpg") -> str:
        """
        Generates a unique image name using UUID.

        Parameters:
        - extension: The file extension for the image name.

        Returns:
        - A unique image name with the specified extension.
        """
        return f"{uuid.uuid4()}{extension}"

    def generate_image_name_timestamp(
        prefix: str = "image", extension: str = ".jpg"
    ) -> str:
        """
        Generates a unique image name using a timestamp and a prefix.

        Parameters:
        - prefix: A prefix for the image name.
        - extension: The file extension for the image name.

        Returns:
        - A unique image name with the specified prefix and extension.
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S%f")
        return f"{prefix}_{timestamp}{extension}"
