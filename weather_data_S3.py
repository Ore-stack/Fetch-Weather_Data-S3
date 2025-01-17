import os
import requests
import boto3
import json
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

# Retrieve sensitive data from environment variables
def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API Key not found. Set the OPENWEATHER_API_KEY environment variable.")
    return api_key

def get_aws_credentials():
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
    return aws_access_key, aws_secret_key

# Fetch weather data from the OpenWeather API
def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

# Upload data to an Amazon S3 bucket
def upload_to_s3(bucket_name, file_name, data, aws_access_key, aws_secret_key):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data),
            ContentType="application/json",
        )
        print(f"File {file_name} successfully uploaded to S3 bucket {bucket_name}.")
    except Exception as e:
        raise Exception(f"Error uploading to S3: {e}")

# Main function
def main():
    try:
        # Get sensitive data from environment variables
        api_key = get_api_key()
        aws_access_key, aws_secret_key = get_aws_credentials()

        # Configuration
        city = "London"  # Replace with your desired city
        bucket_name = "tony-plank-s3"  # Replace with your S3 bucket name
        file_name = "weather_data.json"

        # Fetch weather data
        print("Fetching weather data...")
        weather_data = fetch_weather_data(api_key, city)
        print("Weather data fetched successfully.")

        # Upload weather data to S3
        print("Uploading data to S3...")
        upload_to_s3(bucket_name, file_name, weather_data, aws_access_key, aws_secret_key)
        print("Data uploaded successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

