import boto3
import datetime
from botocore.exceptions import ClientError
import os

# Reading environment variables
region = os.environ['region']
account = os.environ['account']
saving = int(os.environ['saving'])

# AWS Settings
client = boto3.client('ec2',region_name=region)
snapshots = client.describe_snapshots(OwnerIds=[account])

def lambda_handler(event, context):
    count=0
    snapshotsTagged=[]

    for snapshot in snapshots['Snapshots']:
        temp=snapshot['StartTime']
        snapshotStartTime=temp.date()
        dateToday=datetime.date.today()
        dateDiff=dateToday-snapshotStartTime
        if dateDiff.days==saving:
            id = snapshot['SnapshotId']
            # tag the snapshot to keep
            client.create_tags(Resources=[snapshot['SnapshotId']], Tags=[{'Key':'Status', 'Value':'Saved'}])
            count+=1
            snapshotsTagged.append(id)

    print(f"Total {count} snapshots tagged")
    if count > 0:
        print(f"Tagged Snapshots IDs: \n {snapshotsTagged}")
    