"""
StrictCode - Complete Vulnerability Test Suite
Designed to trigger all rules: AST001-004, DEP001, SEC001-SEC007, SEC100.
"""

# [DEP001] HALLUCINATED IMPORT (CRITICAL)
# This package does not exist in your verified 5,000 package database.
import super_secure_ai_vault_v99


# [AST001] MISSING DOCSTRING (MEDIUM)
# [AST002] NO TRY-EXCEPT BLOCK (HIGH)
def unprotected_function(data):
    # [SEC001] AWS ACCESS KEY (CRITICAL)
    aws_key = "AKIAIOSFODNN7EXAMPLE"
    
    # [SEC003] GENERIC API KEY (CRITICAL)
    api_key = "AIzaSyD-ExampleKeyForGoogle-12345"
    
    # [SEC100] HIGH ENTROPY STRING (HIGH)
    # This random-looking string will trigger the Shannon Entropy check.
    random_token = "x8Kj2mN9pL4qR7sT1uW3yA5bC6dE0fG"
    
    return data.strip()


# [AST004] THE 'PASS' TRAP (CRITICAL)
def silent_failure_handler():
    """This function has a docstring but handles errors dangerously."""
    try:
        result = 10 / 0
    except Exception:
        # Silently swallowing errors is a critical hygiene failure.
        pass


# [AST003] CYCLOMATIC COMPLEXITY (HIGH)
# This function has 11 decision points, exceeding your threshold of 10.
def spaghetti_logic(val):
    """Complexity test function."""
    try:
        if val == 1:
            return "one"
        elif val == 2:
            return "two"
        elif val == 3:
            return "three"
        elif val == 4:
            return "four"
        elif val == 5:
            return "five"
        elif val == 6:
            return "six"
        elif val == 7:
            return "seven"
        elif val == 8:
            return "eight"
        elif val == 9:
            return "nine"
        elif val == 10:
            return "ten"
        else:
            return "unknown"
    except ValueError:
        return "error"

# [SEC007] GITHUB TOKEN (CRITICAL)
GITHUB_SECRET = "ghp_ExampleGitHubPersonalAccessToken123"
