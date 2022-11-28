# Serverless - Lambda publishes logs to SNS when CloudWatch encounters error

```
Lambda used to get triggered CloudWatch Logs event(s) and publish them in an SNS Topic.
```

### Commands
1. You will need to set "AWS_PROFILE" environment variable and configure AWS Credentials. These credentials are used for AWS services e.g fetch parameters to genereate .env file etc.


2.  Create the Stack
Modify the custom parameters in the serverless.yml file

```
cd lambda/
serverless deploy
```

#### Delete the Stack
```
serverless remove
```