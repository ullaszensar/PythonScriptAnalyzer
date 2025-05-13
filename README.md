# PyTable Analyzer

A web application that analyzes Python and Shell scripts to identify PyTable tables and fields, organized by file and folder structure.

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

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pytable-analyzer.git
   cd pytable-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Choose one of the three analysis methods:
   - **Analyze Folder**: Enter a path to recursively scan for Python and Shell scripts
   - **Upload Files**: Select one or more files to upload and analyze
   - **Paste Code**: Input code directly into the text area

4. Click "Analyze Code" to process the files and view the results

5. Use the search functionality to filter tables and fields

6. Download the results as JSON for further processing

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.