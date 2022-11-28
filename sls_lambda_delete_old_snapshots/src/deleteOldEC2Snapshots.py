import boto3
import datetime
from botocore.exceptions import ClientError
import os

# Reading environment variables
region = os.environ['region']
account = os.environ['account']
limit = int(os.environ['limit'])

# AWS Settings
client = boto3.client('ec2',region_name=region)
snapshots = client.describe_snapshots(OwnerIds=[account])
taggedSnapshots = client.describe_snapshots(OwnerIds=[account], Filters=[{'Name': 'tag:Status', 'Values': ['Saved']}])

def lambda_handler(event, context):
    count=0
    snapshotsToBeDeleted=[]
    taggedSnapshotIDs=[]
    
    for taggedSnapshot in taggedSnapshots['Snapshots']:
        taggedSnapshotIDs.append(taggedSnapshot['SnapshotId'])
    
    for snapshot in snapshots['Snapshots']:
        temp=snapshot['StartTime']
        snapshotStartTime=temp.date()
        dateToday=datetime.date.today()
        #dateToday=datetime.datetime.strptime('20201201', '%Y%m%d').date()
        dateDiff=dateToday-snapshotStartTime
        try:
            if dateDiff.days>limit and snapshot['SnapshotId'] not in taggedSnapshotIDs:
                id = snapshot['SnapshotId']
                started = snapshot['StartTime']

                # Add this condition if you want to keep a snapshot
                if id == "snap-0ehwehiqweyiwey":
                    print("Skipping sample project last snapshot")
                else:
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