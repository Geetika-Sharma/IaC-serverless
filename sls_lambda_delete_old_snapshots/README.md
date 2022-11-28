# Serverless Lambda project to delete old EC2 Snapshots
This project uses serverless to create the following resources:

- Lambda Function
- IAM role for Lambda function

## deleteSnapshotFunction - Lambda Function
This Lambda function deletes EC2 Snapshots older than 90 days from today. It also has cron job that runs daily at 11PM.

## deleteTwoYearsOldEC2Snapshots.py - Lambda Function
This Lambda function deletes EC2 Snapshots older than 730 days (2 Years) from today. It also has cron job that runs at 11:30 pm every 1st day of the month

## tagSnapshotFunction - Lambda Function
This Lambda function tags (“Status”: “Save”) the snapshots whose creation date is the 90th day before today. It also has cron job that runs at 10:00 pm every Monday 

### Prerequisites 
- Serverless installed on the system
- Update serverless.yml with the required values

#### Updating serverless.yml
Update the values of the environment variables according to their description below:

```
- region: <str> The region from which EC2 Snapshots are to be deleted
- limit: <int> Snapshots older than this limit to be deleted. 
                e.g. if value is 90 then snapshots older than 90 days will be deleted 
- saving: <int> Snapshots created at this limit to be tagged
                e.g. if value is 90 then snapshots created on 90th day from today will be tagged 
```

### Commands
1. You will need to set "AWS_PROFILE" environment variable and configure AWS Credentials to create ~/.aws/credentials file. These credentials are used for AWS services e.g fetch parameters to genereate .env file etc.

2. Create the CloudFormation stack which in turn will create the Lambda Function and IAM Role.
```
serverless deploy
```

To remove the resources
```
serverless remove
```