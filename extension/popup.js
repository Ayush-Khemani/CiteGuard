/**
 * Popup Script for CiteGuard
 */

document.getElementById('analyzeBtn').addEventListener('click', () => {
    // Get active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTab = tabs[0];
        
        // Send analyze message to content script
        chrome.tabs.sendMessage(activeTab.id, {
            action: 'analyzeSelection'
        }, (response) => {
            if (response && response.success) {
                console.log('Analysis triggered on page');
            }
        });
    });
});

document.getElementById('settingsBtn').addEventListener('click', () => {
    // Open settings page or extension options
    chrome.runtime.openOptionsPage();
});

console.log('CiteGuard popup loaded');
