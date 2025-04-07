import os

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-local-development')

# Environment settings
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Google Cloud Storage
GCP_BUCKET_VIDEOS = os.environ.get('GCP_BUCKET_VIDEOS', 'upsl_match_videos')
GCP_BUCKET_STATS = os.environ.get('GCP_BUCKET_STATS', 'upsl_match_stats')

# Supabase (Future implementation)
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')