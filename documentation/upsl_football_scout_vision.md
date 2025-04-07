**Web Development Planning**  
**UPSLteamscout \- Video and Data Analysis tool for Amateur football**

**Home Page**

* URL directory: [www.upslteamscout.com](http://www.upslteamscout.com)  
* Toolbar and Navigation (ordered by left to right)  
  * Web tool logo on top left  
  * Home Page Button  
    * landing page for main url (i.e. home page)  
  * Clubs Page Button  
    * Has hovering functionality; list of clubs appears organized by conference (similar to fbref)  
    * When user clicks on a team, current page is replaced with new content for team selected  
    * Backend Data  
      * Club / Competition Navigation  
        * Team videos/stats are organized in separate google cloud buckets (upsl\_match\_videos & upsl\_match\_stats) based on the below hierarchy that will drive the navigation:  
          * upsl\_match\_videos \-\> Division \-\> Conference \-\> Season \-\> Club \-\> match.mp4  
            * Example: upsl\_match\_videos/Premier/Midwest\_Central/2024\_Fall/Chicago Strikers/  
          * upsl\_match\_stats \-\> Division \-\> Conference \-\> Season \-\> Club \-\> match\_stats.json  
            * Example: upsl\_match\_videos/Premier/Midwest\_Central/2024\_Fall/Chicago Strikers/match\_stats.json  
  * Competitions Page Button  
    * Has hovering functionality; list of competitions appears organized by division (similar to fbref)  
    * When user clicks on a team current page is replaced with new content for competition selected  
    * Backend Data  
      * Club / Competition Navigation  
        * Team videos/stats are organized in separate google cloud buckets (upsl\_match\_videos & upsl\_match\_stats) based on the below hierarchy that will drive the navigation:  
          * upsl\_match\_videos \-\> Division \-\> Conference \-\> Season \-\> Club \-\> match.mp4  
            * Example: upsl\_match\_videos/Premier/Midwest\_Central/2024\_Fall/Chicago Strikers/  
          * upsl\_match\_stats \-\> Division \-\> Conference \-\> Season \-\> Club \-\> match\_stats.json  
            * Example: upsl\_match\_videos/Premier/Midwest\_Central/2024\_Fall/Chicago Strikers/match\_stats.json  
  * User login and settings icons on top right  
    * ***Placeholder for now***  
* Content (ordered by left to right)   
  * Player Rankings table  
    * ***Placeholder for now***  
    * Table of player broad rankings (ranking determined in backend)  
    * Can filter by position rankings (All, GK, MF, Winger, FW, LB/RB, CB)  
    * Can scroll up down table while current page remains constant  
    * Can select players which replaces current page with new content for player selected (placeholder for now)  
  * Team Rankings table  
    * ***Placeholder for now***  
    * Table of team broad rankings (ranking determined in backend)  
    * Can scroll up down table while current page remains constant  
    * Can select teams which replaces current page with new content for team selected (placeholder for now)  
  * AI Chatbot  
    * ***Placeholder for now***  
  * Player Rankings Table  
    * ***Placeholder for now***  
    * Player metadata comes from the UPSL website that is scraped and stored in a nested json file following the same hierarchy as the google cloud buckets:  
      * ***Determine where to store this file; potentially store locally or in google cloud***  
      * Scraping tool functionality within a separate environment called UPSL-Webscraper  
      * ***Will need to figure out how to match player metadata to the nested json file generated below from the object and tracking model.***  
    * Stats generated from videos within upsl\_team\_videos bucket; output json files stored in upsl\_match\_stats bucket  
      * Process to generate stats  
        * Step 1: Object Detection (trained using Yolo) and Tracking (using ByteTrack) trained model applied to videos stored in upsl\_team\_videos bucket to generate a nested json file containing object positions and metadata.  
          * Ball, Player, Goalkeeper and Referee positions  
          * Currently have an independent environment (UPSL-Football-Analysis) dedicated to taking input videos, predicting object detections using YOLO, tracking objects across frames using ByteTrack, and differentiating by team using KMeans clustering based on colors.  
          * ***Still need to fine tune tracker and team differentiation.***  
        * Step 2: Application of deterministic decision tree-based algorithm for automatic event detection for each match in upsl\_match\_videos using tracking data generated from step 1\.  
          * Output files stored in upsl\_match\_stats bucket.  
          * ***Determine if this should be a new environment or implement within UPSL-Football-Analysis env.***  
        * Step 3: Generate player metrics and contextualized stats from tracking/event data generated from step 1 and 2  
          * ***Determine if this should be a new environment or implement within UPSL-Football-Analysis env.***  
        * Step 4: Aggregate stats to develop a methodology to rank performance of players.  
          * This will be the final output for the Player Rankings Table \- will reflect the current season.  
          * Output stored in upsl\_match\_stats bucket  
          * Determine if this should be a new environment or implement within UPSL-Football-Analysis env.  
  * Team Rankings Table  
    * ***Placeholder for now***  
    * Option to sort/rank teams by the below:  
      * All time record (W/D/L)  
        * All time record will come from scraped UPSL website json file with division/conference/season/team/player/roster metadata.  
        * All time record will be a league table of entire UPSL based on W/D/L  
      * Current form  
        * League table ranking based on last 10 games  
      * GD/xGD based ranking  
        * This feature will be added later on when stats database is complete to be able to calc xG for all teams based on contextual event data  
        * ***Need to determine where contextualized data/metrics will be stored relative to upsl metadata, tracking metadata and event data.***  
  * UPSL Scout AI Tool  
    * ***Placeholder for now***  
    * LLM Trained on all metadata json files and contextualized event/tracking data for players, teams and conferences.  
    * Model will be a conversation friendly tool that can provide quick snapshots on every player and team in the database.

**Clubs Page**

* URL directory: [www.upslteamscout/clubs/{team}.com](http://www.upslteamscout.com)  
* Toolbar and Navigation  
  * Main toolbar same as Home page; shows which page is currently selected  
* Content  
  * Team Name, Division and Conference on top left under toolbar matching the team selected  
  * Team roster of most recent 11/formation in pitch view  
    * Players organized based on team formation with initials/shortened version of name  
    * Current player rating based on last 3-5 games  
      * Rating will be driven by contextualized metrics that drive the player rankings table in Home page mapped to the relevant metadata  
  * Team Style Radar  
    * Spider radar chart showing team contextualized metrics relative to conference metrics to show a broad view of the team’s play style (same format as hudlstatsbomb)  
      * Contextualized metrics diven by same database driving the xG/GD ranking methodology in home page  
  * Separate Tab Buttons (Above team style radar & Below main tool bar)  
    * Video Library Tab  
      * Opens a new tab to the video library for the team selected  
      * URL: [www.upslteamscout/{team}/videolibrary.com](http://www.upslteamscout/{team}/videolibrary.com)  
      *  Toolbar and Navigation  
        * Web tool logo on top left  
        * Events: TBD \- placeholder for now  
        * User login and settings on top right  
      * Content  
        * Team Name, Division and Conference on top left under toolbar matching the team selected in clubs page  
        * Left panel (\~¼ of the page default but user can increase or decrease size viewed similar to in cursor or other tools)  
          * Hierarchical selection system of videos of clubs selected, organized by: Season \-\> match.mp4  
          * User can expand or collapse season to hide or view all matches from different seasons  
          * User selects mp4 for full match they want to load  
        * Video player (\~¾ of the page but user can increase or decrease size viewed similar to in cursor or other tools)  
          * Teams of video selected displayed on top of video player to the right of Team Name/conference/division  
          * Video selected in left panel is loaded to the video player with playback features such as:  
            * Pause button  
            * Play Button \- 1x speed  
            * Play Button \- 2x speed  
            * Play Button \- 3x speed  
            * Rewind Button  
            * Fast Forward Button  
            * Time stamp  
            * Slider scroll bar  
            * Volume Button  
            * Full Screen Button  
          * Annotate Frame Button  
            * When video is paused, an “Annotate Frame” button at the top left corner of video player empty space darkens giving user ability to click on it.  
            * After user clicks on it a new window opens:  
            * Annotate Frame Content  
              * URL: [www.upslteamscout/unitedsc/annotateimg.com](http://www.upslteamscout/unitedsc/annotateimg.com)    
              * Web tool logo on top left with same team details of team selected to the right  
              * Toolbar below team logo and team name with following features:  
                * Save Drawing \- drawing is added to the Video Tags list as a downloadable png (see VIdeo Tags below)  
                * Undo / redo  
                * Line style  
                * Line width  
                * Line Gradient  
              * Left panel with following annotation features:  
                * Select \- mouse icon  
                * Player annotation \- person icon \- allows user to click on a player and draws a circle around the selected player  
                * Connected Player Annotation \- 2 overlapping person icons \- allows user to click on multiple players and connect them by a line  
                * Pass annotation \- straight arrow icon \- allows user to draw an arrow showing direction of pass in a straight line  
                * Arc pass annotation \- curved arrow icon \- allows user to draw a curved pass  
                * Area annotation \- dashed box icon \- allows user to draw a boxed area  
                * Add text annotation \- text icon \- allows user to add text to frame  
              * Button at the button allowing user to download image as png “Export PNG”  
          * Video Tags tool panel  
            * Under video player  
            * Option to record / stop recording portion of video  
              * When recording is stopped the recorded clip is added to a list within the video tags panel  
                * User must name the clip which will be how it is shown in the list along with details such as time stamps and .mp4  
            * Any saved screenshots will also be listed here with name user selects along with time stamp and .png  
            * At the bottom right of the panel there is a “Export Content” button that will export anything in the panel.

**Version 1**

* Fully functioning video library access with annotating and video clipping capabilities \- user can export tagged annotations and clips  
* Bug Fixes  
  * Home Page  
    * When hovering over Clubs and Competitions tab it takes a couple seconds for the options to populate  
      * Options need to appear automatically  
    * Competitions Tab  
      * Currently looks like there are random competitions as placeholders \- can we replace this to “Conferences” and return the conferences available based on directory?  
      * Only conference available so far are Midwest\_Central  
  * Clubs Page  
    * Video Library  
      * Takes a while to load when clicking on it  
      * Unable to export saved clips within video tags  
    * Annotate tool  
      * Currently shows a blank screen with no annotation capabilities  
      * Currently unable to save drawing

