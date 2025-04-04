function redraw(imageUrl) {
    const img = new Image();
    img.src = imageUrl;
    img.onload = function() {
        const canvas = document.getElementById('annotationCanvas');
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas before drawing
        ctx.drawImage(img, 0, 0);
    };
    img.onerror = function() {
        console.error('Failed to load image for drawing');
    };
} 