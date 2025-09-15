#!/usr/bin/env python3
"""
Test script for the simplified SAWA application
"""

import uvicorn
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Run the simplified SAWA application"""
    print("🚀 Starting SAWA Simple Test Server")
    print("=" * 40)
    print("📖 Documentation: http://localhost:8000/docs")
    print("🔗 API Root: http://localhost:8000")
    print("💡 This version works without a database")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)
    
    try:
        uvicorn.run(
            "app.main_simple:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have FastAPI installed:")
        print("pip install fastapi uvicorn")

if __name__ == "__main__":
    main()
