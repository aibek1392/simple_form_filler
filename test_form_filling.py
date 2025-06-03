#!/usr/bin/env python3
"""
Test script specifically for form filling functionality
"""

import json
import time
from job_application_tools import JobApplicationFiller

def test_form_filling():
    """Test form filling with existing extracted data"""
    print("🧪 Testing Form Filling...")
    
    # Load the existing extracted fields
    try:
        with open('extracted_fields.json', 'r') as f:
            fields_data = json.load(f)
        print(f"✅ Loaded {len(fields_data.get('fields', []))} extracted fields")
    except FileNotFoundError:
        print("❌ No extracted_fields.json found. Run field extraction first.")
        return False
    
    # Test form filling
    filler = JobApplicationFiller()
    try:
        print("🤖 Initializing form filler...")
        print("🌐 This will open a browser window (non-headless mode)")
        
        # Test with better error handling
        results = filler.fill_application_form(fields_data)
        
        if results.get("success"):
            successful_fills = len([f for f in results.get("filled_fields", []) if f.get("filled")])
            total_fields = len(results.get("filled_fields", []))
            
            print(f"✅ Form filling completed!")
            print(f"📊 Successfully filled: {successful_fills}/{total_fields} fields")
            
            if results.get("errors"):
                print(f"⚠️  Errors encountered: {len(results['errors'])}")
                print("First few errors:")
                for i, error in enumerate(results['errors'][:3], 1):
                    print(f"   {i}. {error}")
            
            print("\n🎯 Form is now filled and ready for manual review!")
            print("⚠️  Remember: DO NOT submit the form - this is for testing only")
            
            return True
        else:
            print(f"❌ Form filling failed: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error during form filling test: {str(e)}")
        return False
    finally:
        # Keep browser open for manual inspection
        print("\n👀 Browser will stay open for manual inspection...")
        print("📝 You can review the filled form and then close the browser manually")
        
        # Don't auto-close the browser
        # filler.close()

def main():
    print("🚀 Form Filling Test Script")
    print("=" * 40)
    
    success = test_form_filling()
    
    if success:
        print("\n✨ Test completed successfully!")
        print("💡 The browser is left open for you to inspect the filled form")
    else:
        print("\n❌ Test failed - please check the error messages above")

if __name__ == "__main__":
    main() 