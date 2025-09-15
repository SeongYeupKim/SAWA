#!/usr/bin/env python3
"""
Test script for the SAWA system
"""

import uvicorn
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Run the SAWA test application"""
    print("🚀 Starting SAWA Test Server")
    print("=" * 50)
    print("📖 Documentation: http://localhost:8000/docs")
    print("🔗 API Root: http://localhost:8000")
    print("💡 This implements the exact CER + Toulmin framework from your PDF")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 SAWA server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have FastAPI installed:")
        print("pip install fastapi uvicorn")

if __name__ == "__main__":
    main()
