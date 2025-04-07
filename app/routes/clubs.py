from flask import Blueprint, render_template, redirect, url_for, request
from app.services.storage import get_all_clubs, get_all_clubs_optimized, get_club_videos

clubs_bp = Blueprint('clubs', __name__, url_prefix='/clubs')

@clubs_bp.route('/')
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
    
    return render_template('clubs_directory.html', clubs=organized_clubs)

@clubs_bp.route('/<team>')
def club_page(team):
    """Render the club page for a specific team"""
    # Find the team info
    all_clubs = get_all_clubs()
    club_info = None
    
    for club in all_clubs:
        if club['name'].lower() == team.lower():
            club_info = club
            break
    
    if club_info is None:
        return redirect(url_for('clubs.clubs_directory'))
    
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
