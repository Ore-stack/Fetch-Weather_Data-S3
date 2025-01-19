import json
import boto3
import urllib.request
import os

# Initialize the SNS client
sns_client = boto3.client('sns')

def fetch_scores():
    api_key = os.getenv('API_KEY')
    api_endpoint = os.getenv('API_ENDPOINT')
    
    headers = {
        'X-Auth-Token': api_key
    }
    req = urllib.request.Request(api_endpoint, headers=headers)
    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            raise Exception(f"Failed to fetch data: {response.status} - {response.reason}")
        data = response.read()
        return json.loads(data)

def generate_message(matches):
    message = "Today's English Premier League Scores:\n"
    for match in matches['matches']:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        score = match['score']
        message += f"{home_team} vs {away_team} - {score['fullTime']['homeTeam']}:{score['fullTime']['awayTeam']}\n"
    return message

def send_notification(message):
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Premier League Game Day Scores'
    )

def lambda_handler(event, context):
    try:
        matches = fetch_scores()
        message = generate_message(matches)
        send_notification(message)
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }
