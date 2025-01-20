## NBA Data Lake for Sports Analytics

## Overview
This project builds a robust data lake for NBA sports analytics using AWS services:
- **Amazon S3**: For scalable storage of raw, transformed, and analytics-ready data.
- **AWS Glue**: For data cataloging and ETL (Extract, Transform, Load) operations.
- **Amazon Athena**: For running SQL queries directly on the data stored in S3.

## Project Workflow

1. **Set Up S3 Bucket**: Create an Amazon S3 bucket to store NBA datasets.
2. **Data Ingestion**: Fetch NBA data from the SportsData.io API and upload it to S3.
3. **Glue Database and Tables**:
    - Create a Glue database to organize metadata.
    - Define Glue tables for raw and transformed data.
4. **Data Transformation**: Use AWS Glue jobs to clean and prepare data for analysis.
5. **Query with Athena**: Configure Athena to query the processed data.

---

## Prerequisites

Before running the project, ensure the following:

1. **AWS Account**: Access to AWS services.
2. **Python Environment**: Python 3.x installed with the following libraries:
    - `boto3`
    - `requests`
3. **API Access**: Obtain an API key from [SportsData.io](https://sportsdata.io/).
4. **IAM Role**: Set up an IAM role with the following permissions:
    - Amazon S3: Full access to the S3 bucket.
    - AWS Glue: Permissions to create databases, tables, and run jobs.
    - Amazon Athena: Permissions to query data.

---

## Installation

1. **Clone the Repository**:
    ```bash
    git clone [<repository-url>](https://github.com/Ore-stack/30-days-DevOps-Challenge)
    cd Day 03
    ```

2. **Install Dependencies**:
    ```bash
    pip install boto3 requests
    ```

3. **Set Up Environment Variables**:
    Create a `.env` file and add:
    ```env
    AWS_ACCESS_KEY_ID=<your-access-key>
    AWS_SECRET_ACCESS_KEY=<your-secret-key>
    SPORTS_DATA_API_KEY=<your-api-key>
    ```

---

## Running the Project

### **Step 1: Create the Data Lake**
Run the Python script to set up the data lake:
```bash
python nba_data_lake.py
```
This script will:
- Create an S3 bucket.
- Set up a Glue database and tables.
- Configure Athena output location.

### **Step 2: Fetch NBA Data**
The script will fetch player and game data from SportsData.io and store it in the S3 bucket.

### **Step 3: Query Data with Athena**
Log in to the AWS Management Console and use Athena to run SQL queries on the processed data.

---

## Example Query
Here is an example of a SQL query to analyze player performance:
```sql
SELECT player_name, team, points, assists, rebounds
FROM processed_nba_data
WHERE game_date = '2023-01-15';
```

---

## Project Structure

```plaintext
.
├── nba_data_lake.py          # Main script for setting up the data lake
├── policies.json             # Policy
├── .env                      # Environment variables (not included in repo)
├── README.md                 # Project documentation
└── data/                     # Local data directory (if needed)
```
---

## Contributions
Contributions are welcome! Please create an issue or pull request for improvements.

---
