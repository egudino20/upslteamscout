from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import datetime
import uuid
import time
import os
from app.services.storage import (
    get_all_clubs, get_club_videos, list_seasons, get_storage_client,
    get_all_clubs_optimized, get_club_videos_optimized
)
from config import GCP_BUCKET_VIDEOS

videos_bp = Blueprint('videos', __name__)

@videos_bp.route('/clubs/<team>/videolibrary')
def video_library(team):
    """Render the video library page for a specific team"""
    # Similar to club_page, find the team info
    all_clubs = get_all_clubs()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs.clubs_directory'))
    
    # Get videos organized by conference and season
    videos_by_conference = {}
    
    # Current conference
    current_conference = club_info['conference']
    current_division = club_info['division']
    
    # List of conferences to check for this team
    conferences_to_check = [current_conference]
    
    # If the current conference is "Midwest Central North", also check "Midwest Central"
    if current_conference == "Midwest_Central_North":
        conferences_to_check.append("Midwest_Central")
    # If the current conference is "Midwest Central", also check both North and South variants
    elif current_conference == "Midwest_Central":
        conferences_to_check.append("Midwest_Central_North")
        conferences_to_check.append("Midwest_Central_South")
    # If the current conference is "Midwest Central South", also check "Midwest Central"
    elif current_conference == "Midwest_Central_South":
        conferences_to_check.append("Midwest_Central")
    
    # For each conference, get all seasons and videos
    for conference in conferences_to_check:
        videos_by_season = {}
        
        for season in list_seasons(club_info['division'], conference):
            season_videos = get_club_videos(
                club_info['division'], 
                conference,
                season, 
                club_info['name']
            )
            if season_videos:
                videos_by_season[season] = season_videos
        
        if videos_by_season:
            # Format conference name for display (replace underscores with spaces)
            display_conference = conference.replace('_', ' ')
            videos_by_conference[display_conference] = videos_by_season
    
    return render_template(
        'video_library.html',
        team=club_info,
        videos_by_conference=videos_by_conference
    )

@videos_bp.route('/clubs/<team>/videos')
def club_videos(team):
    """Render the club videos page for a specific team"""
    all_clubs = get_all_clubs()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs.clubs_directory'))
    
    # Get videos for this club using the optimized function
    videos = get_club_videos_optimized(
        club_info['division'], 
        club_info['conference'],
        club_info['season'], 
        club_info['name']
    )
    
    return render_template('club_videos.html', team=club_info, videos=videos)

@videos_bp.route('/api/export_clip', methods=['POST'])
def export_clip():
    """API endpoint to export a video clip"""
    try:
        # Get data from request
        video_id = request.form.get('video_id')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        clip_name = request.form.get('clip_name')
        
        # Get video URL from Google Cloud
        division, conference, season, club = video_id.split('/')[:4]
        video_filename = video_id.split('/')[-1]
        
        # Create directory for clips if it doesn't exist
        clips_dir = os.path.join('app', 'static', 'clips')
        if not os.path.exists(clips_dir):
            os.makedirs(clips_dir)
        
        # Generate a unique filename
        filename = f"{clip_name or video_filename.split('.')[0]}_{uuid.uuid4().hex[:8]}.mp4"
        file_path = os.path.join(clips_dir, filename)
        
        # Get the video URL
        client = get_storage_client()
        bucket = client.bucket(GCP_BUCKET_VIDEOS)
        blob = bucket.blob(video_id)
        
        # Generate signed URL for video
        video_url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=30),
            method="GET"
        )
        
        # In a real implementation, you would use a video processing library
        # like FFmpeg to extract the clip. For now, we'll simulate this with a delay
        time.sleep(2)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Clip exported successfully',
            'download_url': f'/static/clips/{filename}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
