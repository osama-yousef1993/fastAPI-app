import json
import random
from datetime import datetime, timedelta, timezone

import requests
from fastapi import HTTPException, status
from jinja2 import Environment, FileSystemLoader

from src.queries.users import UserQuery
from src.services.base import Base_Services
from src.utils.config import (
    API_BASE_URL,
    API_KEY,
    PASSWORD_RESET_TEMPLATE,
    PASSWORD_REST_OTP_EXPIRE_MINUTES,
    TEMPLATES_PATH,
)
from src.utils.map_helper import build_users_dict


class User_Services(Base_Services):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint
        self.api_base_url = API_BASE_URL
        self.api_key = API_KEY

    def forget_password(self, email):
        # Check User Exist
        user = UserQuery.get_user_data(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The provided email address is not found.",
            )

        # Update User Data
        user_data = dict()
        user_data["email"] = user.email
        user_data["otp"] = random.randint(100000, 999999)  # Generate OTP
        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=PASSWORD_REST_OTP_EXPIRE_MINUTES
        )
        user_data["otp_expiration_time"] = expiration_time
        user_result = UserQuery.update_user_data(user_data)
        if not user_result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to update user data with the new OTP. Please try again or contact support",
            )
        self.send_password_reset_request(
            first_name=user.first_name,
            recipient_email=user.email,
            otp=user_data["otp"],
            reset_link="....",
        )
        return {
            "detail": "OTP sent successfully to your email address."
        }, status.HTTP_200_OK

    def send_password_reset_request(
        self, first_name, recipient_email, otp, reset_link=""
    ):
        # Email Info
        subject = "Password Reset Request"
        # Prepare Data
        data = {
            "first_name": first_name,
            "otp": otp,
            "expire_minutes": PASSWORD_REST_OTP_EXPIRE_MINUTES,
        }
        try:
            # Set up the Jinja2 environment with the directory containing the HTML file
            env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
            # Load the HTML template
            template = env.get_template(PASSWORD_RESET_TEMPLATE)
            # Render the template with the data
            rendered_html = template.render(data)
        except FileNotFoundError:
            print("The email template file was not found.")
            return
        try:
            self.send_email(
                recipient_email=recipient_email,
                subject=subject,
                html_content=rendered_html,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return

    def UserInfo(self, email):
        # Add your logic to store the user in your database
        # For demonstration, this is just a placeholder function call
        user_result = UserQuery.get_user_data(email)
        if user_result:
            data = build_users_dict(user_result)
            return data, status.HTTP_200_OK
        return {"detail": "User doesn't Exist."}, status.HTTP_406_NOT_ACCEPTABLE

    def UpdateUserPassword(self, email, user_data):
        if user_data.re_password == user_data.new_password:
            # Add your logic to store the user in your database
            # For demonstration, this is just a placeholder function call
            hashed_password = self.pwd_context.hash(user_data.new_password)
            user_data = dict()
            user_data["email"] = email
            user_data["password"] = hashed_password
            user_result = UserQuery.update_user_data(user_data)
            if user_result:
                return build_users_dict(user_result, "update"), status.HTTP_200_OK
        return {
            "detail": "User doesn't Updated successfully."
        }, status.HTTP_400_BAD_REQUEST

    def UpdateUserPasswordByOTP(self, email, user_data):
        if user_data.re_password == user_data.new_password:
            # Add your logic to store the user in your database
            # For demonstration, this is just a placeholder function call
            hashed_password = self.pwd_context.hash(user_data.new_password)
            user_data = dict()
            user_data["email"] = email
            user_data["password"] = hashed_password
            user_data["otp"] = user_data.otp
            user_data["is_verified"] = True
            user_result = UserQuery.update_user_data(user_data)
            if user_result:
                return build_users_dict(user_result, "update"), status.HTTP_200_OK
        return {
            "detail": "User doesn't Updated successfully."
        }, status.HTTP_400_BAD_REQUEST

    def DeleteUser(self, email):
        # Add your logic to store the user in your database
        # For demonstration, this is just a placeholder function call
        user_data = dict()
        user_data["email"] = email
        user_data["deleted_at"] = datetime.now(timezone.utc)
        user_data["is_verified"] = False
        user_result = UserQuery.update_user_data(user_data)
        if user_result:
            return {
                "detail": "User Account Deleted Successfully."
            }, status.HTTP_202_ACCEPTED
        return {
            "detail": "User Account doesn't Deleted successfully."
        }, status.HTTP_400_BAD_REQUEST

    def fetch_credit_balance(self):
        """
        Get current credit balance through API.
        """
        try:
            endpoint = "/api/v1/mySubscription"
            response = requests.get(
                self.api_base_url + endpoint,
                headers={"APIKEY": self.api_key},
            )
            response.raise_for_status()  # This will raise an exception for HTTP error codes
            response_str = response.content.decode(encoding="utf-8")  #
            balance = int(json.loads(response_str)["data"]["monthBalance"])
            content = {"credits": balance}
            return content, status.HTTP_200_OK
        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while enhancing the photo: {e}")
