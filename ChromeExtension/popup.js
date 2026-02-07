const API_BASE = 'http://localhost:8000/api/v1';

// Check API connection on load
document.addEventListener('DOMContentLoaded', async () => {
    checkAPIConnection();
    loadSelectedText();
    
    // Update threshold display
    document.getElementById('threshold').addEventListener('change', (e) => {
        document.getElementById('thresholdValue').textContent = `${e.target.value} (${Math.round(e.target.value * 100)}%)`;
    });
});

// Check if API server is running
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE}/analysis/health`, {
            method: 'GET',
        });
        
        if (response.ok) {
            document.getElementById('serverStatus').innerHTML = '✓ Connected to CiteGuard API';
            document.getElementById('serverStatus').style.background = '#c8e6c9';
            document.getElementById('serverStatus').style.color = '#2e7d32';
            document.getElementById('serverStatus').style.borderColor = '#2e7d32';
        } else {
            showConnectionError('API returned an error');
        }
    } catch (error) {
        showConnectionError('Cannot connect to CiteGuard API. Make sure the server is running on http://localhost:8000');
    }
}

function showConnectionError(message) {
    const statusEl = document.getElementById('serverStatus');
    statusEl.innerHTML = `✗ ${message}`;
    statusEl.style.background = '#ffcdd2';
    statusEl.style.color = '#c62828';
    statusEl.style.borderColor = '#c62828';
}

// Load selected text from current page
function loadSelectedText() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getSelectedText' }, (response) => {
            if (response && response.selectedText) {
                document.getElementById('selectedText').value = response.selectedText;
            }
        });
    });
}

// Switch between tabs
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    
    // Deactivate buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Analyze selected text
async function analyzeSelectedText() {
    const text = document.getElementById('selectedText').value.trim();
    const threshold = parseFloat(document.getElementById('threshold').value);
    
    if (!text) {
        showError('analyzeError', 'Please select or paste some text');
        return;
    }
    
    const btn = document.getElementById('analyzeBtn');
    btn.innerHTML = '<span class="loading"></span> Analyzing...';
    btn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/analysis/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, threshold })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        const score = Math.min(data.plagiarism_score * 100, 100);
        document.getElementById('resultScore').textContent = score.toFixed(1) + '%';
        
        let status = '✓ Safe - No plagiarism detected';
        let className = 'safe';
        if (score > 75) {
            status = '⚠️ HIGH RISK - Likely plagiarism';
            className = 'danger';
        } else if (score > 50) {
            status = '⚠️ WARNING - Potential plagiarism';
            className = 'warning';
        }
        
        document.getElementById('resultStatus').innerHTML = `<div class="status ${className}">${status}</div>`;
        document.getElementById('analyzeResult').classList.remove('hidden');
        hideError('analyzeError');
    } catch (error) {
        showError('analyzeError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = 'Check for Plagiarism';
        btn.disabled = false;
    }
}

// Generate citation
async function generateCitation() {
    const title = document.getElementById('citTitle').value.trim();
    const authors = document.getElementById('citAuthor').value.trim()
        .split(',')
        .map(a => a.trim())
        .filter(a => a);
    const year = parseInt(document.getElementById('citYear').value);
    const style = document.getElementById('citStyle').value;
    
    if (!title) {
        showError('citError', 'Please enter a title');
        return;
    }
    
    const btn = document.getElementById('citBtn');
    btn.innerHTML = '<span class="loading"></span> Generating...';
    btn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/analysis/citation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, authors, year, style })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        document.getElementById('citationOutput').textContent = data.formatted_citation;
        document.getElementById('citResult').classList.remove('hidden');
        hideError('citError');
    } catch (error) {
        showError('citError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = 'Generate';
        btn.disabled = false;
    }
}

// Copy citation to clipboard
function copyCitation() {
    const text = document.getElementById('citationOutput').textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    });
}

// Error handling
function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError(elementId) {
    document.getElementById(elementId).classList.add('hidden');
}
