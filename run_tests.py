#!/usr/bin/env python3
"""
Test runner script for FastAPI User Management API.

This script provides convenient commands to run different categories of tests.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle the output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ pytest not found. Please install it with: pip install pytest")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test runner for FastAPI User Management API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --all              # Run all tests
  python run_tests.py --unit             # Run unit tests only
  python run_tests.py --api              # Run API tests only
  python run_tests.py --integration      # Run integration tests only
  python run_tests.py --coverage         # Run tests with coverage report
  python run_tests.py --quick            # Run a quick smoke test
  python run_tests.py --verbose          # Run all tests with verbose output
        """
    )
    
    # Test category options
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests (models, schemas, CRUD)')
    parser.add_argument('--api', action='store_true', help='Run API endpoint tests')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--quick', action='store_true', help='Run quick smoke test')
    parser.add_argument('--verbose', action='store_true', help='Run with verbose output')
    
    # Specific test options
    parser.add_argument('--file', type=str, help='Run tests from specific file')
    parser.add_argument('--test', type=str, help='Run specific test method')
    parser.add_argument('--pattern', type=str, help='Run tests matching pattern (-k option)')
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ['pytest']
    
    # Check if pytest is available
    try:
        subprocess.run(['pytest', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest not found. Installing test dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-dev.txt'], check=True)
            print("✅ Test dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install test dependencies. Please run: pip install -r requirements-dev.txt")
            return False
    
    success = True
    
    if args.quick:
        # Quick smoke test - just run a few basic tests
        cmd = base_cmd + [
            'tests/test_api_endpoints.py::TestRootEndpoints',
            'tests/test_schemas.py::TestUserSchemas::test_user_base_valid',
            '-v'
        ]
        success &= run_command(cmd, "Quick Smoke Test")
    
    elif args.unit:
        # Unit tests
        cmd = base_cmd + [
            'tests/test_models.py',
            'tests/test_schemas.py', 
            'tests/test_crud_operations.py',
            '-v'
        ]
        success &= run_command(cmd, "Unit Tests")
    
    elif args.api:
        # API tests
        cmd = base_cmd + [
            'tests/test_api_endpoints.py',
            '-v'
        ]
        success &= run_command(cmd, "API Endpoint Tests")
    
    elif args.integration:
        # Integration tests
        cmd = base_cmd + [
            'tests/test_integration.py',
            '-v'
        ]
        success &= run_command(cmd, "Integration Tests")
    
    elif args.coverage:
        # Coverage tests
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest-cov'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Installing pytest-cov for coverage reports...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest-cov'], check=False)
        
        cmd = base_cmd + [
            'tests/',
            '--cov=app',
            '--cov-report=html',
            '--cov-report=term-missing',
            '-v'
        ]
        success &= run_command(cmd, "Tests with Coverage")
        if success:
            print("\n📊 Coverage report generated in htmlcov/index.html")
    
    elif args.file:
        # Run specific file
        cmd = base_cmd + [f'tests/{args.file}', '-v']
        success &= run_command(cmd, f"Tests from {args.file}")
    
    elif args.test:
        # Run specific test
        cmd = base_cmd + [args.test, '-v']
        success &= run_command(cmd, f"Specific test: {args.test}")
    
    elif args.pattern:
        # Run tests matching pattern
        cmd = base_cmd + ['tests/', '-k', args.pattern, '-v']
        success &= run_command(cmd, f"Tests matching pattern: {args.pattern}")
    
    elif args.verbose:
        # All tests with verbose output
        cmd = base_cmd + ['tests/', '-v', '--tb=long']
        success &= run_command(cmd, "All Tests (Verbose)")
    
    elif args.all or len(sys.argv) == 1:
        # Default: run all tests
        cmd = base_cmd + ['tests/', '-v']
        success &= run_command(cmd, "All Tests")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        print("\nTest categories available:")
        print("  --quick        Quick smoke test")
        print("  --unit         Unit tests (models, schemas, CRUD)")
        print("  --api          API endpoint tests")
        print("  --integration  Integration workflow tests")
        print("  --coverage     Tests with coverage report")
        print("  --all          All tests (default)")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        print("\nFor more targeted testing, try:")
        print("  python run_tests.py --quick")
        print("  python run_tests.py --unit")
        print("  python run_tests.py --api")
    print(f"{'='*60}")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 