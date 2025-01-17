import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API Key not found.")
    return api_key

def get_aws_credentials():
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found.")
    return aws_access_key, aws_secret_key
