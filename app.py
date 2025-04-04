from flask import Flask, render_template, redirect, url_for, request, jsonify
from utils.gcloud import (
    get_all_clubs, list_divisions, list_conferences, 
    list_seasons, list_clubs, get_club_videos, get_club_stats, get_all_clubs_optimized, get_storage_client, get_club_videos_optimized
)
import os
import datetime
from config import SECRET_KEY, DEBUG
import base64
import uuid
import json
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Add context processor to make the current year available to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')

@app.route('/clubs')
def clubs_directory():
    """Render the clubs directory page"""
    all_clubs = get_all_clubs_optimized()
    
    # Organize clubs by division and conference
    organized_clubs = {}
    for club in all_clubs:
        division = club['division']
        conference = club['conference']
        
        if division not in organized_clubs:
            organized_clubs[division] = {}
        
        if conference not in organized_clubs[division]:
            organized_clubs[division][conference] = []
        
        organized_clubs[division][conference].append(club['name'])
    
    print(f"Found {len(all_clubs)} clubs")
    print(f"Organized clubs: {organized_clubs}")
    
    return render_template('clubs_directory.html', clubs=organized_clubs)

@app.route('/clubs/<team>')
def club_page(team):
    """Render the club page for a specific team"""
    # For demonstration, find the first instance of the team
    all_clubs = get_all_clubs()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs_directory'))
    
    # Mocked data for team roster and formation
    roster = [
        {'position': 'GK', 'name': 'John', 'rating': 8.5},
        {'position': 'LB', 'name': 'Mike', 'rating': 7.8},
        {'position': 'CB', 'name': 'Steve', 'rating': 8.2},
        {'position': 'CB', 'name': 'Dave', 'rating': 7.9},
        {'position': 'RB', 'name': 'Tony', 'rating': 8.1},
        {'position': 'CDM', 'name': 'Paul', 'rating': 8.3},
        {'position': 'CM', 'name': 'Luke', 'rating': 8.0},
        {'position': 'CAM', 'name': 'Mark', 'rating': 8.7},
        {'position': 'LW', 'name': 'Carlos', 'rating': 8.4},
        {'position': 'RW', 'name': 'Eric', 'rating': 8.2},
        {'position': 'ST', 'name': 'Frank', 'rating': 8.8}
    ]
    
    # Mocked data for team style radar
    team_style = {
        'possession': 65,
        'attacking': 75,
        'defending': 68,
        'pressing': 72,
        'passing': 70
    }
    
    # Get actual videos for the team if available
    videos = get_club_videos(
        club_info['division'], 
        club_info['conference'], 
        club_info['season'], 
        club_info['name']
    )
    
    return render_template(
        'clubs.html', 
        team=club_info,
        roster=roster,
        team_style=team_style,
        videos=videos
    )

@app.route('/clubs/<team>/videolibrary')
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
        return redirect(url_for('clubs_directory'))
    
    # Get videos organized by season
    videos_by_season = {}
    
    for season in list_seasons(club_info['division'], club_info['conference']):
        season_videos = get_club_videos(
            club_info['division'], 
            club_info['conference'], 
            season, 
            club_info['name']
        )
        if season_videos:
            videos_by_season[season] = season_videos
    
    return render_template(
        'video_library.html',
        team=club_info,
        videos_by_season=videos_by_season
    )

@app.route('/clubs/<team>/annotateimg')
def annotate_img(team):
    """Render the annotation tool for a frame from a video"""
    video_id = request.args.get('video_id', '')
    timestamp = request.args.get('timestamp', '0')
    frame = request.args.get('frame', '')
    
    # Get club info 
    all_clubs = get_all_clubs_optimized()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs_directory'))
    
    return render_template('annotate.html', team=club_info, video_id=video_id, timestamp=timestamp, frame=frame)

@app.route('/conferences')
def conferences():
    """Render the conferences page"""
    # Get all divisions
    divisions = list_divisions()
    
    # Get conferences for each division
    division_conferences = {}
    for division in divisions:
        conferences = list_conferences(division)
        if conferences:
            division_conferences[division] = conferences
    
    return render_template('conferences.html', division_conferences=division_conferences)

@app.route('/conferences/<division>/<conference>')
def conference_page(division, conference):
    """Render the page for a specific conference"""
    # Get all clubs in this conference
    all_clubs = get_all_clubs_optimized()
    conference_clubs = []
    
    for club in all_clubs:
        if club['division'] == division and club['conference'] == conference:
            conference_clubs.append(club['name'])
    
    return render_template('conference.html', 
                          division=division, 
                          conference=conference,
                          clubs=conference_clubs)

@app.route('/api/divisions')
def api_divisions():
    """API endpoint to get all divisions, conferences, and clubs"""
    try:
        # Debug: List all divisions
        divisions = list_divisions()
        print(f"Found divisions: {divisions}")
        
        all_clubs = get_all_clubs()
        print(f"Found {len(all_clubs)} clubs")
        
        # Organize clubs by division and conference
        organized_clubs = {}
        for club in all_clubs:
            division = club['division']
            conference = club['conference']
            
            if division not in organized_clubs:
                organized_clubs[division] = {}
            
            if conference not in organized_clubs[division]:
                organized_clubs[division][conference] = []
            
            if club['name'] not in organized_clubs[division][conference]:
                organized_clubs[division][conference].append(club['name'])
        
        print(f"Organized clubs: {organized_clubs}")
        return jsonify(organized_clubs)
    except Exception as e:
        print(f"Error in api_divisions: {str(e)}")
        # Return empty data with a 500 status code
        return jsonify({}), 500

@app.route('/api/competitions')
def api_competitions():
    """API endpoint to get all competitions by division"""
    try:
        divisions = list_divisions()
        print(f"Found divisions for competitions: {divisions}")
        
        # Organize competitions by division
        competitions = {}
        for division in divisions:
            if division not in competitions:
                competitions[division] = []
                
            # Add national championship for each division
            competitions[division].append(f"{division} National Championship")
            
            # Add conferences as competitions
            conferences = list_conferences(division)
            print(f"Found conferences for {division}: {conferences}")
            for conference in conferences:
                competitions[division].append(f"{conference} Conference")
        
        print(f"Organized competitions: {competitions}")
        return jsonify(competitions)
    except Exception as e:
        print(f"Error in api_competitions: {str(e)}")
        # Return empty data with a 500 status code
        return jsonify({}), 500

@app.route('/api/save_annotation', methods=['POST'])
def save_annotation():
    """API endpoint to save an annotation"""
    try:
        # Get data from request
        image_data = request.form.get('image')
        video_id = request.form.get('video_id')
        timestamp = request.form.get('timestamp')
        objects = request.form.get('objects')
        
        # Create directory for annotations if it doesn't exist
        annotations_dir = os.path.join('static', 'annotations')
        if not os.path.exists(annotations_dir):
            os.makedirs(annotations_dir)
        
        # Generate a unique filename
        filename = f"{video_id.replace('/', '_')}_{timestamp.replace(':', '-')}_{uuid.uuid4().hex[:8]}.png"
        file_path = os.path.join(annotations_dir, filename)
        
        # Save the image
        # Remove the data:image/png;base64, prefix
        image_data = image_data.split(',')[1]
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        # Save metadata
        metadata_path = os.path.join(annotations_dir, filename.replace('.png', '.json'))
        with open(metadata_path, 'w') as f:
            json.dump({
                'video_id': video_id,
                'timestamp': timestamp,
                'objects': json.loads(objects),
                'date_created': datetime.datetime.now().isoformat()
            }, f)
        
        return jsonify({
            'success': True,
            'filename': filename
        })
    except Exception as e:
        app.logger.error(f"Error saving annotation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export_clip', methods=['POST'])
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
        clips_dir = os.path.join('static', 'clips')
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
        app.logger.error(f"Error exporting clip: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clubs/<team>/videos')
def club_videos(team):
    """Render the club videos page for a specific team"""
    all_clubs = get_all_clubs()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs_directory'))
    
    # Get videos for this club using the optimized function
    videos = get_club_videos_optimized(
        club_info['division'], 
        club_info['conference'],
        club_info['season'], 
        club_info['name']
    )
    
    return render_template('club_videos.html', team=club_info, videos=videos)

@app.route('/create_placeholder_field')
def create_placeholder_field():
    """Create a placeholder soccer field image if it doesn't exist"""
    # Create directory if it doesn't exist
    images_dir = os.path.join('static', 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    field_path = os.path.join(images_dir, 'soccer_field.jpg')
    
    # Only create if it doesn't exist
    if not os.path.exists(field_path):
        # Create a simple soccer field
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 60)
        
        # Field background
        field = Rectangle((0, 0), 100, 60, fc='#3a7e3a', ec='white', lw=2)
        ax.add_patch(field)
        
        # Center line
        ax.plot([50, 50], [0, 60], 'white', lw=2)
        
        # Center circle
        center_circle = Ellipse((50, 30), 20, 20, fc='none', ec='white', lw=2)
        ax.add_patch(center_circle)
        
        # Penalty areas
        left_penalty = Rectangle((0, 15), 16, 30, fc='none', ec='white', lw=2)
        right_penalty = Rectangle((84, 15), 16, 30, fc='none', ec='white', lw=2)
        ax.add_patch(left_penalty)
        ax.add_patch(right_penalty)
        
        # Goal areas
        left_goal = Rectangle((0, 22), 5, 16, fc='none', ec='white', lw=2)
        right_goal = Rectangle((95, 22), 5, 16, fc='none', ec='white', lw=2)
        ax.add_patch(left_goal)
        ax.add_patch(right_goal)
        
        # Remove axes
        ax.axis('off')
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(field_path, dpi=100)
        plt.close()
        
        return "Placeholder field created"
    else:
        return "Placeholder field already exists"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 