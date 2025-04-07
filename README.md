# UPSL Team Scout

A web-based video analysis and scouting platform for UPSL (United Premier Soccer League) teams.

## Features

- Team and player analytics
- Video library with annotation capabilities
- Conference and club directories
- Detailed team statistics

## Tech Stack

- **Backend**: Python/Flask
- **Storage**: Google Cloud Storage
- **Database**: Supabase (future implementation)
- **ML/AI**: YOLOv8, ByteTrack for player tracking (future implementation)

## Project Structure

```
upslteamscout/
├── app/                           # Application package
│   ├── routes/                    # Route handlers by feature
│   ├── models/                    # Data models
│   ├── services/                  # Business logic and external services
│   │   ├── storage.py             # GCS interactions
│   │   ├── cache.py               # Caching functionality
│   │   └── ml/                    # ML-related services
│   ├── static/                    # Static assets
│   ├── templates/                 # Jinja2 templates
│   └── utils/                     # Utility functions
├── config.py                      # Configuration settings
├── run.py                         # Application entry point
├── requirements.txt               # Dependencies
└── documentation/                 # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/upslteamscout.git
   cd upslteamscout
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up Google Cloud credentials:
   - Place your service account key file in the `credentials/` directory
   - Name it `upsl-video-api-c5071e2d09bf.json`

5. Run the application:
   ```bash
   python run.py
   ```

## Development

To run the application in development mode:

```bash
set FLASK_APP=run.py
set FLASK_ENV=development
flask run
```

## License

This project is proprietary and not available for public use without permission.

