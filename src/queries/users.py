from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select

from src.database.connection import execute_one
from src.database.database import ALL_COLUMNS
from src.models.user import users


class UserQuery:
    def authenticate_user(
        email: str,
    ) -> bool:
        query = users.select().where(users.c.email == email)
        row = execute_one(query)  # Ensure execute_one is designed for async
        if not row:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )
        return row

    @staticmethod
    def check_user(user_data: dict):
        try:
            query = users.select().where(users.c.email == user_data["email"])
            result = execute_one(query)
            # if the result return empty or false this mean the user not exist
            if not result:
                return True
            return False
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not exist",
            )

    @staticmethod
    def get_user_data(email):
        try:
            query = select(
                users.c.first_name,
                users.c.last_name,
                users.c.email,
                users.c.profiles,
                users.c.otp,
                users.c.otp_expiration_time,
                users.c.is_verified
            ).where(users.c.email == email)
            result = execute_one(query)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not exist",
                )
            return result
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not register user",
            )

    @staticmethod
    def update_user_data(user: dict):
        try:
            query = (
                users.update()
                .where(users.c.email == user["email"])
                .values(dict(user))
                .returning(ALL_COLUMNS)
            )
            result = execute_one(query)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User not Updated",
                )
            return result
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not Update user",
            )

    @staticmethod
    def add_user_to_database(user_data: dict):
        try:
            query = users.insert().values(dict(user_data)).returning(ALL_COLUMNS)
            # Assuming insert_object is async and returns the new primary key.
            # You need to pass the query, not just values, and must be awaited if it's async.
            new_user_data = execute_one(query)
            return new_user_data
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not register user",
            )
