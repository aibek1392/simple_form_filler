#!/usr/bin/env python3
"""
Job Application AI Agent Demo

This script demonstrates both AI agent tools:
1. JobApplicationExtractor - Successfully extracted 22 fields from the Wander job application
2. JobApplicationFiller - Fills out forms with intelligent dummy data

Run this to see a quick demo or to fill out the form with dummy data.
"""

import json
import sys
from job_application_tools import JobApplicationExtractor, JobApplicationFiller


def show_extraction_results():
    """Show the results of field extraction that was already performed"""
    print("🔍 AI AGENT TOOL 1: FIELD EXTRACTION RESULTS")
    print("=" * 60)
    
    try:
        with open('extracted_fields.json', 'r') as f:
            fields_data = json.load(f)
        
        print(f"✅ Successfully extracted from: {fields_data['url']}")
        print(f"📅 Extraction time: {fields_data['extracted_at']}")
        print(f"📊 Total fields found: {len(fields_data['fields'])}")
        
        print("\n📋 Field Summary:")
        field_types = {}
        required_count = 0
        
        for field in fields_data['fields']:
            field_type = field['type']
            if field_type in field_types:
                field_types[field_type] += 1
            else:
                field_types[field_type] = 1
                
            if field.get('required', False):
                required_count += 1
        
        for field_type, count in field_types.items():
            print(f"   • {field_type.title()} fields: {count}")
        
        print(f"   • Required fields: {required_count}")
        print(f"   • Optional fields: {len(fields_data['fields']) - required_count}")
        
        print("\n🎯 Key Fields Detected:")
        key_fields = ['Name', 'Email', 'Resume', 'Desired Annual Salary']
        for field in fields_data['fields'][:10]:  # Show first 10 fields
            label = field.get('label', 'No label')
            required = "✅ Required" if field.get('required') else "⚪ Optional"
            field_type = field.get('type', 'unknown')
            print(f"   • {label} ({field_type}) - {required}")
        
        if len(fields_data['fields']) > 10:
            print(f"   ... and {len(fields_data['fields']) - 10} more fields")
            
        return fields_data
        
    except FileNotFoundError:
        print("❌ No extraction results found. Run field extraction first.")
        return None
    except Exception as e:
        print(f"❌ Error reading extraction results: {str(e)}")
        return None


def demo_form_filling(fields_data):
    """Demonstrate the form filling AI agent"""
    print("\n📝 AI AGENT TOOL 2: INTELLIGENT FORM FILLING")
    print("=" * 60)
    
    print("This tool will:")
    print("✅ Fill out the form with realistic dummy data")
    print("✅ Use context-aware field matching")
    print("✅ Keep the browser visible (non-headless)")
    print("⚠️  NOT submit the form (safe operation)")
    
    proceed = input("\n🚀 Start form filling demo? (y/N): ").lower().strip()
    
    if proceed != 'y':
        print("👋 Demo cancelled. Form filling skipped.")
        return
    
    print("\n🤖 Starting AI Form Filler...")
    print("💡 The browser will open and you can watch the AI fill out the form!")
    
    filler = JobApplicationFiller()
    try:
        # Show the dummy profile that will be used
        print(f"\n👤 Using Dummy Profile:")
        profile = filler.dummy_profile
        print(f"   Name: {profile['full_name']}")
        print(f"   Email: {profile['email']}")
        print(f"   Phone: {profile['phone']}")
        print(f"   Location: {profile['city']}, {profile['state']}")
        print(f"   Experience: {profile['years_experience']} years")
        
        print("\n🌐 Opening browser and filling form...")
        results = filler.fill_application_form(fields_data)
        
        if results.get("success"):
            print(f"\n✅ Form filling completed successfully!")
            print(f"📊 Fields processed: {len(results.get('filled_fields', []))}")
            
            # Show some example filled fields
            print("\n📝 Example filled fields:")
            for field_result in results.get('filled_fields', [])[:5]:
                if field_result.get('filled'):
                    field_name = field_result.get('field', 'Unknown')
                    value = str(field_result.get('value', ''))
                    if len(value) > 50:
                        value = value[:47] + "..."
                    print(f"   ✅ {field_name}: {value}")
            
            if results.get('errors'):
                print(f"\n⚠️  Some errors occurred ({len(results['errors'])} total):")
                for error in results['errors'][:3]:
                    print(f"   • {error}")
            
            print("\n" + "🎯" * 30)
            print("🎯 FORM READY FOR MANUAL REVIEW 🎯")
            print("🎯" * 30)
            print("✅ Browser is open with filled form")
            print("✅ Form data is populated but NOT submitted")
            print("✅ You can review and modify before submission")
            print("⚠️  Remember: This is for testing purposes only")
            
            input("\n👀 Press Enter to close the browser after reviewing...")
            
        else:
            print(f"\n❌ Form filling failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Error during form filling: {str(e)}")
    finally:
        filler.close()
        print("🔒 Browser closed safely.")


def main():
    """Main demo function"""
    print("🤖 JOB APPLICATION AI AGENTS DEMO")
    print("🔗 Target: Wander QA Engineer Position")
    print("=" * 70)
    
    # Show extraction results
    fields_data = show_extraction_results()
    
    if not fields_data:
        print("\n❌ Cannot proceed without field extraction data.")
        print("💡 Run 'python job_application_tools.py' first to extract fields.")
        return
    
    # Offer form filling demo
    demo_form_filling(fields_data)
    
    print("\n✨ Demo completed successfully!")
    print("\n📚 What you've seen:")
    print("   🔍 AI extracted 22+ fields from a complex job application")
    print("   🤖 AI intelligently filled forms with contextual dummy data")
    print("   🛡️  Safety features prevent accidental form submission")
    print("   👁️  Non-headless mode allows human oversight")
    
    print("\n💼 Use Cases:")
    print("   • QA testing of job application forms")
    print("   • Form field analysis and documentation")
    print("   • Automated testing with dummy data")
    print("   • UI/UX testing and validation")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1) 