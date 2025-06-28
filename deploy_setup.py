#!/usr/bin/env python3
"""
Helper script to set up environment-specific Alembic configurations.
Usage:
    python deploy_setup.py --env production
    python deploy_setup.py --env staging
    python deploy_setup.py --env local
"""

import argparse
import shutil
import sys
from pathlib import Path


def create_env_config(environment: str) -> None:
    """Create environment-specific alembic configuration."""
    
    template_path = Path("config/alembic.ini.template")
    target_path = Path(f"alembic.{environment}.ini")
    
    if not template_path.exists():
        print(f"❌ Template file {template_path} not found!")
        sys.exit(1)
    
    if target_path.exists():
        response = input(f"⚠️  {target_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Copy template to environment-specific config
    shutil.copy2(template_path, target_path)
    
    # Customize based on environment
    with open(target_path, 'r') as f:
        content = f.read()
    
    if environment == "production":
        # More restrictive logging for production
        content = content.replace("level = WARNING", "level = ERROR")
        content = content.replace(
            "# For local development, use SQLite. For production, set DATABASE_URL environment variable",
            "# Production: DATABASE_URL environment variable is required\n# Example: postgresql://user:password@host:port/dbname"
        )
    elif environment == "staging":
        # Keep warning level for staging
        content = content.replace(
            "# For local development, use SQLite. For production, set DATABASE_URL environment variable",
            "# Staging: DATABASE_URL environment variable is required\n# Example: postgresql://user:password@staging-host:port/staging_db"
        )
    elif environment == "local":
        # Local development can keep SQLite
        pass
    
    with open(target_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created {target_path}")
    print(f"📝 Remember to set DATABASE_URL environment variable for {environment}")
    
    if environment in ["production", "staging"]:
        print(f"🔒 {target_path} is git-ignored for security")


def main():
    parser = argparse.ArgumentParser(description="Set up environment-specific Alembic configurations")
    parser.add_argument(
        "--env", 
        choices=["production", "staging", "local"], 
        required=True,
        help="Environment to create configuration for"
    )
    
    args = parser.parse_args()
    create_env_config(args.env)


if __name__ == "__main__":
    main() 