# database/__init__.py
"""Database package initialization"""

from .models import db, init_db, drop_db, reset_db
from .sample_data import create_sample_data

__all__ = ['db', 'init_db', 'drop_db', 'reset_db', 'create_sample_data']

# ============================================================================
# scripts/setup_database.py - Database Setup Script
# ============================================================================

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import Config

def check_postgresql_installed():
    """Check if PostgreSQL is installed and accessible"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL not installed or not in PATH")
        return False

def create_database_and_user():
    """Create the database and user for the application"""
    print("🔧 Setting up PostgreSQL database and user...")
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres',  # Connect to default database first
        'user': 'postgres',
        'password': input("Enter PostgreSQL admin password: ")
    }
    
    try:
        # Connect to PostgreSQL as admin
        conn = psycopg2.connect(**db_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user
        print("👤 Creating database user...")
        try:
            cursor.execute("CREATE USER sunx_user WITH PASSWORD 'sunx_password';")
            print("✅ User 'sunx_user' created successfully")
        except psycopg2.errors.DuplicateObject:
            print("ℹ️  User 'sunx_user' already exists")
        
        # Create database
        print("🗄️  Creating database...")
        try:
            cursor.execute("CREATE DATABASE sunx_mlm_db OWNER sunx_user;")
            print("✅ Database 'sunx_mlm_db' created successfully")
        except psycopg2.errors.DuplicateDatabase:
            print("ℹ️  Database 'sunx_mlm_db' already exists")
        
        # Grant privileges
        print("🔑 Granting privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE sunx_mlm_db TO sunx_user;")
        cursor.execute("ALTER USER sunx_user CREATEDB;")
        
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def test_connection():
    """Test connection to the application database"""
    print("🔍 Testing database connection...")
    
    try:
        # Parse the database URL
        db_url = Config.SQLALCHEMY_DATABASE_URI
        
        # Extract connection parameters
        import re
        match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_url)
        if not match:
            raise ValueError("Invalid database URL format")
        
        user, password, host, port, database = match.groups()
        
        # Test connection
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connection successful! PostgreSQL version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def main():
    """Main database setup function"""
    print("🚀 SUNX MLM Database Setup")
    print("=" * 40)
    
    # Step 1: Check PostgreSQL installation
    if not check_postgresql_installed():
        print("\n📥 Please install PostgreSQL first:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Or use: winget install PostgreSQL.PostgreSQL")
        return False
    
    # Step 2: Create database and user
    if not create_database_and_user():
        return False
    
    # Step 3: Test connection
    if not test_connection():
        return False
    
    print("\n🎉 Database setup completed successfully!")
    print("🔄 Next step: Run 'python main.py' to start the application")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

# ============================================================================
# scripts/install_dependencies.py - Dependency Installation Script
# ============================================================================

import subprocess
import sys
import os

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install dependencies from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please install Python 3.8 or higher")
        return False

def create_virtual_environment():
    """Create and activate virtual environment"""
    print("🌐 Setting up virtual environment...")
    
    try:
        # Create virtual environment
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        
        # Activation instructions
        if os.name == 'nt':  # Windows
            activate_script = "venv\\Scripts\\activate"
            print(f"✅ Virtual environment created!")
            print(f"💡 To activate: {activate_script}")
        else:  # Unix/Linux
            activate_script = "source venv/bin/activate"
            print(f"✅ Virtual environment created!")
            print(f"💡 To activate: {activate_script}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {str(e)}")
        return False

def main():
    """Main dependency setup function"""
    print("🔧 SUNX MLM Dependency Setup")
    print("=" * 35)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print("\n🎉 Dependencies setup completed!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

# ============================================================================
# scripts/create_executable.py - Windows Executable Creation Script
# ============================================================================

import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} is available")
        return True
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_executable():
    """Create Windows executable using PyInstaller"""
    print("🔨 Creating Windows executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "SUNX_MLM_Commission_Engine",
        "--onefile",
        "--windowed",
        "--add-data", "templates;templates",
        "--add-data", "static;static",
        "--hidden-import", "psycopg2",
        "--hidden-import", "flask",
        "--hidden-import", "sqlalchemy",
        "--icon", "static/icon.ico" if os.path.exists("static/icon.ico") else None,
        "main.py"
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable created successfully!")
        
        # Check if executable exists
        exe_path = Path("dist") / "SUNX_MLM_Commission_Engine.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable location: {exe_path}")
            print(f"📏 File size: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {str(e)}")
        return False

def create_installer_package():
    """Create a complete installer package"""
    print("📦 Creating installer package...")
    
    # Create package directory
    package_dir = Path("SUNX_MLM_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    try:
        # Copy executable
        exe_source = Path("dist") / "SUNX_MLM_Commission_Engine.exe"
        if exe_source.exists():
            shutil.copy2(exe_source, package_dir / "SUNX_MLM_Commission_Engine.exe")
        
        # Create installation script
        install_script = package_dir / "install.bat"
        with open(install_script, 'w') as f:
            f.write("""@echo off
echo SUNX MLM Commission Engine - Installation
echo ========================================
echo.
echo This will install the SUNX MLM Commission Engine on your system.
echo.
pause

REM Create application directory
if not exist "C:\\Program Files\\SUNX MLM" mkdir "C:\\Program Files\\SUNX MLM"

REM Copy executable
copy "SUNX_MLM_Commission_Engine.exe" "C:\\Program Files\\SUNX MLM\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\SUNX MLM Commission Engine.lnk'); $Shortcut.TargetPath = 'C:\\Program Files\\SUNX MLM\\SUNX_MLM_Commission_Engine.exe'; $Shortcut.Save()"

echo.
echo Installation completed successfully!
echo You can now run the application from your desktop or start menu.
echo.
pause
""")
        
        # Create README
        readme_file = package_dir / "README.txt"
        with open(readme_file, 'w') as f:
            f.write("""SUNX MLM Commission Engine
==========================

This package contains the SUNX MLM Commission Engine application.

SYSTEM REQUIREMENTS:
- Windows 10 or later
- PostgreSQL 12 or later
- 4GB RAM minimum
- 100MB free disk space

INSTALLATION:
1. Double-click install.bat to install the application
2. The application will be installed to C:\\Program Files\\SUNX MLM\\
3. A desktop shortcut will be created

FIRST RUN:
1. Make sure PostgreSQL is installed and running
2. Run the application from the desktop shortcut
3. The application will automatically open in your web browser
4. Use the demo data to explore the features

SUPPORT:
For technical support, please contact your implementation team.

Version: 1.0.0
Build Date: {build_date}
""".format(build_date=__import__('datetime').datetime.now().strftime('%Y-%m-%d')))
        
        print(f"✅ Package created: {package_dir}")
        print("📋 Package contents:")
        for item in package_dir.iterdir():
            print(f"   - {item.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating package: {str(e)}")
        return False

def main():
    """Main executable creation function"""
    print("🏗️  SUNX MLM Executable Builder")
    print("=" * 35)
    
    # Check PyInstaller
    if not check_pyinstaller():
        return False
    
    # Create executable
    if not create_executable():
        return False
    
    # Create installer package
    if not create_installer_package():
        return False
    
    print("\n🎉 Windows executable created successfully!")
    print("📦 Ready for deployment!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)