#!/usr/bin/env python3
"""
Alternative Form Filler using webdriver-manager for better compatibility
"""

import json
import time
from typing import Dict, List, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
from datetime import datetime, timedelta

# Use webdriver-manager for better driver management
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False
    print("webdriver-manager not available, falling back to system chromedriver")

class AlternativeFormFiller:
    """Alternative form filler with better driver management"""
    
    def __init__(self):
        self.driver = None
        self.dummy_profile = self._generate_dummy_profile()
    
    def setup_driver(self, headless=False):
        """Setup Chrome driver using webdriver-manager"""
        chrome_options = Options()
        
        if not headless:
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.add_argument("--headless")
        
        # Basic stable options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                # Use webdriver-manager for automatic driver management
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Fallback to system chromedriver
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(45)
            self.driver.implicitly_wait(15)
            return self.driver
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            raise
    
    def _generate_dummy_profile(self) -> Dict[str, Any]:
        """Generate dummy profile data"""
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley"]
        last_names = ["Johnson", "Smith", "Williams", "Brown", "Davis", "Miller"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "linkedin": f"https://linkedin.com/in/{first_name.lower()}{last_name.lower()}",
            "github": f"https://github.com/{first_name.lower()}{last_name.lower()}",
            "portfolio": f"https://{first_name.lower()}{last_name.lower()}.dev",
            "years_experience": str(random.randint(2, 8)),
            "salary_expectation": f"${random.randint(80, 150)}k",
            "cover_letter": f"Dear Hiring Manager,\n\nI am excited to apply for this position. With my background in quality assurance and passion for technology, I believe I would be a great fit for your team.\n\nBest regards,\n{first_name} {last_name}"
        }
    
    def fill_form(self, fields_data: Dict, url: str = None):
        """Fill form with simplified approach"""
        try:
            self.setup_driver(headless=False)
            
            target_url = url or fields_data.get("url")
            print(f"🌐 Navigating to: {target_url}")
            
            self.driver.get(target_url)
            print("⏳ Waiting for page to load...")
            time.sleep(5)  # Give page time to load
            
            # Find all fillable elements
            all_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            print(f"📋 Found {len(all_inputs)} total form elements")
            
            filled_count = 0
            
            for i, element in enumerate(all_inputs, 1):
                try:
                    # Skip hidden or disabled elements
                    if not element.is_displayed() or not element.is_enabled():
                        continue
                    
                    # Get element info
                    tag_name = element.tag_name.lower()
                    input_type = element.get_attribute("type") or "text"
                    name = element.get_attribute("name") or ""
                    placeholder = element.get_attribute("placeholder") or ""
                    
                    print(f"🔄 Processing element {i}: {tag_name} ({input_type}) - {name}")
                    
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                    
                    # Fill based on element type
                    if tag_name == "input":
                        if input_type in ["text", "email", "tel", "url"]:
                            value = self._get_input_value(input_type, name, placeholder)
                            if value:
                                element.clear()
                                element.send_keys(value)
                                filled_count += 1
                                print(f"  ✅ Filled: {value}")
                        elif input_type == "file":
                            print(f"  ⏭️  Skipped file upload: {name}")
                    
                    elif tag_name == "textarea":
                        element.clear()
                        element.send_keys(self.dummy_profile["cover_letter"])
                        filled_count += 1
                        print(f"  ✅ Filled textarea")
                    
                    elif tag_name == "select":
                        select = Select(element)
                        options = [opt.text for opt in select.options if opt.text.strip()]
                        if len(options) > 1:  # Skip if only placeholder option
                            select.select_by_index(1)  # Select second option
                            filled_count += 1
                            print(f"  ✅ Selected option: {select.first_selected_option.text}")
                    
                    time.sleep(0.5)  # Brief pause between fields
                    
                except Exception as e:
                    print(f"  ❌ Error with element {i}: {str(e)}")
                    continue
            
            print(f"\n🎉 Form filling completed!")
            print(f"📊 Successfully filled {filled_count} fields")
            print(f"🎯 Form is ready for manual review - DO NOT SUBMIT")
            
            # Keep browser open
            input("\n⏸️  Press Enter to close browser...")
            
        except Exception as e:
            print(f"❌ Error during form filling: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()
    
    def _get_input_value(self, input_type: str, name: str, placeholder: str) -> str:
        """Get appropriate value for input field"""
        combined = f"{name} {placeholder}".lower()
        
        if input_type == "email" or "email" in combined:
            return self.dummy_profile["email"]
        elif input_type == "tel" or "phone" in combined:
            return self.dummy_profile["phone"]
        elif "name" in combined:
            if "first" in combined:
                return self.dummy_profile["first_name"]
            elif "last" in combined:
                return self.dummy_profile["last_name"]
            else:
                return self.dummy_profile["full_name"]
        elif "linkedin" in combined:
            return self.dummy_profile["linkedin"]
        elif "github" in combined:
            return self.dummy_profile["github"]
        elif "portfolio" in combined or "website" in combined:
            return self.dummy_profile["portfolio"]
        elif "salary" in combined:
            return self.dummy_profile["salary_expectation"]
        elif "experience" in combined:
            return self.dummy_profile["years_experience"]
        else:
            return self.dummy_profile["full_name"]

def main():
    """Test the alternative form filler"""
    print("🚀 Alternative Form Filler Test")
    print("=" * 40)
    
    # Load extracted fields
    try:
        with open('extracted_fields.json', 'r') as f:
            fields_data = json.load(f)
        print(f"✅ Loaded field data with {len(fields_data.get('fields', []))} fields")
    except FileNotFoundError:
        print("❌ No extracted_fields.json found")
        return
    
    # Create and run filler
    filler = AlternativeFormFiller()
    filler.fill_form(fields_data)

if __name__ == "__main__":
    main() 