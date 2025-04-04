import os

# Google Cloud configuration
# Remove the hardcoded path since we handle credentials in app.py
# GCP_CREDENTIAL_FILE = "upsl-video-api-c5071e2d09bf.json"
GCP_BUCKET_VIDEOS = "upsl_match_videos"
GCP_BUCKET_STATS = "upsl_match_stats"

# Flask configuration
SECRET_KEY = os.urandom(24)
DEBUG = True 