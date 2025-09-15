#!/usr/bin/env python3
"""
Setup script for SAWA application
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/sawa_db

# OpenAI Configuration (optional - will use rule-based analysis if not provided)
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your actual configuration")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 SAWA Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Virtual environment creation"):
            sys.exit(1)
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Dependency installation"):
        print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Set up PostgreSQL database (optional - can use SQLite for testing)")
    print("3. Run the server: python run_server.py")
    print("4. Access documentation at: http://localhost:8000/docs")
    
    print("\n💡 Quick start (without database):")
    print("   python run_server.py")
    print("   # Then visit http://localhost:8000/docs")

if __name__ == "__main__":
    main()
