"""Track 5a example: boto3, AWS from Python (READ-ONLY).

Run:    python3 learning-path/advanced/examples/t5_boto3.py [--region us-east-1]
Needs:  pip install boto3     and AWS credentials configured the standard way:
          - `aws configure` (writes ~/.aws/credentials), or
          - environment variables AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY, or
          - an SSO profile / instance role.
NEVER type keys into this file. boto3 finds credentials by itself.
No account yet? Run t5_boto3_mock.py instead: it uses a fake AWS.

This script only READS (list/describe). It creates, changes and deletes nothing.
"""

import argparse

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


# BLOCK 1: who am I? (always the first call to make)
def whoami(session):
    """Return the account id and identity ARN the credentials belong to."""
    sts = session.client("sts")
    ident = sts.get_caller_identity()
    return {"account": ident["Account"], "arn": ident["Arn"]}


# BLOCK 2: list S3 buckets
def list_buckets(session):
    s3 = session.client("s3")
    return [b["Name"] for b in s3.list_buckets()["Buckets"]]


# BLOCK 3: list objects in a bucket with a PAGINATOR (APIs return limited pages)
def list_objects(session, bucket, prefix="", limit=20):
    s3 = session.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    found = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):          # "Contents" is absent when empty
            found.append((obj["Key"], obj["Size"]))
            if len(found) >= limit:
                return found
    return found


# BLOCK 4: list EC2 instances with a server-side filter
def list_instances(session, state=None):
    ec2 = session.client("ec2")
    kwargs = {}
    if state:
        kwargs["Filters"] = [{"Name": "instance-state-name", "Values": [state]}]
    result = []
    for page in ec2.get_paginator("describe_instances").paginate(**kwargs):
        for reservation in page["Reservations"]:       # instances are nested in reservations
            for inst in reservation["Instances"]:
                tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}   # list -> dict
                result.append({
                    "id": inst["InstanceId"],
                    "type": inst["InstanceType"],
                    "state": inst["State"]["Name"],
                    "name": tags.get("Name", "(no name)"),
                })
    return result


# BLOCK 5: pure logic on the data (Day 20 layering: easy to test)
def summarise_by_state(instances):
    counts = {}
    for i in instances:
        counts[i["state"]] = counts.get(i["state"], 0) + 1
    return counts


# BLOCK 6: the program: ties it together and handles failure (Day 16)
def main():
    parser = argparse.ArgumentParser(description="Read-only AWS overview")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--profile", help="named profile from ~/.aws/config")
    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    try:
        print("Identity :", whoami(session))
        buckets = list_buckets(session)
        print(f"Buckets  : {len(buckets)}", buckets[:5])
        instances = list_instances(session)
        print("Instances:", summarise_by_state(instances))
        for i in instances[:5]:
            print("  ", i)
    except NoCredentialsError:
        print("No AWS credentials found. Run `aws configure` or set the AWS_* variables.")
    except ClientError as e:
        code = e.response["Error"]["Code"]            # e.g. AccessDenied, ExpiredToken
        print(f"AWS rejected the request: {code}: {e.response['Error']['Message']}")
    except BotoCoreError as e:
        print("Connection/config problem:", e)


if __name__ == "__main__":
    main()
