#  IaC - Serverless - CloudFormation 
This repository contains Serverless/CloudFormation code (IaC) to accomplish various tasks.

## Features

- Different mini projects in serverless to create AWS resources

### cwlogs_to_sns
- Lambda function that is used to get triggered CloudWatch Logs event(s) and publish them in an SNS Topic

### sls_lambda_delete_old_snapshots
- Lambda function that deletes EC2 Snapshots older than 90 days from today. It also has cron job that runs daily at 11PM
- Lambda function that deletes EC2 Snapshots older than 730 days (2 Years) from today. It also has cron job that runs at 11:30 pm every 1st day of the month
- Lambda function that tags (“Status”: “Save”) the snapshots whose creation date is the 90th day before today. It also has cron job that runs at 10:00 pm every Monday 
