from google.cloud import storage
import json
import os
from config import GCP_BUCKET_VIDEOS, GCP_BUCKET_STATS
import logging
from app.services.cache import get_from_cache, save_to_cache

# Don't set the credentials path here - it's already set in app.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_storage_client():
    """Initialize and return a Google Cloud Storage client"""
    return storage.Client()

def list_divisions():
    """List all divisions in the bucket"""
    try:
        logger.info("Getting storage client")
        client = get_storage_client()
        
        logger.info(f"Getting bucket: {GCP_BUCKET_VIDEOS}")
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # Direct approach - list all blobs and find unique "directory" names
        blobs = list(bucket.list_blobs(max_results=100))
        logger.info(f"Found {len(blobs)} blobs")
        
        # Extract division names from blob names
        divisions = set()
        for blob in blobs:
            # Look for top-level folders (paths with one segment before first slash)
            parts = blob.name.split('/')
            if len(parts) > 1 and parts[0]:  # Ensure there's a non-empty first segment
                divisions.add(parts[0])
        
        divisions_list = list(divisions)
        logger.info(f"Found divisions: {divisions_list}")
        return divisions_list
    except Exception as e:
        logger.error(f"Error in list_divisions: {str(e)}")
        # If there's an error, return an empty list
        return []

def list_conferences(division):
    """List all conferences in a division"""
    try:
        logger.info(f"Listing conferences for division: {division}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # List all blobs with the given prefix
        blobs = list(bucket.list_blobs(prefix=f"{division}/", max_results=100))
        logger.info(f"Found {len(blobs)} blobs for division: {division}")
        
        # Extract conference names from blob names
        conferences = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > 2 and parts[1]:  # Ensure we have a second path segment
                conferences.add(parts[1])
                logger.info(f"Found conference: {parts[1]}")
            
        return list(conferences)
    except Exception as e:
        logger.error(f"Error in list_conferences: {str(e)}")
        return []

def list_seasons(division, conference):
    """List all seasons for a conference"""
    try:
        logger.info(f"Listing seasons for {division}/{conference}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # List all blobs with the given prefix
        blobs = list(bucket.list_blobs(prefix=f"{division}/{conference}/", max_results=100))
        logger.info(f"Found {len(blobs)} blobs for {division}/{conference}")
        
        # Extract season names from blob names
        seasons = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > 3 and parts[2]:  # Ensure we have a third path segment
                seasons.add(parts[2])
                logger.info(f"Found season: {parts[2]}")
            
        return list(seasons)
    except Exception as e:
        logger.error(f"Error in list_seasons: {str(e)}")
        return []

def list_clubs(division, conference, season):
    """List all clubs for a season"""
    try:
        logger.info(f"Listing clubs for {division}/{conference}/{season}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # List all blobs with the given prefix
        blobs = list(bucket.list_blobs(prefix=f"{division}/{conference}/{season}/", max_results=100))
        logger.info(f"Found {len(blobs)} blobs for {division}/{conference}/{season}")
        
        # Extract club names from blob names
        clubs = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) > 4 and parts[3]:  # Ensure we have a fourth path segment
                clubs.add(parts[3])
                logger.info(f"Found club: {parts[3]}")
            
        return list(clubs)
    except Exception as e:
        logger.error(f"Error in list_clubs: {str(e)}")
        return []

def get_club_videos(division, conference, season, club):
    """Get all videos for a club"""
    try:
        logger.info(f"Getting videos for {division}/{conference}/{season}/{club}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # List all blobs with the given prefix
        prefix = f"{division}/{conference}/{season}/{club}/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        logger.info(f"Found {len(blobs)} blobs for {club}")
        
        # Extract video details
        videos = []
        for blob in blobs:
            if blob.name.endswith('.mp4'):
                video_name = blob.name.split('/')[-1]
                videos.append({
                    'name': video_name,
                    'url': f"https://storage.googleapis.com/{GCP_BUCKET_VIDEOS}/{blob.name}",
                    'size': blob.size,
                    'updated': blob.updated
                })
                logger.info(f"Added video: {video_name}")
        
        return videos
    except Exception as e:
        logger.error(f"Error in get_club_videos: {str(e)}")
        return []

def get_club_videos_optimized(division, conference, season, club):
    """Get videos for a club with optimized approach and error handling"""
    # Try to get from cache first
    cache_key = f"videos_{division}_{conference}_{season}_{club}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        logger.info(f"Using cached video data for {club}")
        return cached_data
    
    try:
        logger.info(f"Getting videos for {division}/{conference}/{season}/{club}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # List all blobs with the given prefix
        prefix = f"{division}/{conference}/{season}/{club}/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        logger.info(f"Found {len(blobs)} blobs for {club}")
        
        # Extract video details
        videos = []
        for blob in blobs:
            # Skip directories and non-video files
            if blob.name.endswith('/') or not blob.name.lower().endswith(('.mp4', '.webm', '.mov')):
                continue
            
            # Extract filename without path
            filename = blob.name.split('/')[-1]
            
            # Extract date from filename (assuming format: "Team1 vs Team2_YYYY-MM-DD.mp4")
            date_match = filename.split('_')[-1].split('.')[0] if '_' in filename else None
            
            # Generate public URL
            url = blob.public_url
            
            videos.append({
                'id': blob.name,
                'name': filename,
                'date': date_match,
                'url': url,
                'tags': []  # Placeholder for video tags
            })
        
        # Cache the results
        save_to_cache(cache_key, videos)
        return videos
    except Exception as e:
        logger.error(f"Error in get_club_videos: {str(e)}")
        return []

def get_club_stats(division, conference, season, club):
    """Get all stats for a club"""
    try:
        logger.info(f"Getting stats for {division}/{conference}/{season}/{club}")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_STATS)
        
        # List all blobs with the given prefix
        prefix = f"{division}/{conference}/{season}/{club}/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        logger.info(f"Found {len(blobs)} stat blobs for {club}")
        
        # Extract stats details
        stats = []
        for blob in blobs:
            if blob.name.endswith('.json'):
                # Download the JSON content
                json_content = blob.download_as_text()
                stats_data = json.loads(json_content)
                
                # Add the filename for reference
                stats_data['filename'] = blob.name.split('/')[-1]
                stats.append(stats_data)
                logger.info(f"Added stats from: {stats_data['filename']}")
        
        return stats
    except Exception as e:
        logger.error(f"Error in get_club_stats: {str(e)}")
        return []

def get_all_clubs():
    """Get all clubs across all divisions, conferences, and seasons"""
    # Try to get from cache first
    cache_key = "all_clubs"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        logger.info("Using cached club data")
        return cached_data
    
    try:
        logger.info(f"Getting all clubs")
        all_clubs = []
        
        # Get all divisions
        divisions = list_divisions()
        logger.info(f"Found divisions: {divisions}")
        
        # For each division, get all conferences
        for division in divisions:
            conferences = list_conferences(division)
            logger.info(f"Found conferences for {division}: {conferences}")
            
            # For each conference, get all seasons
            for conference in conferences:
                seasons = list_seasons(division, conference)
                logger.info(f"Found seasons for {division}/{conference}: {seasons}")
                
                # For each season, get all clubs
                for season in seasons:
                    clubs = list_clubs(division, conference, season)
                    logger.info(f"Found clubs for {division}/{conference}/{season}: {clubs}")
                    
                    for club in clubs:
                        all_clubs.append({
                            'name': club,
                            'division': division,
                            'conference': conference,
                            'season': season
                        })
                        logger.info(f"Added club: {club} ({division}/{conference}/{season})")
        
        # Save to cache before returning
        save_to_cache(cache_key, all_clubs)
        return all_clubs
    except Exception as e:
        logger.error(f"Error in get_all_clubs: {str(e)}")
        return []

def get_all_clubs_optimized():
    """Get all clubs with a single pass through all blobs"""
    # Try to get from cache first
    cache_key = "all_clubs_optimized"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        logger.info("Using cached club data (optimized)")
        return cached_data
    
    try:
        logger.info("Getting all clubs with optimized approach")
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        
        # Get all blobs up to a reasonable limit (increase if needed)
        all_blobs = list(bucket.list_blobs(max_results=1000))
        logger.info(f"Found {len(all_blobs)} blobs total")
        
        # Process all paths to extract clubs
        all_clubs = []
        unique_paths = set()
        
        for blob in all_blobs:
            parts = blob.name.split('/')
            if len(parts) >= 5:  # We need at least division/conference/season/club
                path_key = f"{parts[0]}/{parts[1]}/{parts[2]}/{parts[3]}"
                
                if path_key not in unique_paths:
                    unique_paths.add(path_key)
                    all_clubs.append({
                        'name': parts[3],
                        'division': parts[0],
                        'conference': parts[1],
                        'season': parts[2]
                    })
        
        logger.info(f"Extracted {len(all_clubs)} unique clubs")
        
        # Save to cache before returning
        save_to_cache(cache_key, all_clubs)
        return all_clubs
    except Exception as e:
        logger.error(f"Error in get_all_clubs_optimized: {str(e)}")
        return [] 
