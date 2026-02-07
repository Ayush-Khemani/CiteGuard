// Content script - runs on all web pages
// Listens for selected text and provides plagiarism checking

// Get selected text
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getSelectedText') {
        const selectedText = window.getSelection().toString();
        sendResponse({ selectedText: selectedText });
    }
});

// Add selected text indicator
document.addEventListener('mouseup', () => {
    const selectedText = window.getSelection().toString();
    
    if (selectedText.length > 10) {
        // Show a small tooltip indicating text is selected
        createFloatingButton(selectedText);
    }
});

// Create floating button for selected text
function createFloatingButton(selectedText) {
    // Remove existing button
    const existing = document.getElementById('citeguard-floating-btn');
    if (existing) {
        existing.remove();
    }
    
    if (selectedText.length < 10) return;
    
    const button = document.createElement('div');
    button.id = 'citeguard-floating-btn';
    button.innerHTML = '📋 Check Plagiarism';
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        z-index: 10000;
        border: none;
        font-size: 14px;
        transition: all 0.3s;
    `;
    
    button.addEventListener('mouseover', () => {
        button.style.transform = 'translateY(-2px)';
        button.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
    });
    
    button.addEventListener('mouseout', () => {
        button.style.transform = 'translateY(0)';
        button.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
    });
    
    button.addEventListener('click', () => {
        chrome.runtime.sendMessage({
            action: 'analyzeText',
            text: selectedText
        }, (response) => {
            if (response && response.success) {
                showAnalysisResult(response.data);
            }
        });
    });
    
    document.body.appendChild(button);
    
    // Remove after 5 seconds of no selection
    setTimeout(() => {
        if (window.getSelection().toString().length === 0) {
            button.remove();
        }
    }, 5000);
}

// Show analysis result notification
function showAnalysisResult(data) {
    const notification = document.createElement('div');
    notification.id = 'citeguard-notification';
    
    const score = data.plagiarism_score * 100;
    let statusColor = '#4caf50'; // green
    let statusText = 'SAFE';
    
    if (score > 75) {
        statusColor = '#f44336'; // red
        statusText = 'HIGH RISK';
    } else if (score > 50) {
        statusColor = '#ff9800'; // orange
        statusText = 'WARNING';
    }
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-left: 4px solid ${statusColor};
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        z-index: 10001;
        max-width: 300px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    `;
    
    notification.innerHTML = `
        <div style="font-weight: 600; color: ${statusColor}; margin-bottom: 8px;">
            ${statusText}
        </div>
        <div style="color: #333; font-size: 14px; margin-bottom: 4px;">
            Plagiarism Score: <strong>${score.toFixed(1)}%</strong>
        </div>
        <div style="color: #666; font-size: 13px;">
            ${data.flagged_sections || 0} suspicious sections detected
        </div>
        <button onclick="this.parentElement.remove()" style="
            margin-top: 8px;
            width: 100%;
            padding: 8px;
            border: 1px solid #e0e0e0;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        ">Dismiss</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 8000);
}

// Highlight suspicious content on the page
function highlightSuspiciousText(flaggedSections) {
    flaggedSections.forEach((section) => {
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            if (node.textContent.includes(section)) {
                const span = document.createElement('span');
                span.style.backgroundColor = 'rgba(255, 193, 7, 0.3)';
                span.style.borderBottom = '2px dashed #ffc107';
                span.textContent = node.textContent;
                node.parentNode.replaceChild(span, node);
            }
        }
    });
}

console.log('CiteGuard content script loaded - Ready to analyze text');
