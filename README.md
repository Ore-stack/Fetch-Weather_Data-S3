![Real-Time Weather Data Collection - Day 1 AllStarsDevOps Challenge](Open_Weather_S3/architecture.webp)


# Fetch Weather Data and Store in S3 with Automation

This guide provides instructions on how to fetch weather data using the OpenWeatherMap API, store the data in an Amazon S3 bucket, and automate the process using a cron job.

---

## Prerequisites

1. **API Key**: Obtain an API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys).
2. **AWS Account**: Ensure you have an AWS account and necessary permissions to create and manage S3 buckets.
3. **Python Environment**: Install Python (version 3.6 or later).
4. **Required Python Libraries**:
   - `boto3`
   - `requests`
   - `python-dotenv` (for managing environment variables)

Install the libraries using pip:
```bash
pip install boto3 requests python-dotenv
```

---

## Step 1: Set Up Environment Variables

Create a `.env` file in your project directory to securely store sensitive information:

```env
# .env
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=your_aws_region
S3_BUCKET_NAME=your_s3_bucket_name
CITY=city_name
```

Replace the placeholders with your actual API key, AWS credentials, region, S3 bucket name, and city.

---

## Step 2: Write the Python Script

Create a Python script (e.g., `fetch_weather.py`) with the following content:

```python
import os
import requests
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
CITY = os.getenv("CITY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# AWS S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)

def fetch_weather_data():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def upload_to_s3(data):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"weather_data_{timestamp}.json"
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=file_name,
        Body=data,
        ContentType='application/json'
    )
    print(f"Uploaded {file_name} to S3 bucket {S3_BUCKET}")

def main():
    weather_data = fetch_weather_data()
    upload_to_s3(str(weather_data))

if __name__ == "__main__":
    main()
```

---

## Step 3: Test the Script

Run the script to ensure it works correctly:
```bash
python weather_data_s3.py
```
Check the specified S3 bucket for the uploaded weather data file.

---

## Step 4: Automate with Cron Job

### Linux/MacOS:
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add the following line to schedule the script (e.g., run every hour):
   ```bash
   0 * * * * /usr/bin/python3 /path/to/weather_data_s3.py
   ```
   Replace `/path/to/weather_data_s3.py` with the full path to your script.

---

## Additional Notes
- Ensure the `.env` file is not committed to version control (add it to `.gitignore`).
- Rotate AWS keys regularly for security.
- Monitor the cron job logs to ensure smooth operation.

---

## Troubleshooting
- **Invalid API Key**: Double-check the `OPENWEATHERMAP_API_KEY` value.
- **AWS Permission Errors**: Verify that the AWS credentials have `s3:PutObject` permissions.
- **Cron Job Not Running**: Check the cron logs (`/var/log/cron` or equivalent).

---

Now your system is set up to fetch weather data, store it in S3, and automate the process efficiently!
