// Functions for the video player

document.addEventListener('DOMContentLoaded', function() {
    const videoPlayer = document.getElementById('videoPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const captureBtn = document.getElementById('captureBtn');
    const timelineContainer = document.querySelector('.timeline-container');
    const currentTimeDisplay = document.getElementById('currentTime');
    const totalTimeDisplay = document.getElementById('totalTime');
    const clipStartBtn = document.getElementById('clipStartBtn');
    const clipEndBtn = document.getElementById('clipEndBtn');
    const exportClipBtn = document.getElementById('exportClipBtn');
    
    // Variables for storing clip start and end times
    let clipStartTime = null;
    let clipEndTime = null;
    
    if (!videoPlayer) return;
    
    // Play/Pause functionality
    playPauseBtn.addEventListener('click', function() {
        if (videoPlayer.paused) {
            videoPlayer.play();
            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            videoPlayer.pause();
            playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
    });
    
    // Fullscreen functionality
    fullscreenBtn.addEventListener('click', function() {
        if (videoPlayer.requestFullscreen) {
            videoPlayer.requestFullscreen();
        } else if (videoPlayer.webkitRequestFullscreen) {
            videoPlayer.webkitRequestFullscreen();
        } else if (videoPlayer.msRequestFullscreen) {
            videoPlayer.msRequestFullscreen();
        }
    });
    
    // Capture current frame
    captureBtn.addEventListener('click', function() {
        // Pause the video
        videoPlayer.pause();
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        
        // Get current video time
        const time = videoPlayer.currentTime;
        const formattedTime = formatTime(time);
        
        // Create a canvas to capture the current frame
        const canvas = document.createElement('canvas');
        canvas.width = videoPlayer.videoWidth;
        canvas.height = videoPlayer.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoPlayer, 0, 0, canvas.width, canvas.height);
        
        // Get the data URL of the frame
        const frameDataUrl = canvas.toDataURL('image/png');
        
        // Get video ID from the src
        const videoId = videoPlayer.dataset.videoId || 'unknown';
        
        // Open annotation tool with the captured frame
        window.open(`/clubs/${getTeamNameFromUrl()}/annotateimg?video_id=${encodeURIComponent(videoId)}&timestamp=${time}&frame=${encodeURIComponent(frameDataUrl)}`, '_blank');
    });
    
    // Time display and timeline
    videoPlayer.addEventListener('loadedmetadata', function() {
        totalTimeDisplay.textContent = formatTime(videoPlayer.duration);
    });
    
    videoPlayer.addEventListener('timeupdate', function() {
        currentTimeDisplay.textContent = formatTime(videoPlayer.currentTime);
        const percentage = (videoPlayer.currentTime / videoPlayer.duration) * 100;
        timelineContainer.querySelector('.timeline-progress').style.width = `${percentage}%`;
    });
    
    timelineContainer.addEventListener('click', function(e) {
        const rect = timelineContainer.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        videoPlayer.currentTime = pos * videoPlayer.duration;
    });
    
    // Clip start/end buttons
    clipStartBtn.addEventListener('click', function() {
        clipStartTime = videoPlayer.currentTime;
        alert(`Clip start set to ${formatTime(clipStartTime)}`);
    });
    
    clipEndBtn.addEventListener('click', function() {
        clipEndTime = videoPlayer.currentTime;
        alert(`Clip end set to ${formatTime(clipEndTime)}`);
    });
    
    // Export clip functionality
    exportClipBtn.addEventListener('click', function() {
        if (clipStartTime === null || clipEndTime === null) {
            alert('Please set both clip start and end times');
            return;
        }
        
        if (clipStartTime >= clipEndTime) {
            alert('Clip start time must be before clip end time');
            return;
        }
        
        const clipName = prompt('Enter a name for this clip:', '');
        if (clipName === null) return;
        
        // Show loading indicator
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'clip-loading';
        loadingIndicator.innerHTML = '<div class="spinner"></div><p>Exporting clip...</p>';
        document.body.appendChild(loadingIndicator);
        
        // Get the video ID
        const videoId = videoPlayer.src.split('/').slice(-1)[0];
        
        // Create form data
        const formData = new FormData();
        formData.append('video_id', videoId);
        formData.append('start_time', formatTime(clipStartTime));
        formData.append('end_time', formatTime(clipEndTime));
        formData.append('clip_name', clipName);
        
        // Send to server
        fetch('/api/export_clip', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            document.body.removeChild(loadingIndicator);
            
            if (data.success) {
                alert('Clip exported successfully!');
                
                // Create download link
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = data.filename;
                link.textContent = 'Download Clip';
                
                // Add to video tags
                const tagsContainer = document.querySelector('.video-tags');
                const tagItem = document.createElement('div');
                tagItem.className = 'tag-item';
                tagItem.innerHTML = `
                    <span class="tag-title">Clip: ${clipName || 'Unnamed'}</span>
                    <span class="tag-time">${formatTime(clipStartTime)} - ${formatTime(clipEndTime)}</span>
                `;
                tagItem.appendChild(link);
                tagsContainer.appendChild(tagItem);
            } else {
                alert('Error exporting clip: ' + data.error);
            }
        })
        .catch(error => {
            // Remove loading indicator
            document.body.removeChild(loadingIndicator);
            
            console.error('Error exporting clip:', error);
            alert('Error exporting clip. Please try again.');
        });
    });
});

// Helper function to format time in HH:MM:SS
function formatTime(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

// Helper function to get team name from URL
function getTeamNameFromUrl() {
    const path = window.location.pathname;
    const parts = path.split('/');
    return parts[parts.indexOf('clubs') + 1];
} 