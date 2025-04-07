from flask import Blueprint, render_template, redirect, url_for, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')

@main_bp.route('/create_placeholder_field')
def create_placeholder_field():
    """Create a placeholder soccer field image if it doesn't exist"""
    import os
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Ellipse
    
    # Create directory if it doesn't exist
    images_dir = os.path.join('app', 'static', 'images')
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
