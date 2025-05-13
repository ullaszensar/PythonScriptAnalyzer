// Main JavaScript functionality for PyTable Analyzer

document.addEventListener('DOMContentLoaded', function() {
    // Handle file upload form
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('file-input');
            const sourceInput = document.getElementById('source-input');
            
            // Validate at least one input method is provided
            if (fileInput.files.length === 0 && (!sourceInput.value || sourceInput.value.trim() === '')) {
                e.preventDefault();
                showAlert('Please either upload files or paste code to analyze', 'danger');
            }
        });
    }
    
    // File input change handler to display selected files
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    
    if (fileInput && fileList) {
        fileInput.addEventListener('change', function() {
            fileList.innerHTML = '';
            
            if (this.files.length > 0) {
                const listGroup = document.createElement('div');
                listGroup.className = 'list-group mt-3';
                
                for (let i = 0; i < this.files.length; i++) {
                    const file = this.files[i];
                    const item = document.createElement('div');
                    item.className = 'list-group-item d-flex justify-content-between align-items-center';
                    
                    // File icon based on type
                    let icon = 'bi-file-code';
                    if (file.name.endsWith('.py')) {
                        icon = 'bi-filetype-py';
                    } else if (file.name.endsWith('.sh') || file.name.endsWith('.bash')) {
                        icon = 'bi-terminal';
                    }
                    
                    item.innerHTML = `
                        <div>
                            <i class="bi ${icon} me-2"></i>
                            ${file.name}
                        </div>
                        <span class="badge bg-primary rounded-pill">${formatFileSize(file.size)}</span>
                    `;
                    
                    listGroup.appendChild(item);
                }
                
                fileList.appendChild(listGroup);
            }
        });
    }
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize code editor if source input exists
    const sourceInput = document.getElementById('source-input');
    if (sourceInput) {
        // Simple syntax highlighting can be added here if needed
        sourceInput.addEventListener('input', function() {
            // Update file name based on content detection
            updateFileNameFromContent(this.value);
        });
    }
    
    // Handle tabs in the textarea
    if (sourceInput) {
        sourceInput.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                
                // Insert tab at cursor position
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
                
                // Move cursor after the inserted tab
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    }
});

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
}

// Initialize search functionality on results page
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterResults(searchTerm);
    });
}

// Filter results based on search term
function filterResults(searchTerm) {
    const tables = document.querySelectorAll('.table-item');
    
    tables.forEach(table => {
        const tableName = table.querySelector('.table-name').textContent.toLowerCase();
        const fields = Array.from(table.querySelectorAll('.field-item'));
        
        // Check if table name matches
        const tableMatches = tableName.includes(searchTerm);
        
        // Check if any field matches
        const fieldMatches = fields.some(field => {
            const fieldName = field.querySelector('.field-name').textContent.toLowerCase();
            const fieldType = field.querySelector('.field-type')?.textContent.toLowerCase() || '';
            
            return fieldName.includes(searchTerm) || fieldType.includes(searchTerm);
        });
        
        // Show/hide table based on match
        if (tableMatches || fieldMatches) {
            table.style.display = '';
            
            // If searching, highlight matching fields and hide non-matching
            if (searchTerm) {
                fields.forEach(field => {
                    const fieldName = field.querySelector('.field-name').textContent.toLowerCase();
                    const fieldType = field.querySelector('.field-type')?.textContent.toLowerCase() || '';
                    
                    if (fieldName.includes(searchTerm) || fieldType.includes(searchTerm)) {
                        field.style.display = '';
                        field.classList.add('bg-light');
                    } else {
                        if (tableMatches) {
                            field.style.display = '';
                            field.classList.remove('bg-light');
                        } else {
                            field.style.display = 'none';
                        }
                    }
                });
            } else {
                // Reset field visibility and highlighting
                fields.forEach(field => {
                    field.style.display = '';
                    field.classList.remove('bg-light');
                });
            }
        } else {
            table.style.display = 'none';
        }
    });
    
    // Check if any results are visible
    const visibleTables = Array.from(tables).filter(table => table.style.display !== 'none');
    const noResultsMessage = document.getElementById('no-results-message');
    
    if (noResultsMessage) {
        if (visibleTables.length === 0 && searchTerm) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }
}

// Try to detect the type of file based on content
function updateFileNameFromContent(content) {
    const filenameInput = document.getElementById('filename-input');
    if (!filenameInput) return;
    
    // Default filename
    let filename = filenameInput.value || 'input_code.py';
    
    // Check for shell script patterns
    if (content.includes('#!/bin/bash') || 
        content.includes('#!/bin/sh') ||
        (content.match(/\b(echo|export|source)\b/g) || []).length > 3) {
        
        if (!filename.endsWith('.sh')) {
            filename = filename.split('.')[0] + '.sh';
        }
    }
    // Check for Python patterns
    else if (content.includes('import ') || 
             content.includes('def ') || 
             content.includes('class ') ||
             content.includes('print(')) {
        
        if (!filename.endsWith('.py')) {
            filename = filename.split('.')[0] + '.py';
        }
    }
    
    filenameInput.value = filename;
}
