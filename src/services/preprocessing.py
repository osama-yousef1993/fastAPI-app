import requests
from fastapi import HTTPException, status
from src.services.base import Base_Services
from src.utils.config import API_BASE_URL, API_KEY
from PIL import Image, ImageEnhance
import io
import logging


class Preprocessing_Services(Base_Services):
    
    def __init__(self, image_bytes, endpoint):
        super().__init__()
        self.endpoint = endpoint
        self.api_base_url = API_BASE_URL
        self.api_key = API_KEY
        self.image = image_bytes
        self.image_formats = ["PNG", "JPEG", "GIF", "BMP", "TIFF", "ICO", "WEBP", "PDF", 
                              "EPS", "PCX", "PPM"]
     
    
    def photo_enhancer(self):
        """
        Enhances the quality of photos that have issues such as bad focus, low resolution, blurriness, pixelation, or damage.
        Transforms every photo into a high-definition version with sharp focus.
        Raises:
            Exception: If the request to the enhancement API fails.
        """
        try:
            endpoint = "/api/v1/photoEnhance"
            response = requests.post(
                self.api_base_url + endpoint,
                files={"file": self.image},
                headers={"APIKEY": self.api_key},
            )
            response.raise_for_status()  # This will raise an exception for HTTP error codes
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while enhancing the photo: {e}")

    def remove_background(self,):
        """
        Automatically recognizes the foreground in the image, separates it from the background,
        and returns a transparent image (foreground colors along with the alpha matte).
        This function works for images with a distinguishable foreground
        (e.g., people, animals, products, cartoons).

        Parameters:
        img (bytes or file-like object): The image data or a file-like object containing the image.
        Returns:
            bytes: The image data with the background removed.
        Raises:
            Exception: If there's an error with the API request or if the input is not in the expected format.
        """
        try:
            endpoint = "/api/v1/matting?mattingType=6"
            response = requests.post(
                self.api_base_url + endpoint,
                files={"file": self.image},
                headers={"APIKEY": self.api_key},
                )
            response.raise_for_status()  # Checks for HTTP errors and raises an exception if found
            return response.content
        except requests.exceptions.RequestException as e:
            # Rethrow with a more descriptive error message
            raise Exception(f"An error occurred while removing the background: {e}")

    def photo_colorizer(self,):
        """
        Colorizes black and white photos using advanced AI algorithms. This function is ideal for
        enhancing old family photos, historical figure portraits, and any black and white images that
        could benefit from realistic coloring. It provides a way to restore and refresh memories with
        stunning colors through a few clicks.
        Parameters:
            img (bytes or file-like object): The black and white image data or a file-like object containing the image to be colorized.
        Returns:
            bytes: The colorized image data.
        Raises:
            ValueError: If 'img' is neither bytes nor a file-like object.
            Exception: If there's an error with the API request.
        """
        try:
            endpoint = "/api/v1/matting?mattingType=19"
            response = requests.post(
                self.api_base_url + endpoint,
                files={"file": self.image},
                headers={"APIKEY": self.api_key},
            )
            response.raise_for_status()  # This will raise an exception for HTTP error codes
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while colorizing the photo: {e}")

    def segment_face_and_hair(self,):
        """
        Segments the face and hair from a photo, returning the result as image data.
        This method is highly accurate and fast, making it suitable for various applications
        such as print-on-demand services, creating emojis, avatars, and headshot profile pictures.
        Parameters:
            image_data (bytes or file-like object): The image data to process.
        Returns:
            bytes: The processed image data with the background removed, focusing on the face and hair.
        Raises:
            Exception: If the API call fails or there's a problem processing the image.
        """
        endpoint = "/api/v1/matting?mattingType=3"
        try:
            response = requests.post(
                f"{self.api_base_url}{endpoint}",
                files={"file": self.image},
                headers={"APIKEY": self.api_key},
            )
            response.raise_for_status()  # Ensure the API request was successful
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"An error occurred during the face and hair segmentation process: {e}"
            )

    def photo_color_correction(self):
        """
        Apply AI-driven color correction to an image.
        This function communicates with a remote API to perform color correction on an image. 
        It adjusts the colors by removing color casts and enhancing clarity and vibrancy,
        making the image colors more accurate to how they are perceived in real life.
        Raises:
            Exception: If the API call fails or the server returns an error.
        Returns:
            bytes: The corrected image data in binary format, which can also be saved locally.
        """
        endpoint = "/api/v1/matting?mattingType=4"
        try:
            # Prepare and send a POST request to the API with the image data and API key
            response = requests.post(
                f"{self.api_base_url}{endpoint}",
                files={"file": self.image},
                headers={"APIKEY": self.api_key},
            )
            response.raise_for_status()  # Raises an HTTPError for bad requests (4XX or 5XX)
            return response.content  # Return the binary content of the corrected image
        except requests.exceptions.RequestException as e:
            # Handle exceptions from the request and provide a user-friendly message
            raise Exception(
                f"An error occurred during the photo color correction process: {e}"
            )

    def create_mask_image(self):
        """
        Creates a black mask image with the same dimensions as the input image.
        Returns:
            Image: A new black image of the same size as self.image.
        Raises:
            Exception: If there is an error during the image creation process.
        """
        try:
            # Create a black image with the same dimensions as the input image
            image = Image.open(io.BytesIO(self.image))
            black_image= Image.new('RGB', image.size, (0, 0, 0))
            # Prepare the image to send as a response
            img_byte_arr = io.BytesIO()
            black_image.save(img_byte_arr, format='PNG')
            img_byte_arr = io.BytesIO(img_byte_arr.getvalue())
            return img_byte_arr
        except AttributeError as e:
            # Handle exceptions related to image attribute access
            raise Exception(
                f"An error occurred during the mask creation process: {str(e)}"
            )
            
    def enhance_image_local(self):
        """
        Converts byte data into a PIL Image object.
        Args:
            byte_data (bytes): The image data in bytes.
        Returns:
            Image: A PIL Image object if conversion is successful, None otherwise.
        """
        try:
            image = Image.open(io.BytesIO(self.image))
         
            # Brightness enhancement
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.2)  # Adjust the factor to taste
            
            # Contrast enhancement
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)  # Adjust the factor to taste
            
            # Sharpness enhancement
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)  # Adjust the factor to taste

            # Color balance (saturation)
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.5)  # Adjust the factor to taste
        
            # Prepare the image to send as a response
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = io.BytesIO(img_byte_arr.getvalue())
            return img_byte_arr
        except Exception as e:
            print(f"Failed to convert bytes to image: {e}")
            return None
    
cutout_error_code={
    0: "Request succeeded",
    1001: "Request failed, used for unclassified errors, the “msg” field displays specific error information",
    1002: "File size exceeded maximum limit(15M)",
    4001: "Insufficient credits",
    4002: "File does not exist",
    5002: "Invalid api key",
    5003: "Image processing failed",
    5004: "Picture download failed",
    5005: "Too many requests in the queue, please wait",
    5006: "Invalid base64 encoded string",
    5007: "The base64 encoded string cannot be correctly recognized as a picture. Some java libraries have problem with the base64 line feed symbol (‘\n’), and it needs to be removed",
    5008: "Cannot recognize input image correctly"}