#!/usr/bin/env python3
"""
Simple script to run the SAWA server with error handling
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_imports():
    """Check if all required imports work"""
    try:
        print("Checking imports...")
        
        # Test basic imports
        import fastapi
        print("✓ FastAPI imported successfully")
        
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
        
        import pydantic
        print("✓ Pydantic imported successfully")
        
        # Test app imports
        from app.main import app
        print("✓ SAWA app imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main function to run the server"""
    print("SAWA - Scientific Argumentative Writing Assistant")
    print("=" * 50)
    
    # Check imports first
    if not check_imports():
        print("\n❌ Import check failed. Please install dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n✅ All imports successful!")
    print("\nStarting SAWA server...")
    print("📖 Documentation will be available at: http://localhost:8000/docs")
    print("🔗 API root: http://localhost:8000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have installed all dependencies: pip install -r requirements.txt")
        print("2. Check if port 8000 is available")
        print("3. Verify your .env file configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()
