from os import getenv

from dotenv.main import load_dotenv
from termcolor import colored

load_dotenv()

# ---------- Project Details ----------
PROJECT_NAME = getenv("PROJECT_NAME", "Phonetics")
DESCRIPTION = getenv("DESCRIPTION")
Company_Name = "Caesar Family"

# ---------- Flask Config ----------

HOST = getenv("HOST", "0.0.0.0")
PORT = getenv("PORT", "8888")
DEBUG = bool(getenv("DEBUG", False))
VERSION = getenv("VERSION")
LOG_LEVEL = getenv("LOG_LEVEL", "info")

# ---------- Authentication Config ----------

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))
ACCESS_TOKEN_EXPIRE_HOURS = int(getenv("ACCESS_TOKEN_EXPIRE_HOURS", 2))
VERIFY_TOKEN_EXPIRE_MINUTES = int(getenv("VERIFY_TOKEN_EXPIRE_MINUTES", 15))
PASSWORD_REST_OTP_EXPIRE_MINUTES = int(getenv("PASSWORD_REST_OTP_EXPIRE_MINUTES", 15))

if ACCESS_TOKEN_EXPIRE_HOURS not in range(0, 25):
    print(
        colored(
            "Please Change the ACCESS_TOKEN_EXPIRE_HOURS variable should be range 0 to 24.",
            "red",
        )
    )
elif ACCESS_TOKEN_EXPIRE_MINUTES not in range(0, 61):
    print(
        colored(
            "Please Change the ACCESS_TOKEN_EXPIRE_MINUTES variable should be range 0 to 60.",
            "red",
        )
    )
if ACCESS_TOKEN_EXPIRE_MINUTES == 0 and ACCESS_TOKEN_EXPIRE_HOURS == 0:
    print(
        colored(
            "Please Change the ACCESS_TOKEN_EXPIRE_MINUTES and ACCESS_TOKEN_EXPIRE_MINUTES variable, one of them should be bigger than 0.",
            "red",
        )
    )


# ---------- DataBase Config ----------

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")

# ---------- CutOut Config ----------

API_BASE_URL = getenv("API_BASE_URL")
API_KEY = getenv("API_KEY")


def get_database_url():
    """It will Generate Database URL for PostgreSQL To connect with

    Returns:
        string: Database Url to open connection with it
    """
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ---------- Domain URL ----------
Domain_BASE_URL = getenv("Domain_BASE_URL")

# ---------- Email Configuration ----------

EMAIL_SENDER_ADDRESS = getenv("EMAIL_SENDER_ADDRESS")
EMAIL_SENDER_PASSWORD = getenv("EMAIL_SENDER_PASSWORD")
EMAIL_SMTP_SERVER = getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_PORT = getenv("EMAIL_SMTP_PORT")

# ---------- Templates Paths ----------
TEMPLATES_PATH = "/home/CF-ClarityKit/ClarityKit-Backend/templates"
VERIFY_TEMPLATE = getenv("VERIFY_TEMPLATE")
PASSWORD_RESET_TEMPLATE = getenv("PASSWORD_RESET_TEMPLATE")
