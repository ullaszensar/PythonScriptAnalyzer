import ast
import re
import os
import logging
from typing import Dict, List, Any, Optional, Tuple, Set

class TableField:
    """Represents a field in a PyTable table"""
    def __init__(self, name: str, field_type: Optional[str] = None, description: Optional[str] = None):
        self.name = name
        self.field_type = field_type
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.field_type,
            'description': self.description
        }

class Table:
    """Represents a PyTable table with its fields"""
    def __init__(self, name: str, variable_name: Optional[str] = None):
        self.name = name
        self.variable_name = variable_name
        self.fields: List[TableField] = []
        self.is_temp = False
    
    def add_field(self, field: TableField) -> None:
        self.fields.append(field)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'variable_name': self.variable_name,
            'is_temporary': self.is_temp,
            'fields': [field.to_dict() for field in self.fields]
        }

class BaseParser:
    """Base class for file parsers"""
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content
        self.tables: Dict[str, Table] = {}
    
    def parse(self) -> Dict[str, Any]:
        """Parse the file content to extract tables and fields"""
        raise NotImplementedError("Subclasses must implement parse method")
    
    def get_results(self) -> Dict[str, Any]:
        """Return the parsed results"""
        return {
            'filename': self.filename,
            'tables': {name: table.to_dict() for name, table in self.tables.items() if not table.is_temp}
        }

class PythonParser(BaseParser):
    """Parser for Python files to extract PyTable information"""
    
    def parse(self) -> Dict[str, Any]:
        try:
            # Parse the Python code into an AST
            tree = ast.parse(self.content)
            
            # Find PyTable imports
            pytable_imports = self._find_pytable_imports(tree)
            
            if not pytable_imports:
                return self.get_results()
            
            # Extract table definitions and usages
            self._extract_tables(tree, pytable_imports)
            
            # Extract fields from each table
            self._extract_fields(tree)
            
            return self.get_results()
        
        except SyntaxError as e:
            logging.error(f"Syntax error in {self.filename}: {str(e)}")
            return {
                'filename': self.filename,
                'error': f"Syntax error: {str(e)}",
                'tables': {}
            }
        except Exception as e:
            logging.error(f"Error parsing {self.filename}: {str(e)}")
            return {
                'filename': self.filename,
                'error': f"Error: {str(e)}",
                'tables': {}
            }
    
    def _find_pytable_imports(self, tree: ast.AST) -> Set[str]:
        """Find all PyTable-related imports in the code"""
        pytable_modules = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if 'tables' in name.name or 'pytables' in name.name:
                        asname = name.asname or name.name
                        pytable_modules.add(asname)
            
            elif isinstance(node, ast.ImportFrom):
                if 'tables' in node.module or 'pytables' in node.module:
                    for name in node.names:
                        asname = name.asname or name.name
                        pytable_modules.add(asname)
                        
        return pytable_modules
    
    def _extract_tables(self, tree: ast.AST, pytable_imports: Set[str]) -> None:
        """Extract table definitions from the AST"""
        for node in ast.walk(tree):
            # Look for class definitions inheriting from Table or similar
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id in ('Table', 'IsDescription'):
                        table = Table(node.name)
                        self.tables[node.name] = table
                        
            # Look for table creation using createTable
            elif isinstance(node, ast.Call):
                if self._is_create_table_call(node, pytable_imports):
                    table_name = self._extract_table_name_from_call(node)
                    if table_name:
                        # Check if this is a temporary table
                        is_temp = self._is_temp_table(node)
                        
                        # Find variable name if assignment exists
                        var_name = self._find_variable_name(node)
                        
                        table = Table(table_name, var_name)
                        table.is_temp = is_temp
                        self.tables[table_name] = table
            
            # Look for openTable calls
            elif isinstance(node, ast.Call):
                if self._is_open_table_call(node, pytable_imports):
                    table_name = self._extract_table_name_from_open(node)
                    if table_name:
                        var_name = self._find_variable_name(node)
                        if table_name not in self.tables:
                            table = Table(table_name, var_name)
                            self.tables[table_name] = table
    
    def _is_create_table_call(self, node: ast.Call, pytable_imports: Set[str]) -> bool:
        """Check if a node is a createTable call"""
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'createTable':
            return True
        return False
    
    def _is_open_table_call(self, node: ast.Call, pytable_imports: Set[str]) -> bool:
        """Check if a node is an openTable call"""
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'openTable':
            return True
        return False
    
    def _extract_table_name_from_call(self, node: ast.Call) -> Optional[str]:
        """Extract table name from a createTable call"""
        # Check for name parameter
        for kw in node.keywords:
            if kw.arg == 'name':
                if isinstance(kw.value, ast.Str):
                    return kw.value.s
        
        # Check positional arguments - table name is often the second argument
        if len(node.args) >= 2 and isinstance(node.args[1], ast.Str):
            return node.args[1].s
        
        return None
    
    def _extract_table_name_from_open(self, node: ast.Call) -> Optional[str]:
        """Extract table name from an openTable call"""
        # Check for name parameter
        for kw in node.keywords:
            if kw.arg == 'name':
                if isinstance(kw.value, ast.Str):
                    return kw.value.s
        
        # Check positional arguments
        if len(node.args) >= 1 and isinstance(node.args[0], ast.Str):
            return node.args[0].s
        
        return None
    
    def _is_temp_table(self, node: ast.Call) -> bool:
        """Check if a table is marked as temporary"""
        for kw in node.keywords:
            if kw.arg == 'expectedrows':
                return True  # Often temp tables specify expected rows
            if kw.arg == 'temp' and isinstance(kw.value, ast.NameConstant):
                return kw.value.value is True
        return False
    
    def _find_variable_name(self, node: ast.Call) -> Optional[str]:
        """Find the variable name if the call is part of an assignment"""
        for parent in ast.walk(ast.parse(self.content)):
            if isinstance(parent, ast.Assign) and isinstance(parent.value, ast.Call):
                if ast.dump(parent.value) == ast.dump(node) and len(parent.targets) > 0:
                    if isinstance(parent.targets[0], ast.Name):
                        return parent.targets[0].id
        return None
    
    def _extract_fields(self, tree: ast.AST) -> None:
        """Extract fields from each table definition"""
        # Find all classes that might define table fields
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if this class is a table description
                parent_table = self._get_parent_table(node)
                
                if parent_table and parent_table in self.tables:
                    # Extract fields from class body
                    for field_node in node.body:
                        if isinstance(field_node, ast.Assign):
                            field_name, field_type = self._extract_field_info(field_node)
                            if field_name:
                                field = TableField(field_name, field_type)
                                self.tables[parent_table].add_field(field)
    
    def _get_parent_table(self, class_node: ast.ClassDef) -> Optional[str]:
        """Determine if this class is a table description and return the table name"""
        for base in class_node.bases:
            if isinstance(base, ast.Name) and base.id == 'IsDescription':
                return None  # This is a base description, not a specific table
            
            # Check if the parent is in our tables
            if isinstance(base, ast.Name) and base.id in self.tables:
                return base.id
        
        # Check if this class itself is a table
        if class_node.name in self.tables:
            return class_node.name
        
        return None
    
    def _extract_field_info(self, assign_node: ast.Assign) -> Tuple[Optional[str], Optional[str]]:
        """Extract field name and type from an assignment node"""
        if len(assign_node.targets) == 1 and isinstance(assign_node.targets[0], ast.Name):
            field_name = assign_node.targets[0].id
            
            # Extract type information if available
            field_type = None
            if isinstance(assign_node.value, ast.Call):
                if isinstance(assign_node.value.func, ast.Name):
                    field_type = assign_node.value.func.id
            
            return field_name, field_type
        
        return None, None

class ShellParser(BaseParser):
    """Parser for Shell scripts to extract PyTable information"""
    
    def parse(self) -> Dict[str, Any]:
        """Parse shell scripts for PyTable usage"""
        try:
            # Look for Python code blocks or Python invocations
            python_blocks = self._extract_python_blocks()
            
            # Parse each Python block
            for block in python_blocks:
                parser = PythonParser(f"{self.filename}_block", block)
                result = parser.parse()
                
                # Merge the tables
                for table_name, table_data in result.get('tables', {}).items():
                    if table_name not in self.tables:
                        table = Table(table_name, table_data.get('variable_name'))
                        table.is_temp = table_data.get('is_temporary', False)
                        
                        # Add fields
                        for field_data in table_data.get('fields', []):
                            field = TableField(
                                field_data.get('name', ''),
                                field_data.get('type'),
                                field_data.get('description')
                            )
                            table.add_field(field)
                        
                        self.tables[table_name] = table
            
            return self.get_results()
        
        except Exception as e:
            logging.error(f"Error parsing shell script {self.filename}: {str(e)}")
            return {
                'filename': self.filename,
                'error': f"Error: {str(e)}",
                'tables': {}
            }
    
    def _extract_python_blocks(self) -> List[str]:
        """Extract Python code blocks from shell script"""
        python_blocks = []
        
        # Pattern for Python code in heredocs or similar
        python_pattern = r'(?:python\s+-c\s+["\'](.+?)["\'])|(?:<<\s*(?:EOF|PYTHON)\s*\n([\s\S]+?)\nEOF)'
        
        matches = re.finditer(python_pattern, self.content)
        for match in matches:
            if match.group(1):  # python -c '...'
                python_blocks.append(match.group(1))
            elif match.group(2):  # heredoc
                python_blocks.append(match.group(2))
        
        # Also look for Python files being executed
        python_file_pattern = r'python\s+([^\s>|&;]+\.py)'
        file_matches = re.finditer(python_file_pattern, self.content)
        
        # Just record the references, we can't parse the content without the file
        for match in file_matches:
            logging.info(f"Found reference to Python file: {match.group(1)}")
        
        return python_blocks

def analyze_file(filename: str, content: str, file_type: str) -> Dict[str, Any]:
    """Analyze a file to extract PyTable information"""
    if file_type in ('py', 'python'):
        parser = PythonParser(filename, content)
    elif file_type in ('sh', 'bash'):
        parser = ShellParser(filename, content)
    else:
        return {
            'filename': filename,
            'error': f"Unsupported file type: {file_type}",
            'tables': {}
        }
    
    return parser.parse()
