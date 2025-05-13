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

def scan_directory(directory_path):
    """Recursively scan directory for Python and Shell files"""
    results = {}
    
    try:
        # Check if directory exists
        if not os.path.isdir(directory_path):
            return {"error": f"Directory not found: {directory_path}"}, None
        
        file_count = 0
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if allowed_file(file):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, directory_path)
                    
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        file_type = file.split('.')[-1]
                        result = analyze_file(rel_path, content, file_type)
                        
                        # Store the folder path for organization
                        result['folder_path'] = os.path.dirname(rel_path)
                        results[rel_path] = result
                        file_count += 1
                    except Exception as e:
                        logging.error(f"Error processing file {file_path}: {str(e)}")
                        results[rel_path] = {
                            "filename": rel_path,
                            "error": f"Error reading file: {str(e)}",
                            "tables": {},
                            "folder_path": os.path.dirname(rel_path)
                        }
        
        return results, file_count
    except Exception as e:
        logging.error(f"Error scanning directory {directory_path}: {str(e)}")
        return {"error": f"Error scanning directory: {str(e)}"}, 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    results = {}
    
    # Handle folder path input (new option)
    if 'folder_path' in request.form and request.form['folder_path'].strip():
        folder_path = request.form['folder_path'].strip()
        results, file_count = scan_directory(folder_path)
        
        if isinstance(results, dict) and 'error' in results:
            flash(results['error'], 'danger')
            return redirect(url_for('index'))
        
        if file_count == 0:
            flash(f'No supported files found in directory: {folder_path}', 'warning')
            return redirect(url_for('index'))
        
        flash(f'Successfully scanned {file_count} files from directory', 'success')
    
    # Check if the post request has the file part
    elif 'files[]' not in request.files:
        if 'source' in request.form and request.form['source'].strip():
            # Handle direct code input
            source_code = request.form['source']
            filename = request.form.get('filename', 'input_code.py')
            file_type = filename.split('.')[-1] if '.' in filename else 'py'
            
            filename = filename or 'input_code.py'  # Ensure filename is not None
            result = analyze_file(filename, source_code, file_type)
            result['folder_path'] = ''  # No folder for direct input
            results = {
                filename: result
            }
        else:
            flash('No folder path provided, no files uploaded, and no code entered', 'danger')
            return redirect(url_for('index'))
    else:
        files = request.files.getlist('files[]')
        
        # If user did not select files, browser submits empty files without filename
        if not files or files[0].filename == '':
            flash('No files selected', 'danger')
            return redirect(url_for('index'))
            
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    file_type = filename.split('.')[-1]
                    result = analyze_file(filename, content, file_type)
                    result['folder_path'] = ''  # No folder for uploaded files
                    results[filename] = result
                except Exception as e:
                    logging.error(f"Error processing uploaded file {filename}: {str(e)}")
                    results[filename] = {
                        "filename": filename,
                        "error": f"Error reading file: {str(e)}",
                        "tables": {},
                        "folder_path": ""
                    }
                finally:
                    # Clean up
                    os.remove(filepath)
            else:
                flash(f'File {file.filename} is not a supported type', 'warning')
    
    # Store results in session for download later
    session['analysis_results'] = results
    
    # Group results by folder for the template
    folder_structure = {}
    if isinstance(results, dict):
        for filename, result in results.items():
            if isinstance(result, dict) and 'folder_path' in result:
                folder = result['folder_path']
            else:
                folder = ''
                
            if folder not in folder_structure:
                folder_structure[folder] = {}
            folder_structure[folder][filename] = result
    
    return render_template('results.html', results=results, folder_structure=folder_structure)

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
