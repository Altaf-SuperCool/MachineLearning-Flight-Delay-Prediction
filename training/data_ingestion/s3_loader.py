import boto3

def download_from_s3(bucket, key, local_path):
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, local_path)
    print(f"Downloaded from s3://{bucket}/{key}  {local_path}")
