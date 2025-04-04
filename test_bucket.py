from google.cloud import storage
import os

# Set your GCP credential file path
credential_file = "upsl-video-api-c5071e2d09bf.json"
bucket_name = "upsl_match_videos"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file

def test_bucket_access():
    print(f"Testing bucket access with credentials from {credential_file}")
    
    # Create storage client
    client = storage.Client()
    
    # Check if we can list all buckets
    print("Listing all buckets:")
    buckets = list(client.list_buckets())
    print(f"Found {len(buckets)} buckets")
    for bucket in buckets:
        print(f" - {bucket.name}")
    
    # Now try to access the specific bucket
    print(f"\nAccessing bucket: {bucket_name}")
    bucket = client.bucket(bucket_name)
    
    # Try listing objects directly (without delimiter)
    print("\nListing all blobs (max 10):")
    blobs = list(bucket.list_blobs(max_results=10))
    print(f"Found {len(blobs)} blobs")
    for blob in blobs:
        print(f" - {blob.name}")
    
    # Try using delimiter
    print("\nListing with delimiter '/':")
    result = bucket.list_blobs(delimiter='/')
    prefixes = list(result.prefixes)
    print(f"Found {len(prefixes)} prefixes:")
    for prefix in prefixes:
        print(f" - {prefix}")
    
    # Check if we can explicitly list the Premier directory
    print("\nExplicitly checking Premier/ directory:")
    premier_blobs = list(bucket.list_blobs(prefix="Premier/", max_results=5))
    print(f"Found {len(premier_blobs)} blobs in Premier/")
    for blob in premier_blobs:
        print(f" - {blob.name}")

if __name__ == "__main__":
    test_bucket_access() 