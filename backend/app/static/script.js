const API_BASE = 'http://localhost:8000/api/v1';

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Deactivate all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate selected button
    event.target.classList.add('active');
}

// Analyze Text
async function analyzeText() {
    const text = document.getElementById('analyzeText').value.trim();
    const threshold = parseFloat(document.getElementById('threshold').value);

    if (!text) {
        showError('analyzeError', 'Please enter text to analyze');
        return;
    }

    const btn = document.getElementById('analyzeBtn');
    const startTime = Date.now();
    btn.innerHTML = '<span class="loading"></span> Analyzing...';
    btn.disabled = true;

    try {
        console.log('Sending analyze request to:', `${API_BASE}/analysis/analyze`);
        console.log('Stored documents count:', storedDocuments.length);
        
        // Build sources from stored documents
        const sources = storedDocuments.map(doc => ({
            title: doc.title,
            content: doc.content,
            url: doc.sourceUrl
        }));
        
        const payload = { 
            text, 
            threshold,
            sources: sources
        };
        
        console.log('Payload sources:', sources.length > 0 ? sources.length + ' documents' : 'No documents');
        
        const response = await fetch(`${API_BASE}/analysis/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('API Error:', errorData);
            throw new Error(`API Error ${response.status}: ${errorData.detail || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('Analysis response:', data);
        
        const endTime = Date.now();

        // Display results - plagiarism_score is 0-1, convert to 0-100
        const score = Math.min((data.plagiarism_score || 0) * 100, 100);
        document.getElementById('scoreBar').style.width = score + '%';
        document.getElementById('scorePercent').textContent = score.toFixed(1) + '%';

        // Status
        let status = '✓ Safe - No plagiarism detected';
        let statusClass = 'safe';
        if (score > 75) {
            status = '⚠️ High Plagiarism Risk';
            statusClass = 'dangerous';
        } else if (score > 50) {
            status = '⚠️ Moderate Plagiarism Risk';
            statusClass = 'warning';
        }
        const statusEl = document.getElementById('plagiarismStatus');
        statusEl.textContent = status;
        statusEl.className = `status-badge ${statusClass}`;

        document.getElementById('flaggedCount').textContent = data.flagged_sections || 0;
        document.getElementById('processingTime').textContent = (endTime - startTime) + 'ms';

        // Recommendations
        const recList = document.getElementById('recommendations');
        recList.innerHTML = '';
        const recommendations = data.recommendations || [];
        if (recommendations.length === 0) {
            recList.innerHTML = '<li>Text analysis complete</li>';
        } else {
            recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recList.appendChild(li);
            });
        }

        document.getElementById('analyzeResults').classList.remove('hidden');
        hideError('analyzeError');
    } catch (error) {
        console.error('Analyze error:', error);
        showError('analyzeError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = 'Analyze Text';
        btn.disabled = false;
    }
}

// Paraphrase Text
async function paraphraseText() {
    const text = document.getElementById('paraText').value.trim();
    const style = document.getElementById('paraStyle').value;

    if (!text) {
        showError('paraError', 'Please enter text to paraphrase');
        return;
    }

    const btn = document.getElementById('paraBtn');
    btn.innerHTML = '<span class="loading"></span> Paraphrasing...';
    btn.disabled = true;

    try {
        console.log('Sending paraphrase request');
        const response = await fetch(`${API_BASE}/analysis/paraphrase`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, context: style })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API Error ${response.status}: ${errorData.detail || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('Paraphrase response:', data);
        
        document.getElementById('paraOutput').value = data.paraphrased_text || 'Unable to paraphrase. This feature requires LLM integration.';
        document.getElementById('paraResults').classList.remove('hidden');
        hideError('paraError');
    } catch (error) {
        console.error('Paraphrase error:', error);
        showError('paraError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = 'Paraphrase';
        btn.disabled = false;
    }
}

// Generate Citation
async function generateCitation() {
    const title = document.getElementById('citationTitle').value.trim();
    const authors = document.getElementById('citationAuthors').value.trim().split(',').map(a => a.trim()).filter(a => a);
    const year = parseInt(document.getElementById('citationYear').value);
    const style = document.getElementById('citationStyle').value;

    if (!title) {
        showError('citationError', 'Please enter a title');
        return;
    }

    const btn = document.getElementById('citationBtn');
    btn.innerHTML = '<span class="loading"></span> Generating...';
    btn.disabled = true;

    try {
        console.log('Sending citation request');
        const response = await fetch(`${API_BASE}/analysis/citation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title, 
                authors, 
                year, 
                citation_style: style 
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`API Error ${response.status}: ${errorData.detail || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('Citation response:', data);
        
        document.getElementById('citationOutput').textContent = data.formatted_citation;
        document.getElementById('citationResults').classList.remove('hidden');
        hideError('citationError');
    } catch (error) {
        console.error('Citation error:', error);
        showError('citationError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = 'Generate Citation';
        btn.disabled = false;
    }
}

// Copy to Clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.value || element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Copy Citation
function copyCitation() {
    copyToClipboard('citationOutput');
}

// Error Handling
function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError(elementId) {
    document.getElementById(elementId).classList.add('hidden');
}

// Test API on page load
// Document Management
let storedDocuments = JSON.parse(localStorage.getItem('documents')) || [];

async function uploadDocument() {
    const title = document.getElementById('docTitle').value.trim();
    const content = document.getElementById('docContent').value.trim();
    const sourceUrl = document.getElementById('docSource').value.trim();

    if (!title) {
        showError('uploadError', 'Please enter a document title');
        return;
    }
    if (!content) {
        showError('uploadError', 'Please enter document content');
        return;
    }

    const btn = document.getElementById('uploadBtn');
    btn.innerHTML = '⏳ Uploading...';

    try {
        // Create document object
        const docData = {
            id: Date.now(),
            title,
            content,
            sourceUrl,
            uploadedAt: new Date().toLocaleString()
        };

        // Store in localStorage
        storedDocuments.push(docData);
        localStorage.setItem('documents', JSON.stringify(storedDocuments));

        // Clear form
        document.getElementById('docTitle').value = '';
        document.getElementById('docContent').value = '';
        document.getElementById('docSource').value = '';

        showSuccess('uploadSuccess', `✓ Document "${title}" uploaded successfully!`);
        hideError('uploadError');

        // Refresh list
        displayDocuments();

        // Clear success message after 3 seconds
        setTimeout(() => hideSuccess('uploadSuccess'), 3000);
    } catch (error) {
        console.error('Upload error:', error);
        showError('uploadError', 'Error: ' + error.message);
    } finally {
        btn.innerHTML = '📤 Upload Document';
    }
}

function displayDocuments() {
    const listDiv = document.getElementById('documentsList');
    
    if (storedDocuments.length === 0) {
        listDiv.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No documents uploaded yet</p>';
        return;
    }

    listDiv.innerHTML = storedDocuments.map(doc => `
        <div class="document-item">
            <div style="flex: 1;">
                <h4 style="margin: 0 0 8px 0;">${escapeHtml(doc.title)}</h4>
                <p style="margin: 0; color: #666; font-size: 0.9em;">
                    Uploaded: ${doc.uploadedAt}<br>
                    Words: ${doc.content.split(/\s+/).length}
                </p>
                ${doc.sourceUrl ? `<p style="margin: 5px 0 0; color: #0066cc; font-size: 0.85em;"><a href="${escapeHtml(doc.sourceUrl)}" target="_blank">Source</a></p>` : ''}
            </div>
            <button class="btn btn-danger" onclick="deleteDocument(${doc.id})" style="padding: 8px 12px; margin-top: auto;">
                🗑️ Delete
            </button>
        </div>
    `).join('');
}

function deleteDocument(docId) {
    if (confirm('Are you sure you want to delete this document?')) {
        storedDocuments = storedDocuments.filter(doc => doc.id !== docId);
        localStorage.setItem('documents', JSON.stringify(storedDocuments));
        displayDocuments();
        showSuccess('uploadSuccess', '✓ Document deleted');
        setTimeout(() => hideSuccess('uploadSuccess'), 2000);
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.remove('hidden');
    }
}

function hideSuccess(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    // Display stored documents
    displayDocuments();
    
    try {
        const response = await fetch(`${API_BASE}/analysis/health`);
        if (response.ok) {
            console.log('✓ API Connection Established');
        }
    } catch (error) {
        console.error('✗ API Connection Failed:', error);
    }
});
