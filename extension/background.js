/**
 * Background Service Worker for CiteGuard
 * Handles message passing between content scripts and popup
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Background received message:', request.action);
    
    switch(request.action) {
        case 'analyzeText':
            handleAnalyzeText(request.text, sendResponse);
            break;
        case 'generateCitation':
            handleGenerateCitation(request.metadata, sendResponse);
            break;
        case 'paraphrase':
            handleParaphrase(request.text, sendResponse);
            break;
        default:
            sendResponse({ error: 'Unknown action' });
    }
    
    return true; // Keep channel open for async response
});

/**
 * Send text to backend for plagiarism analysis
 */
async function handleAnalyzeText(text, sendResponse) {
    try {
        const response = await fetch(`${API_BASE_URL}/analysis/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                sources: [],
                threshold: 0.85
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        sendResponse({ success: true, data: result });
    } catch (error) {
        console.error('Analysis error:', error);
        sendResponse({ success: false, error: error.message });
    }
}

/**
 * Generate citation from metadata
 */
async function handleGenerateCitation(metadata, sendResponse) {
    try {
        const response = await fetch(`${API_BASE_URL}/analysis/citation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(metadata)
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        sendResponse({ success: true, data: result });
    } catch (error) {
        console.error('Citation generation error:', error);
        sendResponse({ success: false, error: error.message });
    }
}

/**
 * Get paraphrasing suggestions
 */
async function handleParaphrase(text, sendResponse) {
    try {
        const response = await fetch(`${API_BASE_URL}/analysis/paraphrase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                num_alternatives: 3
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        sendResponse({ success: true, data: result });
    } catch (error) {
        console.error('Paraphrase error:', error);
        sendResponse({ success: false, error: error.message });
    }
}

// Service worker has persistent access to extension storage
console.log('CiteGuard background service worker loaded');
