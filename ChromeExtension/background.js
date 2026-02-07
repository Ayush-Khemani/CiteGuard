// Background service worker for CiteGuard extension

const API_BASE = 'http://localhost:8000/api/v1';

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeText') {
        analyzeTextInBackground(request.text, sendResponse);
        return true; // Keep channel open for async response
    }
});

// Analyze text from background script
async function analyzeTextInBackground(text, callback) {
    try {
        const response = await fetch(`${API_BASE}/analysis/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, threshold: 0.7 })
        });
        
        if (response.ok) {
            const data = await response.json();
            callback({ success: true, data: data });
        } else {
            callback({ success: false, error: 'API Error' });
        }
    } catch (error) {
        callback({ success: false, error: error.message });
    }
}

// Extension icon click handler
chrome.action.onClicked.addListener((tab) => {
    // Open the popup when extension icon is clicked
    chrome.action.openPopup();
});

console.log('CiteGuard background service worker started');
