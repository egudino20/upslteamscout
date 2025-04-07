from flask import Blueprint, render_template
from app.services.storage import list_divisions, list_conferences, get_all_clubs_optimized

conferences_bp = Blueprint('conferences', __name__, url_prefix='/conferences')

@conferences_bp.route('/')
def conferences_list():
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

@conferences_bp.route('/<division>/<conference>')
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
