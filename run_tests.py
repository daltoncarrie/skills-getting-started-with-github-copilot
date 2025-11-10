#!/usr/bin/env python3
"""
Test runner script for the Mergington High School Activities API.

This script provides an easy way to run tests with different options.
"""

import subprocess
import sys
import argparse


def run_tests(coverage=False, verbose=False, specific_test=None):
    """Run the test suite with specified options."""
    cmd = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])
    
    if specific_test:
        cmd.append(f"tests/{specific_test}")
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests for the Activities API")
    parser.add_argument("--coverage", "-c", action="store_true", 
                       help="Run tests with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Run tests in verbose mode")
    parser.add_argument("--test", "-t", type=str,
                       help="Run a specific test file (e.g., test_signup.py)")
    
    args = parser.parse_args()
    
    return run_tests(
        coverage=args.coverage,
        verbose=args.verbose, 
        specific_test=args.test
    )


if __name__ == "__main__":
    sys.exit(main())