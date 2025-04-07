// Main JavaScript file for UPSL Team Scout

document.addEventListener('DOMContentLoaded', function() {
    // Set up filter tabs functionality
    initializeFilterTabs();
});

// Function to initialize filter tabs
function initializeFilterTabs() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Get the parent container to only affect tabs in the same group
            const tabsContainer = this.parentElement;
            
            // Remove active class from all tabs in this container
            tabsContainer.querySelectorAll('.filter-tab').forEach(t => {
                t.classList.remove('active');
            });
            
            // Add active class to the clicked tab
            this.classList.add('active');
            
            // Get the filter value
            const filter = this.dataset.filter;
            
            // In a real application, this would filter the content based on the filter value
            console.log(`Filter changed to: ${filter}`);
        });
    });
}

// Date formatting helper function
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
} 