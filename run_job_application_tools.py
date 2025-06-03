#!/usr/bin/env python3
"""
Job Application AI Tools Runner

This script demonstrates the two AI agent tools:
1. JobApplicationExtractor - Extracts all required fields from job application forms
2. JobApplicationFiller - Fills out forms with dummy profile data

Usage:
    python run_job_application_tools.py
"""

import json
import sys
from job_application_tools import JobApplicationExtractor, JobApplicationFiller


def main():
    # The specific URL from the user's request
    url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
    
    print("🤖 Job Application AI Agents")
    print("=" * 50)
    print(f"Target URL: {url}")
    print("=" * 50)
    
    # Tool 1: Extract form fields
    print("\n🔍 TOOL 1: FIELD EXTRACTION")
    print("-" * 30)
    
    extractor = JobApplicationExtractor()
    try:
        print("Extracting form fields...")
        fields_data = extractor.extract_form_fields(url)
        
        if "error" in fields_data:
            print(f"❌ Error extracting fields: {fields_data['error']}")
            return
        
        print(f"✅ Successfully extracted {len(fields_data.get('fields', []))} fields")
        
        # Save extracted fields to file for reference
        with open('extracted_fields.json', 'w') as f:
            json.dump(fields_data, f, indent=2)
        print("📁 Saved field data to 'extracted_fields.json'")
        
    except Exception as e:
        print(f"❌ Error in field extraction: {str(e)}")
        return
    finally:
        extractor.close()
    
    # Ask user if they want to proceed with form filling
    print("\n" + "=" * 50)
    proceed = input("🚀 Proceed with form filling? (y/N): ").lower().strip()
    
    if proceed != 'y':
        print("👋 Stopping here. Field extraction complete.")
        return
    
    # Tool 2: Fill out the form
    print("\n📝 TOOL 2: FORM FILLING")
    print("-" * 30)
    
    filler = JobApplicationFiller()
    try:
        print("Filling out the form with dummy data...")
        print("⚠️  IMPORTANT: The form will NOT be submitted automatically!")
        
        results = filler.fill_application_form(fields_data, url)
        
        if results.get("success"):
            print(f"✅ Form filling completed!")
            print(f"📊 Filled {len(results.get('filled_fields', []))} fields")
            
            if results.get("errors"):
                print(f"⚠️  {len(results['errors'])} errors occurred")
                for error in results['errors'][:3]:  # Show first 3 errors
                    print(f"   - {error}")
            
            # Save results to file
            with open('form_filling_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print("📁 Saved results to 'form_filling_results.json'")
            
            print("\n" + "🎯" * 25)
            print("FORM IS READY FOR MANUAL REVIEW")
            print("- The browser will stay open for you to inspect")
            print("- Form is filled but NOT submitted")
            print("- Review the filled data before any submission")
            print("🎯" * 25)
            
            input("\nPress Enter to close the browser...")
            
        else:
            print(f"❌ Form filling failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error in form filling: {str(e)}")
    finally:
        filler.close()
    
    print("\n✨ AI Agents task completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1) 