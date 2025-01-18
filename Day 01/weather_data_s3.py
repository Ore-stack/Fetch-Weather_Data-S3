import os
import requests
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Function to retrieve secrets from AWS Secrets Manager
def get_secret(secret_name, region_name="us-west-2"):
    # Create a Secrets Manager client
    client = boto3.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise Exception(f"Error retrieving secret: {e}")

    # Parse the secret
    secret = json.loads(get_secret_value_response["SecretString"])
    return secret

def get_api_key(secret):
    api_key = secret.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API Key not found in AWS Secrets Manager.")
    return api_key

def get_aws_credentials(secret):
    aws_access_key = secret.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = secret.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found in AWS Secrets Manager.")
    return aws_access_key, aws_secret_key

def fetch_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

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

def main():
    try:
        # Retrieve secrets from AWS Secrets Manager
        secret_name = "wetaher_data"  # Replace with your secret name
        region_name = "us-east-1"  # Replace with your AWS region
        secret = get_secret(secret_name, region_name)

        # Get sensitive data from the secrets
        api_key = get_api_key(secret)
        aws_access_key, aws_secret_key = get_aws_credentials(secret)

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

