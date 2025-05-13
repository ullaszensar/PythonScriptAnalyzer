# PyTable Analyzer | Zensar

A web application developed by Zensar Technologies that analyzes Python and Shell scripts to identify PyTable tables and fields, organized by file and folder structure.

## Features

- **Analyze Entire Folders**: Recursively scan directories for Python and Shell scripts
- **Upload Individual Files**: Analyze specific Python (.py) and Shell (.sh, .bash) files
- **Direct Code Input**: Paste code directly into the application for analysis
- **Folder Organization**: Results are organized by folder structure for better navigation
- **Search & Filter**: Search through tables and fields to find specific information
- **Download Results**: Export analysis results as JSON for further processing

## What It Analyzes

The PyTable Analyzer scans your code for:

- PyTable table definitions and declarations
- Table fields and their types
- Relationships between tables
- Temporary vs. persistent tables

## How It Works

The analyzer parses your code using Python's abstract syntax tree (AST) module and regular expressions to identify PyTable-specific patterns, including:

- Table definitions using `createTable` calls
- Field definitions in `IsDescription` subclasses
- Table references in code
- Table operations and queries

## Supported PyTable Patterns

```python
# Table creation
table = h5file.createTable(group, 'sensors', SensorDescription)

# Table definition
class SensorDescription(IsDescription):
    timestamp = Int64Col()
    value = FloatCol()
    location = StringCol(16)

# Table operations
for row in table.iterrows():
    print(row['value'])
```

## Requirements

- Python 3.6+
- Flask
- Additional dependencies in `pyproject.toml`

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Method 1: Using Git

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pytable-analyzer.git
   cd pytable-analyzer
   ```

2. Create a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -e .
   # Or if you prefer to use the requirements file
   pip install -r requirements.txt
   ```

### Method 2: Manual Download

1. Download the ZIP file of this project from GitHub
2. Extract the contents to a directory of your choice
3. Open a terminal/command prompt and navigate to that directory
4. Create a virtual environment and install dependencies as shown in steps 2-3 above

### Method 3: Using Docker (Optional)

If you prefer using Docker:

1. Build the Docker image:
   ```bash
   docker build -t pytable-analyzer .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 pytable-analyzer
   ```

### Configuration

1. (Optional) Set environment variables:
   ```bash
   # On Windows
   set SESSION_SECRET=your_secret_key

   # On macOS/Linux
   export SESSION_SECRET=your_secret_key
   ```

2. If no secret key is provided, a default development key will be used (not recommended for production)

## Usage

### Starting the Application

1. Start the application:
   ```bash
   # Make sure your virtual environment is activated
   python main.py
   
   # Alternatively, use Flask directly
   flask run --host=0.0.0.0 --port=5000
   
   # Or with gunicorn in production
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

2. Open your browser and go to `http://localhost:5000`

### Analyzing Code

3. Choose one of the three analysis methods:
   - **Analyze Folder**: Enter a path to recursively scan for Python and Shell scripts
     - Example: `/path/to/your/project`
     - The analyzer will walk through all subdirectories
     - Only `.py`, `.sh`, and `.bash` files will be analyzed
   
   - **Upload Files**: Select one or more files to upload and analyze
     - You can select multiple files by holding Ctrl/Cmd while selecting
     - Maximum upload size is 16MB total
   
   - **Paste Code**: Input code directly into the text area
     - Useful for quick analysis of code snippets
     - Enter a filename with appropriate extension (.py/.sh) to help with parsing

4. Configure analysis options:
   - Choose whether to exclude temporary tables
   - This helps focus on persistent data structures

5. Click "Analyze Code" to process the files and view the results

### Working with Results

6. View results organized by folder structure
   - Files are grouped by their directory
   - Tables are listed under each file
   - Fields are displayed in a table format

7. Use the search functionality to filter tables and fields
   - Search for specific table names or field types
   - Results update dynamically as you type

8. Download the results as JSON for further processing or integration with other tools

### Troubleshooting

- If you encounter permission errors when analyzing folders:
  - Ensure the application has read access to the specified directory
  - Try using absolute paths instead of relative paths
  
- For large codebases:
  - Consider analyzing specific subfolders rather than the entire project
  - Increase the timeout settings if needed

## About Zensar

Zensar is a leading digital solutions and technology services company that specializes in partnering with global organizations across industries on their Digital Transformation journey. A technology partner of choice, backed by strong track-record of innovation; credible investment in Digital solutions; assertion of commitment to client's success, Zensar's comprehensive range of digital and technology services and solutions enable its customers to achieve new thresholds of business performance.

## License

Proprietary - Copyright © 2025 Zensar Technologies. All rights reserved.

This software is the confidential and proprietary information of Zensar Technologies. You shall not disclose such confidential information and shall use it only in accordance with the terms of the license agreement you entered into with Zensar Technologies.