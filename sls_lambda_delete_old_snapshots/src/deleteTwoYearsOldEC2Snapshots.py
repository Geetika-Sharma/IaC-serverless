import boto3
import datetime
import getopt
from pathlib import Path
from botocore.exceptions import ClientError
import os

# Reading environment variables
region = os.environ['region']
account = os.environ['account']
twoYearsInDays = int(os.environ['twoYearsInDays'])

# AWS Settings
client = boto3.client('ec2',region_name=region)
taggedSnapshots = client.describe_snapshots(OwnerIds=[account], Filters=[{'Name': 'tag:Status', 'Values': ['Saved']}])

def lambda_handler(event, context):
    count=0
    snapshotsToBeDeleted=[]
    
    for snapshot in taggedSnapshots['Snapshots']:
        temp=snapshot['StartTime']
        snapshotStartTime=temp.date()
        dateToday=datetime.date.today()
        dateDiff=dateToday-snapshotStartTime
        try:
            if dateDiff.days>twoYearsInDays:
                id = snapshot['SnapshotId']
                started = snapshot['StartTime']
                # Add this condition if you want to keep a snapshot
                if id == "snap-0ehwehiqweyiwey":
                    print("Skipping sample project last snapshot")
                else:
                    #Uncomment below line to delete the snapshot
                    client.delete_snapshot(SnapshotId=id)
                    count+=1
                    snapshotsToBeDeleted.append(id)
        except ClientError as e:
            if e:
                print(e)
                continue
    print(f"Total {count} snapshots deleted")
    if count > 0:
        print(f"Deleted Snapshots IDs: \n {snapshotsToBeDeleted}")