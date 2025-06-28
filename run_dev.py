#!/usr/bin/env python3
"""
Development startup script for FastAPI User Management API
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main startup sequence"""
    print("=" * 60)
    print("FastAPI User Management API - Development Setup")
    print("=" * 60)
    
    # Check if virtual environment is recommended
    if not os.path.exists('.venv') and not os.environ.get('VIRTUAL_ENV'):
        print("\n⚠️  Recommendation: Create a virtual environment")
        print("Run these commands first:")
        print("  python -m venv .venv")
        print("  .venv\\Scripts\\activate  (Windows)")
        print("  source .venv/bin/activate  (Linux/Mac)")
        print()
    
    # Install dependencies
    if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
        print("Failed to install dependencies. Exiting.")
        return
    
    # Check if database exists
    if not os.path.exists("fastapi_app.db"):
        print("\n📁 Database not found. Setting up database...")
        
        # Run migrations
        if not run_command("alembic upgrade head", "Running database migrations"):
            print("Failed to run migrations. Exiting.")
            return
    else:
        print("\n📁 Database found. Checking for pending migrations...")
        run_command("alembic upgrade head", "Applying any pending migrations")
    
    print("\n" + "=" * 60)
    print("🚀 Starting FastAPI development server...")
    print("=" * 60)
    print()
    print("API will be available at:")
    print("  • Main API: http://localhost:8000")
    print("  • Interactive Docs: http://localhost:8000/docs")
    print("  • ReDoc: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Start the development server
    try:
        subprocess.run([
            "uvicorn", "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the project directory")
        print("2. Check that all dependencies are installed")
        print("3. Verify the app/main.py file exists")

if __name__ == "__main__":
    main() 