/**
 * Content Script for CiteGuard
 * Injected into Google Docs, Office, Notion, and Overleaf
 * Detects text selection and analyzes for plagiarism
 */

console.log('CiteGuard content script loaded');

// Listen for text selection
document.addEventListener('mouseup', debounce(() => {
    const selectedText = window.getSelection().toString().trim();
    
    if (selectedText.length > 20) {
        // Send to background for analysis
        chrome.runtime.sendMessage({
            action: 'analyzeText',
            text: selectedText
        }, (response) => {
            if (response.success) {
                highlightAnalysis(response.data);
            } else {
                console.error('Analysis failed:', response.error);
            }
        });
    }
}, 500));

// Context menu for quick analysis and paraphrasing
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeSelection') {
        const text = window.getSelection().toString().trim();
        if (text) {
            chrome.runtime.sendMessage({
                action: 'analyzeText',
                text: text
            }, sendResponse);
        }
    }
});

/**
 * Highlight problematic sections in document
 */
function highlightAnalysis(analysisData) {
    const flaggedSections = analysisData.flagged_sections || [];
    
    flaggedSections.forEach((section) => {
        highlightText(section.text, 'citation-highlight');
    });
    
    // Show sidebar with results
    showAnalysisSidebar(analysisData);
}

/**
 * Highlight specific text in the page
 */
function highlightText(text, className) {
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    let node;
    while (node = walker.nextNode()) {
        if (node.nodeValue.includes(text)) {
            const span = document.createElement('span');
            span.textContent = text;
            span.className = className;
            node.parentNode.replaceChild(span, node);
        }
    }
}

/**
 * Show analysis results in sidebar
 */
function showAnalysisSidebar(data) {
    let sidebar = document.getElementById('citeguard-sidebar');
    
    if (!sidebar) {
        sidebar = document.createElement('div');
        sidebar.id = 'citeguard-sidebar';
        sidebar.className = 'citeguard-sidebar';
        document.body.appendChild(sidebar);
        
        // Load sidebar styles
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = chrome.runtime.getURL('content.css');
        document.head.appendChild(link);
    }
    
    sidebar.innerHTML = `
        <div class="sidebar-header">
            <h3>CiteGuard Analysis</h3>
            <button id="close-sidebar" class="close-btn">×</button>
        </div>
        <div class="sidebar-content">
            <div class="score-box">
                <div class="score-value">${data.overall_score.toFixed(1)}%</div>
                <div class="score-label">Originality</div>
            </div>
            <div class="recommendations">
                <h4>Recommendations:</h4>
                <ul>
                    ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('close-sidebar').addEventListener('click', () => {
        sidebar.style.display = 'none';
    });
}

/**
 * Debounce function for performance
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
