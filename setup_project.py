# setup_project.py - Complete Project Setup Script

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

def create_project_structure():
    """Create the complete project directory structure"""
    print("📁 Creating project structure...")
    
    directories = [
        "app",
        "app/database",
        "app/services", 
        "app/templates",
        "app/static",
        "app/static/css",
        "app/static/js",
        "app/static/images",
        "scripts",
        "tests",
        "docs",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    # Create __init__.py files
    init_files = [
        "app/__init__.py",
        "app/database/__init__.py", 
        "app/services/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"   ✅ Created: {init_file}")
    
    return True

def create_vscode_config():
    """Create VSCode configuration files"""
    print("⚙️  Creating VSCode configuration...")
    
    # Create .vscode directory
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    # settings.json
    settings = {
        "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["tests"],
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/venv": True,
            "**/node_modules": True
        },
        "sqltools.connections": [
            {
                "name": "SUNX MLM Database",
                "driver": "PostgreSQL",
                "previewLimit": 50,
                "server": "localhost",
                "port": 5432,
                "database": "sunx_mlm_db",
                "username": "sunx_user",
                "password": "sunx_password"
            }
        ]
    }
    
    with open(vscode_dir / "settings.json", 'w') as f:
        json.dump(settings, f, indent=4)
    
    # launch.json for debugging
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask App",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal",
                "env": {
                    "FLASK_ENV": "development",
                    "FLASK_DEBUG": "1"
                },
                "jinja": True
            },
            {
                "name": "Python: Current File",
                "type": "python", 
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            }
        ]
    }
    
    with open(vscode_dir / "launch.json", 'w') as f:
        json.dump(launch_config, f, indent=4)
    
    # tasks.json for build tasks
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Setup Database",
                "type": "shell",
                "command": "python",
                "args": ["scripts/setup_database.py"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Run Application",
                "type": "shell",
                "command": "python",
                "args": ["main.py"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Create Executable",
                "type": "shell",
                "command": "python",
                "args": ["scripts/create_executable.py"],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            },
            {
                "label": "Run Tests",
                "type": "shell",
                "command": "python",
                "args": ["-m", "pytest", "tests/"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared"
                }
            }
        ]
    }
    
    with open(vscode_dir / "tasks.json", 'w') as f:
        json.dump(tasks_config, f, indent=4)
    
    # extensions.json for recommended extensions
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.flake8",
            "ms-python.black-formatter",
            "mtxr.sqltools",
            "mtxr.sqltools-driver-pg",
            "ms-vscode.vscode-json",
            "bradlc.vscode-tailwindcss",
            "formulahendry.auto-rename-tag",
            "christian-kohler.path-intellisense"
        ]
    }
    
    with open(vscode_dir / "extensions.json", 'w') as f:
        json.dump(extensions, f, indent=4)
    
    print("   ✅ VSCode configuration created")
    return True

def create_project_files():
    """Create additional project files"""
    print("📄 Creating project files...")
    
    # README.md
    readme_content = """# SUNX MLM Commission Engine

A comprehensive Multi-Level Marketing commission calculation system built with Python, Flask, and PostgreSQL.

## 🚀 Quick Start

1. **Setup Environment:**
   ```bash
   python setup_project.py
   ```

2. **Install Dependencies:**
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Setup Database:**
   ```bash
   python scripts/setup_database.py
   ```

4. **Run Application:**
   ```bash
   python main.py
   ```

## 🎯 Features

- ✅ **Complete MLM Hierarchy Management**
- ✅ **Real-time Commission Calculations** (6 types)
- ✅ **PostgreSQL Database** with full audit trail
- ✅ **Interactive Web Interface** with live updates
- ✅ **Promotion Tracking** and eligibility monitoring
- ✅ **Windows Executable** generation
- ✅ **VSCode Integration** with debugging support

## 📊 Commission Types Implemented

1. **Outright Discount** - Product-based commission rates
2. **Group Override** - Silver/Gold/Diamond tiers for IBOs
3. **Lifetime Incentive** - 2% on qualifying IBO downlines
4. **BD Service Fee** - Tiered service fees for BDs
5. **BD Override** - 1% on qualifying BD downlines
6. **Promotion Tracking** - BP to IBO advancement

## 🏗️ Architecture

```
sunx-mlm-commission-engine/
├── app/
│   ├── database/          # SQLAlchemy models
│   ├── services/          # Business logic
│   ├── templates/         # HTML templates
│   └── static/           # CSS, JS, images
├── scripts/              # Setup and build scripts
├── tests/                # Unit tests
└── docs/                 # Documentation
```

## 🛠️ Development

### VSCode Tasks
- `Ctrl+Shift+P` → "Tasks: Run Task"
- **Setup Database** - Initialize PostgreSQL
- **Run Application** - Start development server
- **Create Executable** - Build Windows .exe
- **Run Tests** - Execute test suite

### Database Schema
- `organizations` - Company/organization data
- `resellers` - MLM participants with hierarchy
- `monthly_sales` - GPPIS tracking by month
- `commission_calculations` - Detailed commission records
- `commission_rules` - Configurable business rules

## 📦 Building Executable

```bash
python scripts/create_executable.py
```

Creates a standalone Windows executable in `dist/` folder.

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Support

For technical support and implementation questions, please contact the development team.
"""
    
    with open("README.md", 'w') as f:
        f.write(readme_content)
    
    # Create LICENSE file
    license_content = """MIT License

Copyright (c) 2024 SUNX MLM Commission Engine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open("LICENSE", 'w') as f:
        f.write(license_content)
    
    # Create .env.example
    env_example = """# SUNX MLM Commission Engine - Environment Variables

# Database Configuration
DATABASE_URL=postgresql://sunx_user:sunx_password@localhost:5432/sunx_mlm_db

# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Application Settings
LOG_LEVEL=INFO

# PostgreSQL Connection Details
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sunx_mlm_db
DB_USER=sunx_user
DB_PASSWORD=sunx_password
"""
    
    with open(".env.example", 'w') as f:
        f.write(env_example)
    
    # Create basic test file
    test_content = """# tests/test_commission_engine.py - Basic test example

import pytest
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

from services.commission_engine import CommissionEngine

class TestCommissionEngine:
    
    def setup_method(self):
        \"\"\"Setup test fixtures\"\"\"
        self.engine = CommissionEngine()
    
    def test_commission_engine_initialization(self):
        \"\"\"Test that commission engine initializes properly\"\"\"
        assert self.engine is not None
        assert hasattr(self.engine, 'rules')
        assert 'outright_discount' in self.engine.rules
    
    def test_outright_discount_rates(self):
        \"\"\"Test outright discount rate configuration\"\"\"
        rules = self.engine.rules['outright_discount']
        
        # Test SUNX-PREMIUM rates
        assert rules['SUNX-PREMIUM']['BP'] == 0.25
        assert rules['SUNX-PREMIUM']['IBO'] == 0.40
        assert rules['SUNX-PREMIUM']['BD'] == 0.40
        
        # Test SUNX-STANDARD rates
        assert rules['SUNX-STANDARD']['BP'] == 0.20
        assert rules['SUNX-STANDARD']['IBO'] == 0.35
        assert rules['SUNX-STANDARD']['BD'] == 0.35
    
    def test_active_thresholds(self):
        \"\"\"Test active status thresholds\"\"\"
        thresholds = self.engine.rules['active_thresholds']
        
        assert thresholds['BP'] == 2000
        assert thresholds['IBO'] == 2000
        assert thresholds['IBO_BD_CALC'] == 10000
        assert thresholds['BD'] == 10000
    
    def test_group_override_tiers(self):
        \"\"\"Test group override tier configuration\"\"\"
        override = self.engine.rules['group_override']
        
        # Silver tier
        assert override['silver']['min_active_bps'] == 3
        assert override['silver']['min_ggpis'] == 50000
        assert override['silver']['rate'] == 0.05
        
        # Gold tier
        assert override['gold']['min_active_bps'] == 5
        assert override['gold']['min_ggpis'] == 100000
        assert override['gold']['rate'] == 0.06
        
        # Diamond tier
        assert override['diamond']['min_active_bps'] == 8
        assert override['diamond']['min_ggpis'] == 180000
        assert override['diamond']['rate'] == 0.08

if __name__ == "__main__":
    pytest.main([__file__])
"""
    
    with open("tests/test_commission_engine.py", 'w') as f:
        f.write(test_content)
    
    print("   ✅ Project files created")
    return True

def create_batch_scripts():
    """Create Windows batch scripts for easy execution"""
    print("🔧 Creating batch scripts...")
    
    # Start application script
    start_script = """@echo off
title SUNX MLM Commission Engine

echo Starting SUNX MLM Commission Engine...
echo =====================================
echo.

REM Activate virtual environment
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
)

REM Start the application
echo Starting Flask application...
python main.py

pause
"""
    
    with open("start_app.bat", 'w') as f:
        f.write(start_script)
    
    # Setup script
    setup_script = """@echo off
title SUNX MLM Setup

echo SUNX MLM Commission Engine - Setup
echo ==================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv

echo Step 2: Activating virtual environment...
call venv\\Scripts\\activate.bat

echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Step 4: Setting up database...
python scripts\\setup_database.py

echo.
echo Setup completed successfully!
echo Run 'start_app.bat' to launch the application.
echo.
pause
"""
    
    with open("setup.bat", 'w') as f:
        f.write(setup_script)
    
    # Build executable script
    build_script = """@echo off
title SUNX MLM Build

echo SUNX MLM Commission Engine - Build Executable
echo ==============================================
echo.

REM Activate virtual environment
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
) else (
    echo Error: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

echo Building Windows executable...
python scripts\\create_executable.py

echo.
echo Build process completed!
echo Check the 'SUNX_MLM_Package' folder for the installer.
echo.
pause
"""
    
    with open("build.bat", 'w') as f:
        f.write(build_script)
    
    print("   ✅ Batch scripts created")
    return True

def create_documentation():
    """Create project documentation"""
    print("📚 Creating documentation...")
    
    docs_dir = Path("docs")
    
    # API documentation
    api_docs = """# SUNX MLM API Documentation

## Overview

The SUNX MLM Commission Engine provides a REST API for managing the MLM hierarchy and calculating commissions.

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Hierarchy Management

#### GET /api/hierarchy
Get the complete MLM hierarchy structure.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "full_name": "Maria Isabel Santos",
      "level": "BD",
      "children": [...]
    }
  ]
}
```

#### GET /api/reseller/{id}
Get detailed information for a specific reseller.

**Parameters:**
- `id` (integer): Reseller ID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "full_name": "Maria Isabel Santos",
    "level": "BD",
    "current_performance": {...},
    "sales_history": [...],
    "commission_history": [...]
  }
}
```

### Commission Calculations

#### GET /api/commissions/{reseller_id}/{month}
Calculate commissions for a specific reseller and month.

**Parameters:**
- `reseller_id` (integer): Reseller ID
- `month` (string): Month in YYYY-MM format

**Response:**
```json
{
  "success": true,
  "data": {
    "reseller_id": 1,
    "month": "2024-07",
    "gppis": 125000,
    "ggpis": 4500000,
    "commissions": [...],
    "total_commission": 45000
  }
}
```

### Sales Management

#### POST /api/sales/update
Update monthly sales for a reseller.

**Request Body:**
```json
{
  "reseller_id": 1,
  "month": "2024-07",
  "amount": 150000
}
```

**Response:**
```json
{
  "success": true,
  "data": {...},
  "message": "Sales updated successfully"
}
```

### Dashboard Statistics

#### GET /api/dashboard/stats/{month}
Get dashboard statistics for a specific month.

**Parameters:**
- `month` (string): Month in YYYY-MM format

**Response:**
```json
{
  "success": true,
  "data": {
    "total_sales": 500000,
    "total_resellers": 10,
    "active_counts": {
      "BP": 6,
      "IBO": 3,
      "BD": 1
    },
    "top_performers": [...]
  }
}
```

## Error Handling

All endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

## Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
"""
    
    with open(docs_dir / "api.md", 'w') as f:
        f.write(api_docs)
    
    # Database schema documentation
    schema_docs = """# Database Schema Documentation

## Overview

The SUNX MLM system uses PostgreSQL with the following main tables:

## Tables

### organizations
Stores company/organization information.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(200) | Organization name |
| organization_type | VARCHAR(50) | Type: corporate, individual, franchise |
| address | TEXT | Physical address |
| city | VARCHAR(100) | City |
| province | VARCHAR(100) | Province |
| phone | VARCHAR(50) | Contact phone |
| email | VARCHAR(120) | Contact email |
| territory | VARCHAR(100) | Sales territory |

### resellers
Stores MLM participant information and hierarchy.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| employee_code | VARCHAR(20) | Unique employee code |
| first_name | VARCHAR(100) | First name |
| last_name | VARCHAR(100) | Last name |
| level | VARCHAR(10) | MLM level: BP, IBO, BD |
| position | VARCHAR(100) | Job position |
| email | VARCHAR(120) | Email address |
| phone | VARCHAR(50) | Phone number |
| sponsor_id | INTEGER | Parent in hierarchy (FK) |
| organization_id | INTEGER | Organization (FK) |
| join_date | DATE | MLM join date |
| promotion_date | DATE | Last promotion date |
| active_status | BOOLEAN | Active status |
| territory | VARCHAR(100) | Sales territory |
| avatar_initials | VARCHAR(5) | Display initials |

### monthly_sales
Tracks monthly sales performance for each reseller.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| reseller_id | INTEGER | Reseller (FK) |
| month | VARCHAR(7) | Month (YYYY-MM) |
| gppis | DECIMAL(12,2) | Gross Personal Paid-In Sales |
| premium_sales | DECIMAL(12,2) | Premium product sales |
| standard_sales | DECIMAL(12,2) | Standard product sales |
| basic_sales | DECIMAL(12,2) | Basic product sales |

### commission_calculations
Stores detailed commission calculation records.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| reseller_id | INTEGER | Commission earner (FK) |
| source_reseller_id | INTEGER | Commission source (FK) |
| commission_type | VARCHAR(50) | Type of commission |
| month | VARCHAR(7) | Month (YYYY-MM) |
| base_amount | DECIMAL(12,2) | Base calculation amount |
| commission_rate | DECIMAL(5,4) | Rate as decimal |
| commission_amount | DECIMAL(12,2) | Final commission amount |
| tier_name | VARCHAR(50) | Tier name if applicable |
| notes | TEXT | Additional notes |

### commission_rules
Configurable business rules for commission calculations.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | Rule name |
| rule_type | VARCHAR(50) | Rule type |
| level | VARCHAR(10) | Applicable level |
| product_category | VARCHAR(50) | Product category |
| parameters | JSON | Rule parameters |
| active | BOOLEAN | Rule active status |
| effective_date | DATE | Effective date |

## Relationships

- `resellers.sponsor_id` → `resellers.id` (self-referencing hierarchy)
- `resellers.organization_id` → `organizations.id`
- `monthly_sales.reseller_id` → `resellers.id`
- `commission_calculations.reseller_id` → `resellers.id`
- `commission_calculations.source_reseller_id` → `resellers.id`

## Indexes

Key indexes for performance:
- `resellers.sponsor_id` - For hierarchy traversal
- `monthly_sales.reseller_id, month` - For sales lookups
- `commission_calculations.reseller_id, month` - For commission queries
"""
    
    with open(docs_dir / "database.md", 'w') as f:
        f.write(schema_docs)
    
    print("   ✅ Documentation created")
    return True

def main():
    """Main project setup function"""
    print("🚀 SUNX MLM Commission Engine - Project Setup")
    print("=" * 50)
    
    try:
        # Create project structure
        if not create_project_structure():
            return False
        
        # Create VSCode configuration
        if not create_vscode_config():
            return False
        
        # Create project files
        if not create_project_files():
            return False
        
        # Create batch scripts
        if not create_batch_scripts():
            return False
        
        # Create documentation
        if not create_documentation():
            return False
        
        print("\n🎉 Project setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Run: setup.bat (or python scripts/setup_database.py)")
        print("2. Run: start_app.bat (or python main.py)")
        print("3. Open VSCode and install recommended extensions")
        print("4. Create Git repository: git init && git add . && git commit -m 'Initial commit'")
        print("\n🚀 Ready for development!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)