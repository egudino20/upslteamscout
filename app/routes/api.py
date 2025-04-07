from flask import Blueprint, jsonify
from app.services.storage import (
    list_divisions, list_conferences, get_all_clubs
)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/divisions')
def api_divisions():
    """API endpoint to get all divisions, conferences, and clubs"""
    try:
        # Debug: List all divisions
        divisions = list_divisions()
        
        all_clubs = get_all_clubs()
        
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
        
        return jsonify(organized_clubs)
    except Exception as e:
        # Return empty data with a 500 status code
        return jsonify({}), 500

@api_bp.route('/competitions')
def api_competitions():
    """API endpoint to get all competitions by division"""
    try:
        divisions = list_divisions()
        
        # Organize competitions by division
        competitions = {}
        for division in divisions:
            if division not in competitions:
                competitions[division] = []
            
            # Add conferences as competitions
            conferences = list_conferences(division)
            for conference in conferences:
                competitions[division].append(f"{conference} Conference")
        
        return jsonify(competitions)
    except Exception as e:
        # Return empty data with a 500 status code
        return jsonify({}), 500 
