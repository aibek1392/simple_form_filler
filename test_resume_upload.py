#!/usr/bin/env python3
"""
Simple test script specifically for testing resume upload
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_resume_upload():
    """Test only the resume upload functionality"""
    print("🧪 Testing Resume Upload Only")
    print("=" * 40)
    
    # Check if resume file exists
    resume_path = os.path.join(os.getcwd(), "Taylor_Johnson_QA_Resume.pdf")
    print(f"📄 Resume file: {resume_path}")
    print(f"📁 File exists: {'✅ Yes' if os.path.exists(resume_path) else '❌ No'}")
    
    if not os.path.exists(resume_path):
        print("❌ Resume file not found. Please run 'python create_resume.py' first.")
        return
    
    # Start browser
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Browser started successfully")
        
        # Load the page
        url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
        print(f"🌐 Loading: {url}")
        driver.get(url)
        
        print("⏳ Waiting for page to load...")
        time.sleep(8)
        
        # Find resume upload field
        print("\n🔍 Looking for resume upload field...")
        
        # Try multiple selectors
        selectors_to_try = [
            ("ID", "_systemfield_resume"),
            ("CSS", "input[type='file']"),
            ("CSS", "input[id='_systemfield_resume']"),
            ("CSS", "input[accept*='pdf']"),
            ("XPATH", "//input[@type='file']")
        ]
        
        resume_element = None
        for selector_type, selector in selectors_to_try:
            try:
                print(f"   Trying {selector_type}: {selector}")
                if selector_type == "ID":
                    resume_element = driver.find_element(By.ID, selector)
                elif selector_type == "CSS":
                    resume_element = driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "XPATH":
                    resume_element = driver.find_element(By.XPATH, selector)
                
                if resume_element:
                    print(f"   ✅ Found with {selector_type}: {selector}")
                    print(f"   Element details:")
                    print(f"     - Tag: {resume_element.tag_name}")
                    print(f"     - Type: {resume_element.get_attribute('type')}")
                    print(f"     - ID: {resume_element.get_attribute('id')}")
                    print(f"     - Name: {resume_element.get_attribute('name')}")
                    print(f"     - Visible: {resume_element.is_displayed()}")
                    print(f"     - Enabled: {resume_element.is_enabled()}")
                    break
            except Exception as e:
                print(f"   ❌ Failed with {selector_type}: {e}")
                continue
        
        if not resume_element:
            print("❌ No resume upload field found!")
            input("Press Enter to close browser and check manually...")
            return False
        
        # Try to upload resume
        print(f"\n📤 Attempting to upload resume...")
        try:
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", resume_element)
            time.sleep(2)
            
            # Highlight the element for visual confirmation
            driver.execute_script("arguments[0].style.border='3px solid red'", resume_element)
            time.sleep(1)
            
            # Upload file
            resume_element.send_keys(resume_path)
            print(f"✅ Resume upload successful!")
            
            # Wait a moment for upload to process
            time.sleep(3)
            
            # Check if file name appears somewhere
            try:
                page_text = driver.page_source
                filename = os.path.basename(resume_path)
                if filename in page_text:
                    print(f"✅ Confirmed: {filename} appears on page")
                else:
                    print("⚠️  File name not visible on page (but upload may have worked)")
            except:
                pass
            
            print("\n🎯 SUCCESS: Resume upload completed!")
            print("👀 Please verify the upload worked in the browser window")
            input("Press Enter to close browser...")
            return True
            
        except Exception as upload_error:
            print(f"❌ Upload failed: {upload_error}")
            print("🔍 Let's check what happened...")
            input("Press Enter to close browser and debug...")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔒 Browser closed")

if __name__ == "__main__":
    test_resume_upload() 