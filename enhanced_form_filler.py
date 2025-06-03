#!/usr/bin/env python3
"""
Enhanced Form Filler with Contextual Responses and Resume Upload
"""

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class EnhancedFormFiller:
    """Enhanced form filler with contextual responses and file upload"""
    
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
            "experience": "5"
        }
        
        # Enhanced contextual responses
        self.responses = {
            "cover_letter": """Dear Hiring Manager,

I am excited to apply for the QA Engineer position at Wander. With my 5 years of experience in quality assurance and passion for travel technology, I believe I would be a valuable addition to your team.

I am particularly drawn to Wander's mission of creating exceptional travel experiences through technology. My experience with automated testing, bug tracking, and cross-platform testing would help ensure your platform delivers the high-quality experience your customers expect.

Thank you for considering my application. I look forward to discussing how I can contribute to Wander's continued success.

Best regards,
Taylor Johnson""",
            
            "why_interested": "I'm passionate about travel technology and quality assurance. Wander's innovative approach to hospitality and their commitment to exceptional user experiences aligns perfectly with my career goals and values.",
            
            "experience": "I have 5 years of experience in quality assurance, specializing in automated testing frameworks, mobile app testing, and API testing. I've worked with tools like Selenium, Cypress, and Postman.",
            
            "strengths": "My key strengths include attention to detail, analytical thinking, and strong communication skills. I excel at identifying edge cases and collaborating with development teams to resolve issues efficiently.",
            
            "challenge": "In my previous role, I led the implementation of an automated testing pipeline that reduced regression testing time by 60% while improving test coverage. This required coordinating with multiple teams and learning new technologies quickly.",
            
            "motivation": "I'm motivated by the opportunity to ensure users have seamless, bug-free experiences with technology. There's great satisfaction in knowing that thorough testing prevents user frustration and protects company reputation.",
            
            "teamwork": "I believe in collaborative problem-solving and clear communication. I regularly participate in cross-functional meetings, provide detailed bug reports, and work closely with developers to understand root causes of issues.",
            
            "work_style": "I'm detail-oriented yet efficient, preferring to work systematically through test cases while staying adaptable to changing priorities. I value thorough documentation and believe in continuous learning.",
            
            "remote_experience": "I have 3 years of remote work experience and am comfortable with distributed teams. I'm proficient with collaboration tools like Slack, Zoom, and project management platforms.",
            
            "availability": "I can start within 2 weeks notice and am available for full-time employment. I'm flexible with working hours to accommodate team collaboration across time zones.",
            
            "questions": "I'm curious about Wander's quality assurance processes, the testing tools and frameworks currently in use, and opportunities for professional development in the QA team.",
            
            "travel": "I've traveled to over 15 countries and understand the importance of reliable technology when you're away from home. This personal experience fuels my passion for ensuring travel platforms work flawlessly.",
            
            "technology": "I'm comfortable with both manual and automated testing, experienced with various testing frameworks, and always eager to learn new tools and technologies to improve testing efficiency.",
            
            "career_goals": "I aim to grow into a senior QA role where I can mentor junior testers, contribute to testing strategy, and help build robust quality assurance processes that scale with company growth."
        }
        
        # Create resume file path
        self.resume_path = os.path.join(os.getcwd(), "Taylor_Johnson_QA_Resume.pdf")
    
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
        """Fill the Wander job application form with enhanced responses"""
        if not self.start_browser():
            return False
        
        try:
            url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
            print(f"🌐 Loading: {url}")
            
            self.driver.get(url)
            print("⏳ Waiting for page to load...")
            time.sleep(8)
            
            print("\n🤖 STARTING ENHANCED FORM FILLING")
            print("=" * 50)
            print(f"Name: {self.profile['full_name']}")
            print(f"Email: {self.profile['email']}")
            print(f"Resume: {'✅ Available' if os.path.exists(self.resume_path) else '❌ Missing'}")
            print("=" * 50)
            
            filled_count = 0
            
            # Find and fill all visible elements
            elements = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            print(f"📋 Found {len(elements)} form elements")
            
            for i, element in enumerate(elements, 1):
                try:
                    if not element.is_displayed() or not element.is_enabled():
                        continue
                    
                    tag = element.tag_name.lower()
                    input_type = element.get_attribute("type") or ""
                    name = element.get_attribute("name") or ""
                    placeholder = element.get_attribute("placeholder") or ""
                    
                    # Get surrounding text for better context
                    context = self._get_element_context(element)
                    
                    desc = f"{tag}"
                    if input_type: desc += f"[{input_type}]"
                    if name: desc += f" name='{name[:20]}...'" if len(name) > 20 else f" name='{name}'"
                    
                    print(f"\n🔄 {i}. Processing: {desc}")
                    if context:
                        print(f"   📝 Context: {context[:100]}..." if len(context) > 100 else f"   📝 Context: {context}")
                    
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(1)
                    
                    # Get appropriate value
                    value = self._get_contextual_value(tag, input_type, name, placeholder, context)
                    
                    if value:
                        if tag == "input":
                            if input_type == "file":
                                if os.path.exists(self.resume_path):
                                    element.send_keys(self.resume_path)
                                    print(f"   ✅ Uploaded resume: {os.path.basename(self.resume_path)}")
                                    filled_count += 1
                                else:
                                    print("   ⚠️  Resume file not found - skipped upload")
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
                                    selected_option = self._choose_select_option(options, name, placeholder, context)
                                    if selected_option:
                                        select.select_by_visible_text(selected_option)
                                        print(f"   ✅ Selected: {selected_option}")
                                        filled_count += 1
                            except Exception as e:
                                print(f"   ❌ Select error: {e}")
                        
                        time.sleep(1)
                    else:
                        print("   ⏭️  Skipped (no suitable value)")
                
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    continue
            
            print(f"\n🎉 ENHANCED FORM FILLING COMPLETED!")
            print(f"📊 Successfully filled {filled_count} fields")
            print("\n🎯 IMPORTANT:")
            print("- Form filled with contextual, varied responses")
            print("- Resume uploaded if PDF file exists")
            print("- Please review all fields before submitting")
            print("- DO NOT submit unless you intend to apply")
            
            print("\n👀 Browser will stay open for review...")
            input("Press Enter to close browser...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during form filling: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")
    
    def _get_element_context(self, element):
        """Get surrounding text context for better field understanding"""
        try:
            # Try to find associated label or nearby text
            parent = element.find_element(By.XPATH, "./..")
            context_text = parent.text.strip()
            
            # Clean up the context
            if context_text and len(context_text) < 500:
                return context_text
                
            # Try grandparent if parent text is too long or empty
            grandparent = parent.find_element(By.XPATH, "./..")
            context_text = grandparent.text.strip()
            
            if context_text and len(context_text) < 500:
                return context_text
                
        except:
            pass
        
        return ""
    
    def _get_contextual_value(self, tag, input_type, name, placeholder, context):
        """Get contextual value based on element characteristics and surrounding text"""
        # Combine all text sources for analysis
        all_text = f"{name} {placeholder} {context}".lower()
        
        # Email fields
        if input_type == "email" or "email" in all_text:
            return self.profile["email"]
        
        # Phone fields
        elif input_type == "tel" or any(word in all_text for word in ["phone", "tel", "mobile"]):
            return self.profile["phone"]
        
        # Name fields
        elif "name" in all_text:
            if "first" in all_text:
                return self.profile["first_name"]
            elif "last" in all_text:
                return self.profile["last_name"]
            else:
                return self.profile["full_name"]
        
        # URL fields
        elif input_type == "url" or any(word in all_text for word in ["linkedin", "github", "portfolio", "website"]):
            if "linkedin" in all_text:
                return self.profile["linkedin"]
            elif "github" in all_text:
                return self.profile["github"]
            else:
                return self.profile["portfolio"]
        
        # Salary fields
        elif any(word in all_text for word in ["salary", "compensation", "pay"]):
            return self.profile["salary"]
        
        # Experience fields
        elif any(word in all_text for word in ["experience", "years"]) and tag != "textarea":
            return self.profile["experience"]
        
        # Context-specific textarea responses
        elif tag == "textarea":
            return self._get_textarea_response(all_text)
        
        # Other text inputs - try to match context
        elif tag == "input" and input_type in ["text", ""]:
            return self._get_text_input_response(all_text)
        
        return None
    
    def _get_textarea_response(self, context):
        """Get appropriate response for textarea based on context"""
        context = context.lower()
        
        # Map context keywords to appropriate responses
        if any(word in context for word in ["cover", "letter", "introduction", "tell us about yourself"]):
            return self.responses["cover_letter"]
        elif any(word in context for word in ["why", "interested", "motivation", "attracted"]):
            return self.responses["why_interested"]
        elif any(word in context for word in ["experience", "background", "qualifications"]):
            return self.responses["experience"]
        elif any(word in context for word in ["strength", "skills", "abilities"]):
            return self.responses["strengths"]
        elif any(word in context for word in ["challenge", "difficult", "problem", "overcome"]):
            return self.responses["challenge"]
        elif any(word in context for word in ["team", "collaboration", "work with others"]):
            return self.responses["teamwork"]
        elif any(word in context for word in ["work style", "approach", "methodology"]):
            return self.responses["work_style"]
        elif any(word in context for word in ["remote", "distributed", "home", "virtual"]):
            return self.responses["remote_experience"]
        elif any(word in context for word in ["available", "start", "notice"]):
            return self.responses["availability"]
        elif any(word in context for word in ["question", "ask", "curious", "learn more"]):
            return self.responses["questions"]
        elif any(word in context for word in ["travel", "trip", "journey", "destination"]):
            return self.responses["travel"]
        elif any(word in context for word in ["technology", "tools", "software", "technical"]):
            return self.responses["technology"]
        elif any(word in context for word in ["career", "goal", "future", "growth"]):
            return self.responses["career_goals"]
        elif any(word in context for word in ["motivate", "drive", "inspire"]):
            return self.responses["motivation"]
        else:
            # Default to a shorter, more general response
            return "I am excited about this opportunity and believe my skills and experience make me a strong candidate for this position."
    
    def _get_text_input_response(self, context):
        """Get appropriate response for text inputs based on context"""
        # For short text inputs, usually want brief answers
        if any(word in context for word in ["salary", "compensation"]):
            return self.profile["salary"]
        elif any(word in context for word in ["experience", "years"]):
            return self.profile["experience"]
        else:
            return self.profile["full_name"]
    
    def _choose_select_option(self, options, name, placeholder, context):
        """Choose appropriate option from dropdown with context awareness"""
        all_text = f"{name} {placeholder} {context}".lower()
        
        # Remove empty and placeholder options
        valid_options = [opt for opt in options if opt and not any(word in opt.lower() for word in ["select", "choose", "please", "--"])]
        
        if not valid_options:
            return None
        
        # Context-based selection
        if any(word in all_text for word in ["experience", "years"]):
            for opt in valid_options:
                if any(exp in opt for exp in ["3-5", "4-6", "5+", "5-7"]):
                    return opt
        elif any(word in all_text for word in ["work", "employment", "type"]):
            for opt in valid_options:
                if "full" in opt.lower():
                    return opt
        elif any(word in all_text for word in ["eligible", "authorized"]):
            for opt in valid_options:
                if "yes" in opt.lower():
                    return opt
        
        return valid_options[0] if valid_options else None

def main():
    print("🚀 Enhanced Form Filler for Wander Job Application")
    print("=" * 55)
    print("Features:")
    print("• Contextual responses for different question types")
    print("• Resume upload capability")
    print("• Intelligent field matching")
    print("• Non-headless browser mode")
    print("\n⚠️  IMPORTANT: Review all data before submitting!")
    
    proceed = input("\n🤔 Continue? (y/N): ").lower().strip()
    if proceed != 'y':
        print("👋 Cancelled.")
        return
    
    filler = EnhancedFormFiller()
    success = filler.fill_wander_form()
    
    if success:
        print("\n✨ Enhanced form filling completed successfully!")
    else:
        print("\n❌ Form filling failed - check error messages above")

if __name__ == "__main__":
    main() 