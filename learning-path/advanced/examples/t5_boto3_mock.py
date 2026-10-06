"""Track 5b example: practise boto3 with a FAKE AWS (no account needed).

Run:    python3 learning-path/advanced/examples/t5_boto3_mock.py
Needs:  pip install boto3 "moto[s3,ec2,sts]"

moto intercepts boto3 calls and answers from a pretend AWS held in memory.
Nothing leaves your computer. The functions tested here are the SAME ones
that t5_boto3.py uses against real AWS.
"""

import os

# BLOCK 1: fake credentials, set BEFORE importing boto3.
# They are dummies so no code in this process can ever authenticate to real AWS.
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ.pop("AWS_PROFILE", None)

import boto3
from moto import mock_aws

import t5_boto3 as aws          # the real-AWS functions, reused unchanged


def build_fake_world(session):
    """Create a few fake resources to read back."""
    s3 = session.client("s3")
    s3.create_bucket(Bucket="demo-logs")
    s3.create_bucket(Bucket="demo-backups")
    for n in range(25):
        s3.put_object(Bucket="demo-logs", Key=f"2026/01/app-{n:02d}.log", Body=b"x" * (n + 1))

    ec2 = session.client("ec2")
    image_id = ec2.describe_images()["Images"][0]["ImageId"]       # moto ships sample AMIs
    for name in ("web01", "web02", "db01"):
        ec2.run_instances(
            ImageId=image_id, MinCount=1, MaxCount=1, InstanceType="t3.micro",
            TagSpecifications=[{"ResourceType": "instance",
                                "Tags": [{"Key": "Name", "Value": name}]}],
        )
    # stop one instance so there are two states to summarise
    db = [i for i in aws.list_instances(session) if i["name"] == "db01"][0]
    ec2.stop_instances(InstanceIds=[db["id"]])


# BLOCK 2: everything inside mock_aws() talks to the pretend AWS
with mock_aws():
    session = boto3.Session(region_name="us-east-1")
    build_fake_world(session)

    print("Identity       :", aws.whoami(session))
    print("Buckets        :", aws.list_buckets(session))

    # BLOCK 3: the paginator at work: 25 objects, but we ask for 10
    objs = aws.list_objects(session, "demo-logs", prefix="2026/01/", limit=10)
    print(f"First {len(objs)} objects:", objs[:3], "...")
    print("All objects    :", len(aws.list_objects(session, "demo-logs", limit=1000)))

    # BLOCK 4: filters and tags
    instances = aws.list_instances(session)
    print("Instances      :", [(i["name"], i["state"]) for i in instances])
    print("Only running   :", [i["name"] for i in aws.list_instances(session, state="running")])
    print("By state       :", aws.summarise_by_state(instances))

    # BLOCK 5: error handling: what a permission/nonexistent-resource error looks like
    from botocore.exceptions import ClientError
    try:
        session.client("s3").list_objects_v2(Bucket="no-such-bucket")
    except ClientError as e:
        print("Error code     :", e.response["Error"]["Code"])       # NoSuchBucket

print("Done. Everything above happened in memory only.")
