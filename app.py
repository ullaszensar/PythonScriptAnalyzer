import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
import tempfile
import json
from werkzeug.utils import secure_filename
from parser import analyze_file, PythonParser, ShellParser

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure upload settings
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'py', 'sh', 'bash'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    results = {}
    
    # Check if the post request has the file part
    if 'files[]' not in request.files:
        if 'source' in request.form and request.form['source'].strip():
            # Handle direct code input
            source_code = request.form['source']
            filename = request.form.get('filename', 'input_code.py')
            file_type = filename.split('.')[-1] if '.' in filename else 'py'
            
            results = {
                filename: analyze_file(filename, source_code, file_type)
            }
        else:
            flash('No files uploaded and no code entered', 'danger')
            return redirect(url_for('index'))
    else:
        files = request.files.getlist('files[]')
        
        # If user did not select files, browser submits empty files without filename
        if not files or files[0].filename == '':
            flash('No files selected', 'danger')
            return redirect(url_for('index'))
            
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                with open(filepath, 'r') as f:
                    content = f.read()
                
                file_type = filename.split('.')[-1]
                results[filename] = analyze_file(filename, content, file_type)
                
                # Clean up
                os.remove(filepath)
            else:
                flash(f'File {file.filename} is not a supported type', 'warning')
    
    # Store results in session for download later
    session['analysis_results'] = results
    
    return render_template('results.html', results=results)

@app.route('/download_results')
def download_results():
    if 'analysis_results' not in session:
        flash('No analysis results found', 'danger')
        return redirect(url_for('index'))
    
    # Create a temporary file to store the JSON results
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    with open(temp_file.name, 'w') as f:
        json.dump(session['analysis_results'], f, indent=2)
    
    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name='pytable_analysis.json',
        mimetype='application/json'
    )

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for analyzing code"""
    if request.json:
        content = request.json.get('content', '')
        filename = request.json.get('filename', 'input.py')
        file_type = filename.split('.')[-1] if '.' in filename else 'py'
        
        result = analyze_file(filename, content, file_type)
        return jsonify(result)
    else:
        return jsonify({'error': 'No content provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
