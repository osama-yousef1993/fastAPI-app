import random
import time
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jinja2 import Environment, FileSystemLoader
from jose import JWTError, jwt

from src.queries.users import UserQuery
from src.services.base import Base_Services
from src.utils.config import (
    ACCESS_TOKEN_EXPIRE_HOURS,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    TEMPLATES_PATH,
    VERIFY_TEMPLATE,
    VERIFY_TOKEN_EXPIRE_MINUTES,
    Domain_BASE_URL,
)


class Authentication_Services(Base_Services):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint

    def signup(self, user):
        # Prepare user Data
        user_data = user.dict()
        user_data["password"] = self.pwd_context.hash(
            user.password
        )  # Hash the password
        user_data["otp"] = random.randint(100000, 999999)
        user_data["is_verified"] = False
        # check if user exists.
        user_result = UserQuery.check_user(user_data)
        if user_result:
            # Add user to database.
            _ = UserQuery.add_user_to_database(user_data)
            # Create Activation Token
            expires_delta = timedelta(minutes=VERIFY_TOKEN_EXPIRE_MINUTES)
            payload = {"email": user_data["email"], "otp": user_data["otp"]}
            token = self.create_access_token(data=payload, expires_delta=expires_delta)
            # Send Activation Template
            self.send_activation_request(
                first_name=user_data["first_name"],
                recipient_email=user_data["email"],
                verification_link=f"{Domain_BASE_URL}/auth/activate/{token}",
            )
            return {"detail": "User added successfully."}, status.HTTP_201_CREATED
        return {"detail": "User already exists."}, status.HTTP_409_CONFLICT

    def send_activation_request(
        self, first_name, recipient_email, verification_link=""
    ):
        # Email Info
        subject = "Verify Your ClarityKit Account"
        # Prepare Data
        data = {
            "first_name": first_name,
            "verification_link": verification_link,
            "expire_minutes": VERIFY_TOKEN_EXPIRE_MINUTES,
        }
        try:
            # Set up the Jinja2 environment with the directory containing the HTML file
            env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
            # Load the HTML template
            template = env.get_template(VERIFY_TEMPLATE)
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

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        # to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        data["exp"] = expire
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return (
                decoded
                if decoded.get("exp") > datetime.now(timezone.utc).timestamp()
                else None
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Oops! Your token has expired.",
            )

    def account_verification(self, token: str):
        payload = self.decode_access_token(token)
        user = UserQuery.get_user_data(payload["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found."
            )

        elif user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account already verified.",
            )

        elif self.is_token_expired(payload["exp"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification link has expired.",
            )
        user_data = dict()
        user_data["is_verified"] = True
        user_data["email"] = user.email
        _ = UserQuery.update_user_data(user_data)
        content = self.create_token(user.email)
        content["detail"] = "Account verified successfully."
        return content, status.HTTP_202_ACCEPTED

    def is_token_expired(self, exp_timestamp):
        # Get the current time as a Unix timestamp
        current_timestamp = int(time.time())
        # Calculate the difference in seconds
        difference = exp_timestamp - current_timestamp
        # Check if the difference is less than 900 seconds (15 minutes)
        return difference < 0

    def login(self, data):
        user_data = UserQuery.authenticate_user(email=data.email)
        if not self.pwd_context.verify(data.password, user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        content = self.create_token(email=data.email)
        return content, status.HTTP_202_ACCEPTED

    def verify_account_request(self, data):
        user_data = UserQuery.authenticate_user(email=data.email)
        if not self.pwd_context.verify(data.password, user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user_data.is_verified:
            expires_delta = timedelta(minutes=VERIFY_TOKEN_EXPIRE_MINUTES)
            payload = {"email": user_data.email, "otp": user_data.otp}
            token = self.create_access_token(data=payload, expires_delta=expires_delta)
            self.send_activation_request(
                first_name=user_data["first_name"],
                recipient_email=user_data.email,
                verification_link=f"{Domain_BASE_URL}/auth/activate/{token}",
            )
        return {
            "details: Please Check your Email to Confirm your Account"
        }, status.HTTP_200_OK

    def create_token(self, email):
        expires_delta = timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS, minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.create_access_token(
            data={"sub": email}, expires_delta=expires_delta
        )
        content = {"access_token": access_token, "token_type": "bearer"}
        return content

    def refresh_token(self, token: str):
        # Decode the existing token
        payload = self.decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Extract user identity from token payload
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user information",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Create a new token
        new_token = self.create_access_token(data={"sub": username})
        content = {"access_token": new_token, "token_type": "bearer"}
        return content, status.HTTP_202_ACCEPTED

    def verify_otp(self, email, user_otp):
        # Retrieve the user by email
        user = UserQuery.get_user_data(email=email)
        # date_format = "%Y-%m-%d %H:%M:%S.%f%z"
        # otp_expiration_time = datetime.strptime(
        #     str(user.otp_expiration_time), date_format
        # )
        # local_datetime = datetime.strptime(
        #     str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f"
        # )

        # Check if the OTP matches and is still valid
        if not user:
            content = {"detail": "Incorrect username or password."}
            return content, status.HTTP_401_UNAUTHORIZED

        elif user.otp_expiration_time < datetime.now(timezone.utc):
            content = {"detail": "Oops! your OTP code has expired."}
            return content, status.HTTP_400_BAD_REQUEST

        if user.otp == user_otp:
            user_data = dict()
            user_data["is_verified"] = True
            user_data["email"] = email
            UserQuery.update_user_data(user_data)
            content = self.create_token(email)
            content["detail"] = "Account verified successfully."
            return content, status.HTTP_202_ACCEPTED
        else:
            content = {
                "detail": "The OTP you entered is invalid. Please check your entry and try again."
            }
            return content, status.HTTP_400_BAD_REQUEST
