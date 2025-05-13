# Installation Guide for PyTable Analyzer

This guide provides detailed instructions on how to set up and run the PyTable Analyzer application.

## System Requirements

- Python 3.6 or newer (Python 3.8+ recommended)
- pip (Python package installer)
- 50MB of disk space for the application and dependencies
- Internet connection for downloading dependencies

## Dependencies

The application requires the following main Python packages:
- Flask
- Werkzeug
- Flask-SQLAlchemy
- email-validator
- gunicorn (for production deployment)
- psycopg2-binary (optional, for PostgreSQL support)

## Step-by-Step Installation

### 1. Prepare Your Environment

#### For Windows:

1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Open Command Prompt and verify installation:
   ```
   python --version
   pip --version
   ```

#### For macOS:

1. Install Homebrew if not already installed:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```
   brew install python
   ```
3. Verify installation:
   ```
   python3 --version
   pip3 --version
   ```

#### For Linux (Ubuntu/Debian):

1. Update package list:
   ```
   sudo apt update
   ```
2. Install Python and pip:
   ```
   sudo apt install python3 python3-pip python3-venv
   ```
3. Verify installation:
   ```
   python3 --version
   pip3 --version
   ```

### 2. Get the Application

#### Option A: Clone with Git

```bash
git clone https://github.com/yourusername/pytable-analyzer.git
cd pytable-analyzer
```

#### Option B: Download Zip Archive

1. Download the ZIP file from the repository
2. Extract it to your preferred location
3. Open terminal/command prompt and navigate to the extracted folder

### 3. Create a Virtual Environment

Creating a virtual environment is recommended to avoid conflicts with other Python packages.

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### 4. Install Dependencies

With your virtual environment activated, install the required packages:

```bash
# Using pip
pip install Flask Werkzeug Flask-SQLAlchemy email-validator gunicorn psycopg2-binary

# Alternative: if a requirements.txt file exists
pip install -r requirements.txt
```

### 5. Configure the Application (Optional)

For security in production environments, set a session secret key:

#### Windows:

```bash
set SESSION_SECRET=your_secure_secret_key_here
```

#### macOS/Linux:

```bash
export SESSION_SECRET=your_secure_secret_key_here
```

### 6. Run the Application

#### For Development:

```bash
# Using Python directly
python main.py

# Or using Flask
flask run --host=0.0.0.0 --port=5000
```

#### For Production:

```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

### 7. Access the Application

Open your web browser and navigate to:
- Local access: `http://localhost:5000`
- Network access: `http://your_server_ip:5000`

## Troubleshooting

### Common Issues:

1. **Port already in use**:
   ```
   OSError: [Errno 98] Address already in use
   ```
   Solution: Change the port by setting it in the run command:
   ```bash
   flask run --port=5001
   ```

2. **Module not found errors**:
   ```
   ModuleNotFoundError: No module named 'flask'
   ```
   Solution: Ensure you've activated the virtual environment and installed all dependencies.

3. **Permission errors when scanning directories**:
   Solution: Make sure the application has read access to the directories you're trying to scan.

4. **Application errors or crashes**:
   For detailed error information, check the application logs in the terminal where the server is running.

## Upgrading

To update the application to the latest version:

### If installed from Git:

```bash
cd pytable-analyzer
git pull
pip install -r requirements.txt  # Install any new dependencies
```

### If installed from ZIP:

Download the latest version and repeat the installation steps.