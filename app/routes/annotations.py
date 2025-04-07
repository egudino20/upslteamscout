from flask import Blueprint, render_template, redirect, url_for, request, jsonify
import os
import uuid
import json
import base64
import datetime
from app.services.storage import get_all_clubs_optimized

annotations_bp = Blueprint('annotations', __name__)

@annotations_bp.route('/clubs/<team>/annotateimg')
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
        return redirect(url_for('clubs.clubs_directory'))
    
    return render_template('annotate.html', team=club_info, video_id=video_id, timestamp=timestamp, frame=frame)

@annotations_bp.route('/api/save_annotation', methods=['POST'])
def save_annotation():
    """API endpoint to save an annotation"""
    try:
        # Get data from request
        image_data = request.form.get('image')
        video_id = request.form.get('video_id')
        timestamp = request.form.get('timestamp')
        objects = request.form.get('objects')
        
        # Create directory for annotations if it doesn't exist
        annotations_dir = os.path.join('app', 'static', 'annotations')
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 
