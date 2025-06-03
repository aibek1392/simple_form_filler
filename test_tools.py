#!/usr/bin/env python3
"""
Test script for Job Application AI Tools

This script performs a quick test to ensure the tools are working correctly.
"""

import json
from job_application_tools import JobApplicationExtractor, JobApplicationFiller


def test_extraction():
    """Test the field extraction tool"""
    print("🧪 Testing Field Extraction Tool...")
    
    # Simple test URL (can be changed to any form)
    test_url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
    
    extractor = JobApplicationExtractor()
    try:
        # Quick test - just check if we can initialize and access the page
        extractor.setup_driver(headless=True)  # Use headless for testing
        extractor.driver.get(test_url)
        
        # Check if page loaded
        title = extractor.driver.title
        print(f"✅ Successfully loaded page: {title}")
        
        # Quick field detection test
        forms = extractor.driver.find_elements("tag name", "form")
        print(f"✅ Found {len(forms)} form(s) on the page")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        extractor.close()


def test_dummy_profile():
    """Test the dummy profile generation"""
    print("🧪 Testing Dummy Profile Generation...")
    
    try:
        filler = JobApplicationFiller()
        profile = filler.dummy_profile
        
        # Check if profile has required fields
        required_fields = ['full_name', 'email', 'phone', 'address']
        for field in required_fields:
            if field not in profile:
                print(f"❌ Missing field: {field}")
                return False
            print(f"✅ {field}: {profile[field]}")
        
        print("✅ Dummy profile generation working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Profile test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("🚀 Job Application AI Tools - Quick Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Field extraction basics
    if test_extraction():
        tests_passed += 1
    
    print("\n" + "-" * 30)
    
    # Test 2: Dummy profile generation
    if test_dummy_profile():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Tools are ready to use.")
        print("\n💡 Run 'python run_job_application_tools.py' to start the full demo")
    else:
        print("❌ Some tests failed. Please check your setup.")
    
    return tests_passed == total_tests


if __name__ == "__main__":
    main() 