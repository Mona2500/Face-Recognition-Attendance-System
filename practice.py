import sys

from google.oauth2 import service_account
from google.cloud import storage

google_credentials = service_account.Credentials.from_service_account_file("E:\\D drive\\Downloads\\facerecognitionattendanc-711f1-05ad1073e20a.json")

def create_bucket(bucket_name):

    storage_client = storage.Client(credentials= google_credentials)

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")


if __name__ == "__main__":
    create_bucket(bucket_name="asy_automation_reports")