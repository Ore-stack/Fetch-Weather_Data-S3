# English Premier League (EPL) Real-Time Notification System

This project demonstrates how to create a real-time notification system for English Premier League (EPL) game day scores. Using AWS Lambda, Amazon Simple Notification Service (SNS), Amazon EventBridge, and EPL APIs, this system provides fans with up-to-date match information via SMS and email notifications.

## Features
- Real-time game day score notifications.
- Multi-channel delivery through SMS and email.
- Automated scheduling using Amazon EventBridge.
- Integration with EPL APIs to fetch live game data.

## Architecture
1. **EPL API**: Fetches live game data.
2. **AWS Lambda**: Processes the data and triggers notifications.
3. **Amazon SNS**: Sends notifications via SMS and email.
4. **Amazon EventBridge**: Schedules Lambda execution for game days.

---

## Prerequisites

1. **AWS Account**: Ensure you have access to AWS services.
2. **IAM Permissions**: Set up IAM roles with permissions for Lambda, SNS, and EventBridge.
3. **API Access**: Register and obtain an API key for an EPL API provider (e.g., SportMonks).
4. **Python Environment**: Install Python 3.7+ and required dependencies.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ore-stack/30-days-DevOps-Challenge.git
cd epl-alert-system
```

### 2. Configure Environment Variables
Create a `.env` file and add the following:
```ini
EPL_API_KEY=your_api_key
AWS_REGION=your_aws_region
SNS_TOPIC_ARN=your_sns_topic_arn
```

### 3. Install Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Deploy Lambda Function
1. Zip the Lambda function:
   ```bash
   zip function.zip lambdafunction.py
   ```
2. Upload the zip to AWS Lambda:
   ```bash
   aws lambda create-function \
     --function-name EPLAlertFunction \
     --runtime python3.x \
     --role your_lambda_execution_role_arn \
     --handler lambdafunction.lambda_handler \
     --zip-file fileb://function.zip
   ```

### 5. Set Up EventBridge Rule
1. Create a rule to invoke the Lambda function during game days:
   ```bash
   aws events put-rule \
     --schedule-expression "cron(0 14 ? * SUN *)" \
     --name EPLGameDayRule
   ```
2. Add the Lambda function as the target:
   ```bash
   aws events put-targets \
     --rule EPLGameDayRule \
     --targets "Id"="1","Arn"="your_lambda_function_arn"
   ```

---

## Lambda Function Overview
The `lambdafunction.py` script:
1. Fetches live EPL game data using the EPL API.
2. Formats the data for user-friendly notifications.
3. Publishes the message to the specified Amazon SNS topic.

### Sample Code (lambdafunction.py)
```python
import os
import boto3
import requests

def lambda_handler(event, context):
    api_key = os.getenv("EPL_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")

    # Fetch EPL game data
    response = requests.get(f"https://api.sportmonks.com/v3/football/fixtures?api_key={api_key}")
    data = response.json()

    # Process and format data
    message = "Today's EPL Scores:\n"
    for match in data['data']:
        home = match['home_team']['name']
        away = match['away_team']['name']
        score = match['scores']['fulltime']
        message += f"{home} {score} {away}\n"

    # Publish to SNS
    sns_client = boto3.client('sns')
    sns_client.publish(TopicArn=sns_topic_arn, Message=message)

    return {"statusCode": 200, "body": "Notification sent!"}
```

---

## Testing
1. Test the Lambda function locally:
   ```bash
   python lambdafunction.py
   ```
2. Trigger a test event in the AWS Lambda console.

