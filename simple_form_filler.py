#!/usr/bin/env python3
"""
Simple Form Filler - Uses system chromedriver for maximum compatibility
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SimpleFormFiller:
    """Simple, robust form filler"""
    
    def __init__(self):
        self.driver = None
        self.profile = {
            "full_name": "Taylor Johnson",
            "first_name": "Taylor", 
            "last_name": "Johnson",
            "email": "taylor.johnson@example.com",
            "phone": "(555) 123-4567",
            "linkedin": "https://linkedin.com/in/taylorjohnson",
            "github": "https://github.com/taylorjohnson",
            "portfolio": "https://taylorjohnson.dev",
            "salary": "$100k",
            "experience": "5",
            "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply for this QA Engineer position at Wander. With my 5 years of experience in quality assurance and passion for travel technology, I believe I would be a valuable addition to your team.\n\nI am particularly drawn to Wander's mission of creating exceptional travel experiences through technology. My experience with automated testing, bug tracking, and cross-platform testing would help ensure your platform delivers the high-quality experience your customers expect.\n\nThank you for considering my application. I look forward to discussing how I can contribute to Wander's continued success.\n\nBest regards,\nTaylor Johnson"
        }
    
    def start_browser(self):
        """Start Chrome browser with minimal options"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Browser started successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            return False
    
    def fill_wander_form(self):
        """Fill the Wander job application form"""
        if not self.start_browser():
            return False
        
        try:
            url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
            print(f"🌐 Loading: {url}")
            
            self.driver.get(url)
            print("⏳ Waiting for page to load...")
            time.sleep(8)  # Give ample time for page to load
            
            # Show user what we're about to do
            print("\n🤖 STARTING FORM FILLING")
            print("=" * 40)
            print(f"Name: {self.profile['full_name']}")
            print(f"Email: {self.profile['email']}")
            print(f"Phone: {self.profile['phone']}")
            print("=" * 40)
            
            filled_count = 0
            
            # Find and fill all visible input/textarea/select elements
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            print(f"📋 Found {len(elements)} form elements")
            
            for i, element in enumerate(elements, 1):
                try:
                    # Skip if element is not visible or interactable
                    if not element.is_displayed() or not element.is_enabled():
                        continue
                    
                    # Get element information
                    tag = element.tag_name.lower()
                    input_type = element.get_attribute("type") or ""
                    name = element.get_attribute("name") or ""
                    placeholder = element.get_attribute("placeholder") or ""
                    
                    # Create a description for logging
                    desc = f"{tag}"
                    if input_type: desc += f"[{input_type}]"
                    if name: desc += f" name='{name}'"
                    if placeholder: desc += f" placeholder='{placeholder}'"
                    
                    print(f"\n🔄 {i}. Processing: {desc}")
                    
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(1)
                    
                    # Determine what to fill based on element characteristics
                    value = self._get_value_for_element(tag, input_type, name, placeholder)
                    
                    if value:
                        if tag == "input":
                            if input_type == "file":
                                print("   ⏭️  Skipped file upload")
                            else:
                                element.clear()
                                element.send_keys(value)
                                print(f"   ✅ Filled: {value}")
                                filled_count += 1
                        
                        elif tag == "textarea":
                            element.clear()
                            element.send_keys(value)
                            print(f"   ✅ Filled textarea ({len(value)} chars)")
                            filled_count += 1
                        
                        elif tag == "select":
                            try:
                                select = Select(element)
                                options = [opt.text.strip() for opt in select.options if opt.text.strip()]
                                if len(options) > 1:
                                    # Try to find a good option or use the second one
                                    selected_option = self._choose_select_option(options, name, placeholder)
                                    if selected_option:
                                        select.select_by_visible_text(selected_option)
                                        print(f"   ✅ Selected: {selected_option}")
                                        filled_count += 1
                            except Exception as e:
                                print(f"   ❌ Select error: {e}")
                        
                        time.sleep(1)  # Pause between fields
                    else:
                        print("   ⏭️  Skipped (no suitable value)")
                
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    continue
            
            print(f"\n🎉 FORM FILLING COMPLETED!")
            print(f"📊 Successfully filled {filled_count} fields")
            print("\n🎯 IMPORTANT:")
            print("- Form is now filled with dummy data")
            print("- Please review all fields before submitting")
            print("- DO NOT submit unless you intend to apply")
            print("- This is for testing/demo purposes")
            
            print("\n👀 Browser will stay open for you to review...")
            input("Press Enter to close browser...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during form filling: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")
    
    def _get_value_for_element(self, tag, input_type, name, placeholder):
        """Get appropriate value for form element"""
        # Combine name and placeholder for analysis
        text = f"{name} {placeholder}".lower()
        
        # Email fields
        if input_type == "email" or "email" in text:
            return self.profile["email"]
        
        # Phone fields
        elif input_type == "tel" or any(word in text for word in ["phone", "tel", "mobile"]):
            return self.profile["phone"]
        
        # Name fields
        elif "name" in text:
            if "first" in text:
                return self.profile["first_name"]
            elif "last" in text:
                return self.profile["last_name"]
            else:
                return self.profile["full_name"]
        
        # URL fields
        elif input_type == "url" or any(word in text for word in ["linkedin", "github", "portfolio", "website"]):
            if "linkedin" in text:
                return self.profile["linkedin"]
            elif "github" in text:
                return self.profile["github"]
            else:
                return self.profile["portfolio"]
        
        # Salary fields
        elif any(word in text for word in ["salary", "compensation", "pay"]):
            return self.profile["salary"]
        
        # Experience fields
        elif any(word in text for word in ["experience", "years"]):
            return self.profile["experience"]
        
        # Text areas and other text inputs
        elif tag == "textarea" or input_type in ["text", ""]:
            if any(word in text for word in ["cover", "letter", "why", "motivation", "interest"]):
                return self.profile["cover_letter"]
            elif len(text) > 20:  # Likely a question that needs a longer answer
                return "I am excited about this opportunity and believe my skills and experience make me a strong candidate for this position."
            else:
                return self.profile["full_name"]
        
        return None
    
    def _choose_select_option(self, options, name, placeholder):
        """Choose appropriate option from dropdown"""
        text = f"{name} {placeholder}".lower()
        
        # Remove empty and placeholder options
        valid_options = [opt for opt in options if opt and not any(word in opt.lower() for word in ["select", "choose", "please", "--"])]
        
        if not valid_options:
            return None
        
        # Context-based selection
        if any(word in text for word in ["experience", "years"]):
            # Look for experience ranges
            for opt in valid_options:
                if any(exp in opt for exp in ["3-5", "4-6", "5+", "5-7"]):
                    return opt
        
        elif any(word in text for word in ["work", "employment", "type"]):
            # Look for full-time
            for opt in valid_options:
                if "full" in opt.lower():
                    return opt
        
        elif any(word in text for word in ["eligible", "authorized"]):
            # Look for yes
            for opt in valid_options:
                if "yes" in opt.lower():
                    return opt
        
        # Default: return first valid option
        return valid_options[0] if valid_options else None

def main():
    print("🚀 Simple Form Filler for Wander Job Application")
    print("=" * 50)
    print("This will fill out the Wander QA Engineer application")
    print("with dummy data for testing purposes.")
    print("\n⚠️  IMPORTANT: Review all data before submitting!")
    
    proceed = input("\n🤔 Continue? (y/N): ").lower().strip()
    if proceed != 'y':
        print("👋 Cancelled.")
        return
    
    filler = SimpleFormFiller()
    success = filler.fill_wander_form()
    
    if success:
        print("\n✨ Demo completed successfully!")
    else:
        print("\n❌ Demo failed - check error messages above")

if __name__ == "__main__":
    main() 