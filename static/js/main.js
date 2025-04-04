// Main JavaScript file for UPSL Team Scout

// Global variables to store preloaded data
let divisionsData = null;
let competitionsData = null;

document.addEventListener('DOMContentLoaded', function() {
    // Preload dropdown data as soon as the page loads
    preloadDropdownData();
    
    // Set up filter tabs functionality
    initializeFilterTabs();
    
    // Set up dropdown hover behavior
    setupDropdownHoverBehavior();
});

// Function to preload dropdown data
function preloadDropdownData() {
    console.log("Preloading dropdown data...");
    
    // Fetch divisions data
    fetch('/api/divisions')
        .then(response => response.json())
        .then(data => {
            console.log("Divisions data preloaded");
            divisionsData = data;
            // Pre-populate the dropdown
            populateDropdown('clubs-dropdown-content', divisionsData);
        })
        .catch(error => {
            console.error('Error preloading divisions:', error);
            populateDropdownWithMockData('clubs-dropdown-content', getClubsMockData());
        });
    
    // Fetch competitions data
    fetch('/api/competitions')
        .then(response => response.json())
        .then(data => {
            console.log("Competitions data preloaded");
            competitionsData = data;
            // Pre-populate the dropdown
            populateDropdown('competitions-dropdown-content', competitionsData);
        })
        .catch(error => {
            console.error('Error preloading competitions:', error);
            populateDropdownWithMockData('competitions-dropdown-content', getCompetitionsMockData());
        });
}

// Function to set up dropdown hover behavior
function setupDropdownHoverBehavior() {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            const dropdownContent = this.querySelector('.dropdown-content');
            dropdownContent.style.display = 'block';
        });
        
        dropdown.addEventListener('mouseleave', function() {
            const dropdownContent = this.querySelector('.dropdown-content');
            dropdownContent.style.display = 'none';
        });
    });
}

// Function to initialize dropdowns with dynamic data
function initializeDropdowns() {
    // Fetch divisions and conferences for the clubs dropdown
    console.log("Fetching divisions data...");
    fetch('/api/divisions')
        .then(response => {
            console.log("Divisions API response status:", response.status);
            if (!response.ok) {
                console.error("Error fetching divisions:", response.statusText);
                populateDropdownWithMockData('clubs-dropdown-content', getClubsMockData());
                return null;
            }
            return response.json();
        })
        .then(data => {
            console.log("Divisions data received:", data);
            if (data) {
                populateDropdown('clubs-dropdown-content', data);
            } else {
                console.warn("No divisions data received, using mock data");
                populateDropdownWithMockData('clubs-dropdown-content', getClubsMockData());
            }
        })
        .catch(error => {
            console.error('Error fetching divisions:', error);
            populateDropdownWithMockData('clubs-dropdown-content', getClubsMockData());
        });
    
    // Fetch competitions for the competitions dropdown
    console.log("Fetching competitions data...");
    fetch('/api/competitions')
        .then(response => {
            console.log("Competitions API response status:", response.status);
            if (!response.ok) {
                console.error("Error fetching competitions:", response.statusText);
                populateDropdownWithMockData('competitions-dropdown-content', getCompetitionsMockData());
                return null;
            }
            return response.json();
        })
        .then(data => {
            console.log("Competitions data received:", data);
            if (data) {
                populateDropdown('competitions-dropdown-content', data);
            } else {
                console.warn("No competitions data received, using mock data");
                populateDropdownWithMockData('competitions-dropdown-content', getCompetitionsMockData());
            }
        })
        .catch(error => {
            console.error('Error fetching competitions:', error);
            populateDropdownWithMockData('competitions-dropdown-content', getCompetitionsMockData());
        });
}

// Function to populate a dropdown with data
function populateDropdown(elementId, data) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let html = '';
    
    if (elementId === 'clubs-dropdown-content') {
        // Format for clubs dropdown
        for (const division in data) {
            html += `<div class="dropdown-category">${division}</div>`;
            
            for (const conference in data[division]) {
                html += `<div class="dropdown-subcategory">${conference}</div>`;
                
                data[division][conference].forEach(club => {
                    html += `<a href="/clubs/${encodeURIComponent(club)}">${club}</a>`;
                });
            }
        }
    } else if (elementId === 'competitions-dropdown-content') {
        // Format for competitions dropdown
        for (const division in data) {
            html += `<div class="dropdown-category">${division}</div>`;
            
            data[division].forEach(competition => {
                html += `<a href="/competitions/${encodeURIComponent(competition)}">${competition}</a>`;
            });
        }
    }
    
    element.innerHTML = html;
}

// Function to populate dropdown with mock data when API is not available
function populateDropdownWithMockData(elementId, mockData) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.innerHTML = mockData;
}

// Function to get mock data for clubs dropdown
function getClubsMockData() {
    return `
        <div class="dropdown-category">Premier Division</div>
        <div class="dropdown-subcategory">Midwest Conference</div>
        <a href="/clubs/Chicago-Strikers">Chicago Strikers</a>
        <a href="/clubs/Milwaukee-FC">Milwaukee FC</a>
        <a href="/clubs/Detroit-City">Detroit City</a>
        
        <div class="dropdown-subcategory">Northeast Conference</div>
        <a href="/clubs/New-York-Warriors">New York Warriors</a>
        <a href="/clubs/Boston-United">Boston United</a>
        <a href="/clubs/Philadelphia-Stars">Philadelphia Stars</a>
        
        <div class="dropdown-category">Division 1</div>
        <div class="dropdown-subcategory">West Conference</div>
        <a href="/clubs/LA-Legends">LA Legends</a>
        <a href="/clubs/San-Diego-FC">San Diego FC</a>
        <a href="/clubs/Seattle-Sounders">Seattle Sounders</a>
    `;
}

// Function to get mock data for competitions dropdown
function getCompetitionsMockData() {
    return `
        <div class="dropdown-category">Premier Division</div>
        <a href="/competitions/Premier-National">National Championship</a>
        <a href="/competitions/Premier-Midwest">Midwest Conference</a>
        <a href="/competitions/Premier-Northeast">Northeast Conference</a>
        <a href="/competitions/Premier-Southeast">Southeast Conference</a>
        <a href="/competitions/Premier-Southwest">Southwest Conference</a>
        <a href="/competitions/Premier-West">West Conference</a>
        
        <div class="dropdown-category">Division 1</div>
        <a href="/competitions/Division1-National">National Championship</a>
        <a href="/competitions/Division1-Midwest">Midwest Conference</a>
        <a href="/competitions/Division1-Northeast">Northeast Conference</a>
        <a href="/competitions/Division1-Southeast">Southeast Conference</a>
        <a href="/competitions/Division1-Southwest">Southwest Conference</a>
        <a href="/competitions/Division1-West">West Conference</a>
    `;
}

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