// Variables to store the canvas state
let canvas;
let ctx;
let currentTool = 'select';
let isDrawing = false;
let startX, startY;
let objects = [];
let selectedObject = null;
let redoStack = [];
let videoFrame = null;

// Initialize the annotation tool
document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById('annotationCanvas');
    if (!canvas) return;
    
    ctx = canvas.getContext('2d');
    
    // Get video frame URL from query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('video_id');
    const timestamp = urlParams.get('timestamp');
    const frameUrl = urlParams.get('frame');
    
    // Load the video frame
    loadVideoFrame(frameUrl, videoId, timestamp);
    
    // Set up tool buttons
    setupToolButtons();
    
    // Add canvas event listeners
    setupCanvasListeners();
    
    // Set up other UI controls
    setupUIControls();
});

// Function to load video frame
function loadVideoFrame(frameUrl, videoId, timestamp) {
    // Create a frame image
    videoFrame = new Image();
    
    // Check if we have a data URL from the frameDataUrl element
    const frameDataUrlElement = document.getElementById('frameDataUrl');
    if (frameDataUrlElement && frameDataUrlElement.value) {
        videoFrame.src = frameDataUrlElement.value;
        console.log("Using frame from data URL");
    } 
    // If no frame URL is provided, use a placeholder
    else if (!frameUrl) {
        videoFrame.src = "/static/images/soccer_field.jpg";
        console.warn("No frame URL provided, using placeholder");
    } else {
        videoFrame.src = frameUrl;
    }
    
    videoFrame.onload = function() {
        // Draw the frame image once it's loaded
        canvas.width = this.width || 800;
        canvas.height = this.height || 450;
        ctx.drawImage(videoFrame, 0, 0, canvas.width, canvas.height);
        
        // Update frame info
        if (videoId && timestamp) {
            document.querySelector('.frame-info').innerHTML = `
                <span>Video: ${videoId}</span>
                <span>Time: ${timestamp}</span>
            `;
        }
    };
    
    videoFrame.onerror = function() {
        console.error("Error loading video frame");
        // Draw fallback
        ctx.fillStyle = "#333";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fff";
        ctx.font = "20px Arial";
        ctx.textAlign = "center";
        ctx.fillText("Error loading video frame", canvas.width/2, canvas.height/2);
    };
}

// Function to set up tool buttons
function setupToolButtons() {
    const toolButtons = document.querySelectorAll('.tool-btn');
    toolButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            toolButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentTool = this.id.replace('Tool', '');
        });
    });
    
    // Set up the select tool as active by default
    document.getElementById('selectTool').classList.add('active');
}

// Function to set up canvas listeners
function setupCanvasListeners() {
    // Mouse down event
    canvas.addEventListener('mousedown', function(e) {
        const rect = canvas.getBoundingClientRect();
        startX = e.clientX - rect.left;
        startY = e.clientY - rect.top;
        isDrawing = true;
        
        // Check if we're selecting an object
        if (currentTool === 'select') {
            selectedObject = getObjectAt(startX, startY);
        }
    });
    
    // Mouse move event
    canvas.addEventListener('mousemove', function(e) {
        if (!isDrawing) return;
        
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Handle drawing based on the current tool
        if (currentTool === 'select' && selectedObject) {
            // Move the selected object
            moveObject(selectedObject, x - startX, y - startY);
            startX = x;
            startY = y;
            redraw();
        } else if (currentTool === 'straightArrow') {
            // Draw a preview of the arrow
            redraw();
            drawArrow(startX, startY, x, y);
        } else if (currentTool === 'areaAnnotation') {
            // Draw a preview of the rectangle
            redraw();
            drawRectangle(startX, startY, x - startX, y - startY);
        }
    });
    
    // Mouse up event
    canvas.addEventListener('mouseup', function(e) {
        if (!isDrawing) return;
        
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Add the drawing to objects array based on the current tool
        if (currentTool === 'straightArrow') {
            objects.push({
                type: 'straightArrow',
                startX: startX,
                startY: startY,
                endX: x,
                endY: y,
                color: document.getElementById('lineColor').value,
                width: parseInt(document.getElementById('lineWidth').value),
                style: document.getElementById('lineStyle').value
            });
        } else if (currentTool === 'areaAnnotation') {
            objects.push({
                type: 'areaAnnotation',
                x: Math.min(startX, x),
                y: Math.min(startY, y),
                width: Math.abs(x - startX),
                height: Math.abs(y - startY),
                color: document.getElementById('lineColor').value,
                lineWidth: parseInt(document.getElementById('lineWidth').value),
                style: document.getElementById('lineStyle').value
            });
        } else if (currentTool === 'playerAnnotation') {
            objects.push({
                type: 'playerAnnotation',
                x: x,
                y: y,
                radius: 10,
                color: document.getElementById('lineColor').value,
                lineWidth: parseInt(document.getElementById('lineWidth').value)
            });
        }
        
        // Clear the redo stack
        redoStack = [];
        
        // Reset drawing state
        isDrawing = false;
        selectedObject = null;
        
        // Redraw canvas
        redraw();
    });
}

// Function to set up UI controls
function setupUIControls() {
    // Set up line style, width, and color pickers
    document.getElementById('lineStyle').addEventListener('change', redraw);
    document.getElementById('lineWidth').addEventListener('input', redraw);
    document.getElementById('lineColor').addEventListener('input', redraw);
    
    // Set up undo/redo buttons
    document.getElementById('undoBtn').addEventListener('click', undo);
    document.getElementById('redoBtn').addEventListener('click', redo);
    
    // Set up save button
    document.getElementById('saveBtn').addEventListener('click', saveDrawing);
    
    // Set up export button
    document.getElementById('exportBtn').addEventListener('click', exportPNG);
}

// Function to redraw the canvas
function redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw the video frame first
    if (videoFrame) {
        ctx.drawImage(videoFrame, 0, 0, canvas.width, canvas.height);
    }
    
    // Draw all objects
    objects.forEach(drawObject);
}

// More functions here for drawing objects, undo/redo, etc. (keeping same functionality)

// Function to save the drawing
function saveDrawing() {
    // Get the canvas data URL
    const dataURL = canvas.toDataURL('image/png');
    
    // Get video ID and timestamp from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('video_id') || 'unknown';
    const timestamp = urlParams.get('timestamp') || '00:00:00';
    
    // Create form data
    const formData = new FormData();
    formData.append('image', dataURL);
    formData.append('video_id', videoId);
    formData.append('timestamp', timestamp);
    formData.append('objects', JSON.stringify(objects));
    
    // Send to server
    fetch('/api/save_annotation', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Annotation saved successfully!');
        } else {
            alert('Error saving annotation: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error saving annotation:', error);
        alert('Error saving annotation. Please try again.');
    });
} 