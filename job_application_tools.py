import json
import time
from typing import Dict, List, Any
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
from datetime import datetime, timedelta

# Auto-install chromedriver
try:
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()
except ImportError:
    print("Warning: chromedriver_autoinstaller not available. Make sure chromedriver is in PATH.")


class JobApplicationExtractor:
    """AI Agent Tool 1: Extract all required fields from job application forms"""
    
    def __init__(self):
        self.driver = None
        
    def setup_driver(self, headless=False):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if not headless:
            # Keep browser visible as requested
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.add_argument("--headless")
        
        # Improved Chrome options for better compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Set timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            return self.driver
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            # Fallback with minimal options
            minimal_options = Options()
            if not headless:
                minimal_options.add_argument("--start-maximized")
            minimal_options.add_argument("--no-sandbox")
            minimal_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=minimal_options)
            return self.driver
    
    def extract_form_fields(self, url: str) -> Dict[str, Any]:
        """
        Extract all required fields from the job application form
        
        Args:
            url: The job application URL
            
        Returns:
            Dictionary containing all found form fields with their properties
        """
        try:
            if not self.driver:
                self.setup_driver(headless=False)  # Keep visible as requested
            
            print(f"Loading job application form: {url}")
            self.driver.get(url)
            
            # Wait for page to load and look for various indicators
            print("Waiting for page to load...")
            try:
                # Try multiple strategies to wait for form content
                WebDriverWait(self.driver, 15).until(
                    lambda driver: (
                        driver.find_elements(By.TAG_NAME, "form") or
                        driver.find_elements(By.CSS_SELECTOR, "input, textarea, select") or
                        driver.find_elements(By.CSS_SELECTOR, "[role='form']") or
                        driver.find_elements(By.CSS_SELECTOR, ".form, .application-form")
                    )
                )
            except TimeoutException:
                print("No forms detected with standard selectors, checking for any input elements...")
            
            # Additional wait for dynamic content
            time.sleep(3)
            
            fields_info = {
                "url": url,
                "extracted_at": datetime.now().isoformat(),
                "fields": [],
                "form_metadata": {}
            }
            
            # Find all form elements (look both inside forms and globally)
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            if forms:
                print(f"Found {len(forms)} form(s)")
                for form_idx, form in enumerate(forms):
                    print(f"Analyzing form {form_idx + 1}")
                    self._extract_fields_from_container(form, fields_info)
            else:
                print("No form tags found, scanning entire page for input elements...")
                # Scan entire page for form elements
                self._extract_fields_from_container(self.driver, fields_info)
            
            # Extract additional metadata
            fields_info["form_metadata"] = self._extract_form_metadata()
            
            print(f"Extracted {len(fields_info['fields'])} fields from the form")
            return fields_info
            
        except Exception as e:
            print(f"Error extracting form fields: {str(e)}")
            return {"error": str(e), "fields": []}
    
    def _extract_fields_from_container(self, container, fields_info):
        """Extract fields from a container (form or entire page)"""
        # Extract input fields
        inputs = container.find_elements(By.TAG_NAME, "input")
        textareas = container.find_elements(By.TAG_NAME, "textarea")
        selects = container.find_elements(By.TAG_NAME, "select")
        
        # Process input fields
        for input_elem in inputs:
            field_info = self._extract_input_field_info(input_elem)
            if field_info:
                fields_info["fields"].append(field_info)
        
        # Process textarea fields
        for textarea in textareas:
            field_info = self._extract_textarea_field_info(textarea)
            if field_info:
                fields_info["fields"].append(field_info)
        
        # Process select fields
        for select in selects:
            field_info = self._extract_select_field_info(select)
            if field_info:
                fields_info["fields"].append(field_info)
        
        # Look for file upload fields specifically
        file_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='file']")
        for file_input in file_inputs:
            field_info = self._extract_file_field_info(file_input)
            if field_info:
                fields_info["fields"].append(field_info)
    
    def _extract_input_field_info(self, input_elem) -> Dict[str, Any]:
        """Extract information from input elements"""
        try:
            field_type = input_elem.get_attribute("type") or "text"
            name = input_elem.get_attribute("name")
            id_attr = input_elem.get_attribute("id")
            placeholder = input_elem.get_attribute("placeholder")
            required = input_elem.get_attribute("required") is not None
            
            # Get label text
            label_text = self._find_label_for_input(input_elem)
            
            if not name and not id_attr:
                return None
                
            return {
                "type": "input",
                "input_type": field_type,
                "name": name,
                "id": id_attr,
                "label": label_text,
                "placeholder": placeholder,
                "required": required,
                "selector": f"input[name='{name}']" if name else f"input[id='{id_attr}']"
            }
        except Exception as e:
            print(f"Error extracting input field: {e}")
            return None
    
    def _extract_textarea_field_info(self, textarea) -> Dict[str, Any]:
        """Extract information from textarea elements"""
        try:
            name = textarea.get_attribute("name")
            id_attr = textarea.get_attribute("id")
            placeholder = textarea.get_attribute("placeholder")
            required = textarea.get_attribute("required") is not None
            
            label_text = self._find_label_for_input(textarea)
            
            if not name and not id_attr:
                return None
                
            return {
                "type": "textarea",
                "name": name,
                "id": id_attr,
                "label": label_text,
                "placeholder": placeholder,
                "required": required,
                "selector": f"textarea[name='{name}']" if name else f"textarea[id='{id_attr}']"
            }
        except Exception as e:
            print(f"Error extracting textarea field: {e}")
            return None
    
    def _extract_select_field_info(self, select_elem) -> Dict[str, Any]:
        """Extract information from select elements"""
        try:
            name = select_elem.get_attribute("name")
            id_attr = select_elem.get_attribute("id")
            required = select_elem.get_attribute("required") is not None
            multiple = select_elem.get_attribute("multiple") is not None
            
            label_text = self._find_label_for_input(select_elem)
            
            # Get options
            options = []
            option_elements = select_elem.find_elements(By.TAG_NAME, "option")
            for option in option_elements:
                option_text = option.text.strip()
                option_value = option.get_attribute("value")
                if option_text:  # Skip empty options
                    options.append({"text": option_text, "value": option_value})
            
            if not name and not id_attr:
                return None
                
            return {
                "type": "select",
                "name": name,
                "id": id_attr,
                "label": label_text,
                "required": required,
                "multiple": multiple,
                "options": options,
                "selector": f"select[name='{name}']" if name else f"select[id='{id_attr}']"
            }
        except Exception as e:
            print(f"Error extracting select field: {e}")
            return None
    
    def _extract_file_field_info(self, file_input) -> Dict[str, Any]:
        """Extract information from file input elements"""
        try:
            name = file_input.get_attribute("name")
            id_attr = file_input.get_attribute("id")
            accept = file_input.get_attribute("accept")
            required = file_input.get_attribute("required") is not None
            
            label_text = self._find_label_for_input(file_input)
            
            if not name and not id_attr:
                return None
                
            return {
                "type": "file",
                "name": name,
                "id": id_attr,
                "label": label_text,
                "required": required,
                "accept": accept,
                "selector": f"input[type='file'][name='{name}']" if name else f"input[type='file'][id='{id_attr}']"
            }
        except Exception as e:
            print(f"Error extracting file field: {e}")
            return None
    
    def _find_label_for_input(self, input_elem) -> str:
        """Find associated label text for an input element"""
        try:
            # Try to find label by 'for' attribute
            id_attr = input_elem.get_attribute("id")
            if id_attr:
                try:
                    label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{id_attr}']")
                    return label.text.strip()
                except NoSuchElementException:
                    pass
            
            # Try to find parent label
            try:
                parent_label = input_elem.find_element(By.XPATH, "./ancestor::label[1]")
                return parent_label.text.strip()
            except NoSuchElementException:
                pass
            
            # Try to find nearby text/labels
            try:
                parent = input_elem.find_element(By.XPATH, "./..")
                text_content = parent.text.strip()
                if text_content and len(text_content) < 100:  # Reasonable label length
                    return text_content
            except:
                pass
            
            return ""
        except Exception:
            return ""
    
    def _extract_form_metadata(self) -> Dict[str, Any]:
        """Extract additional form metadata"""
        try:
            metadata = {
                "title": self.driver.title,
                "url": self.driver.current_url,
                "page_heading": ""
            }
            
            # Try to find main heading
            headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, .title, .heading")
            if headings:
                metadata["page_heading"] = headings[0].text.strip()
            
            return metadata
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


class JobApplicationFiller:
    """AI Agent Tool 2: Fill out job application forms with dummy data"""
    
    def __init__(self):
        self.driver = None
        self.dummy_profile = self._generate_dummy_profile()
    
    def setup_driver(self, headless=False):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        if not headless:
            # Keep browser visible as requested
            chrome_options.add_argument("--start-maximized")
        else:
            chrome_options.add_argument("--headless")
        
        # Improved Chrome options for better compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9223")  # Different port for filler
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Set timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            return self.driver
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            # Fallback with minimal options
            minimal_options = Options()
            if not headless:
                minimal_options.add_argument("--start-maximized")
            minimal_options.add_argument("--no-sandbox")
            minimal_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=minimal_options)
            return self.driver
    
    def _generate_dummy_profile(self) -> Dict[str, Any]:
        """Generate dummy profile data for form filling"""
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn"]
        last_names = ["Johnson", "Smith", "Williams", "Brown", "Davis", "Miller", "Wilson", "Garcia"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 9999)} Main Street",
            "city": random.choice(["San Francisco", "New York", "Los Angeles", "Chicago", "Austin", "Seattle"]),
            "state": random.choice(["CA", "NY", "TX", "IL", "WA"]),
            "zip_code": f"{random.randint(10000, 99999)}",
            "linkedin": f"https://linkedin.com/in/{first_name.lower()}{last_name.lower()}",
            "website": f"https://{first_name.lower()}{last_name.lower()}.dev",
            "github": f"https://github.com/{first_name.lower()}{last_name.lower()}",
            "cover_letter": f"Dear Hiring Manager,\n\nI am excited to apply for this position. With my background in software development and passion for innovation, I believe I would be a great fit for your team.\n\nBest regards,\n{first_name} {last_name}",
            "years_experience": str(random.randint(2, 8)),
            "salary_expectation": f"${random.randint(80, 150)}k",
            "availability": random.choice(["Immediately", "2 weeks notice", "1 month"]),
            "work_authorization": "Yes",
            "willing_to_relocate": random.choice(["Yes", "No"]),
            "education_level": random.choice(["Bachelor's Degree", "Master's Degree", "PhD"]),
            "university": random.choice(["Stanford University", "UC Berkeley", "MIT", "Harvard", "UCLA"]),
            "graduation_year": str(random.randint(2015, 2023))
        }
    
    def fill_application_form(self, fields_json: str, url: str = None) -> Dict[str, Any]:
        """
        Fill out job application form using provided field information
        
        Args:
            fields_json: JSON string containing field information from extractor
            url: Optional URL to navigate to (if different from fields data)
            
        Returns:
            Dictionary with results of the form filling operation
        """
        try:
            # Parse the fields data
            fields_data = json.loads(fields_json) if isinstance(fields_json, str) else fields_json
            
            if not self.driver:
                self.setup_driver(headless=False)  # Keep visible as requested
            
            # Navigate to URL
            target_url = url or fields_data.get("url")
            if target_url:
                print(f"Navigating to: {target_url}")
                try:
                    self.driver.get(target_url)
                    print("Page loaded, waiting for content...")
                    
                    # Wait for page to load with multiple strategies
                    try:
                        # Wait for any form elements to appear
                        WebDriverWait(self.driver, 15).until(
                            lambda driver: (
                                driver.find_elements(By.TAG_NAME, "form") or
                                driver.find_elements(By.CSS_SELECTOR, "input, textarea, select") or
                                driver.find_elements(By.CSS_SELECTOR, "[role='form']")
                            )
                        )
                        print("Form elements detected!")
                    except TimeoutException:
                        print("No forms detected immediately, but continuing...")
                    
                    # Additional wait for dynamic content
                    time.sleep(3)
                    
                except Exception as e:
                    print(f"Error loading page: {e}")
                    return {
                        "success": False,
                        "error": f"Failed to load page: {str(e)}",
                        "filled_fields": [],
                        "errors": [f"Page loading failed: {str(e)}"]
                    }
            
            results = {
                "success": True,
                "filled_fields": [],
                "errors": [],
                "dummy_profile_used": self.dummy_profile
            }
            
            print(f"Starting to process {len(fields_data.get('fields', []))} fields...")
            
            # Process each field
            for i, field in enumerate(fields_data.get("fields", []), 1):
                try:
                    print(f"Processing field {i}/{len(fields_data.get('fields', []))}: {field.get('label', 'Unknown')}")
                    field_result = self._fill_field(field)
                    results["filled_fields"].append(field_result)
                    
                    # Add small delay between fields
                    time.sleep(0.8)
                    
                except Exception as e:
                    error_msg = f"Error filling field {field.get('name', 'unknown')}: {str(e)}"
                    print(error_msg)
                    results["errors"].append(error_msg)
            
            successful_fills = len([f for f in results["filled_fields"] if f.get("filled")])
            print(f"Form filling completed. Filled {successful_fills} out of {len(results['filled_fields'])} fields.")
            print(f"Errors: {len(results['errors'])}")
            print("IMPORTANT: Form is ready for review. DO NOT SUBMIT - as requested.")
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filled_fields": [],
                "errors": [str(e)]
            }
    
    def _fill_field(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """Fill a single form field based on its type and properties"""
        field_type = field.get("type")
        selector = field.get("selector")
        
        result = {
            "field": field.get("name") or field.get("id"),
            "type": field_type,
            "filled": False,
            "value": None
        }
        
        try:
            # Find the element
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.3)
            
            if field_type == "input":
                result = self._fill_input_field(element, field, result)
            elif field_type == "textarea":
                result = self._fill_textarea_field(element, field, result)
            elif field_type == "select":
                result = self._fill_select_field(element, field, result)
            elif field_type == "file":
                result = self._fill_file_field(element, field, result)
            
        except TimeoutException:
            result["error"] = f"Element not found: {selector}"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _fill_input_field(self, element, field: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Fill input field based on its type and name"""
        input_type = field.get("input_type", "text")
        name = (field.get("name") or "").lower()
        label = (field.get("label") or "").lower()
        placeholder = (field.get("placeholder") or "").lower()
        
        # Determine appropriate value based on field characteristics
        value = self._get_input_value(input_type, name, label, placeholder)
        
        if value is not None:
            try:
                # Clear existing value
                element.clear()
                time.sleep(0.1)
                
                # Type the value
                element.send_keys(value)
                result["filled"] = True
                result["value"] = value
                
            except Exception as e:
                result["error"] = f"Failed to input value: {str(e)}"
        
        return result
    
    def _fill_textarea_field(self, element, field: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Fill textarea field"""
        name = (field.get("name") or "").lower()
        label = (field.get("label") or "").lower()
        
        # Determine appropriate text content
        if any(keyword in name + label for keyword in ["cover", "letter", "message", "why", "motivation"]):
            value = self.dummy_profile["cover_letter"]
        elif any(keyword in name + label for keyword in ["experience", "background", "about"]):
            value = f"I have {self.dummy_profile['years_experience']} years of experience in software development with expertise in various technologies and frameworks."
        else:
            value = "Thank you for considering my application. I look forward to discussing this opportunity with you."
        
        try:
            element.clear()
            time.sleep(0.1)
            element.send_keys(value)
            result["filled"] = True
            result["value"] = value
        except Exception as e:
            result["error"] = f"Failed to fill textarea: {str(e)}"
        
        return result
    
    def _fill_select_field(self, element, field: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Fill select field"""
        try:
            select = Select(element)
            options = field.get("options", [])
            
            if not options:
                return result
            
            name = (field.get("name") or "").lower()
            label = (field.get("label") or "").lower()
            
            # Choose appropriate option based on field context
            selected_option = self._choose_select_option(options, name, label)
            
            if selected_option:
                select.select_by_visible_text(selected_option["text"])
                result["filled"] = True
                result["value"] = selected_option["text"]
            
        except Exception as e:
            result["error"] = f"Failed to fill select: {str(e)}"
        
        return result
    
    def _fill_file_field(self, element, field: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file upload fields (skip actual file upload)"""
        # We skip file uploads as requested - just note that we found the field
        result["filled"] = False
        result["value"] = "FILE_UPLOAD_SKIPPED"
        result["note"] = "File upload field detected but skipped (no actual file uploaded)"
        return result
    
    def _get_input_value(self, input_type: str, name: str, label: str, placeholder: str) -> str:
        """Determine appropriate value for input field"""
        combined_text = f"{name} {label} {placeholder}".lower()
        
        if input_type == "email" or "email" in combined_text:
            return self.dummy_profile["email"]
        elif input_type == "tel" or any(keyword in combined_text for keyword in ["phone", "tel", "mobile"]):
            return self.dummy_profile["phone"]
        elif "first" in combined_text and "name" in combined_text:
            return self.dummy_profile["first_name"]
        elif "last" in combined_text and "name" in combined_text:
            return self.dummy_profile["last_name"]
        elif "name" in combined_text and not any(keyword in combined_text for keyword in ["user", "company", "file"]):
            return self.dummy_profile["full_name"]
        elif "address" in combined_text:
            return self.dummy_profile["address"]
        elif "city" in combined_text:
            return self.dummy_profile["city"]
        elif "state" in combined_text:
            return self.dummy_profile["state"]
        elif any(keyword in combined_text for keyword in ["zip", "postal"]):
            return self.dummy_profile["zip_code"]
        elif "linkedin" in combined_text:
            return self.dummy_profile["linkedin"]
        elif "website" in combined_text or "portfolio" in combined_text:
            return self.dummy_profile["website"]
        elif "github" in combined_text:
            return self.dummy_profile["github"]
        elif "salary" in combined_text:
            return self.dummy_profile["salary_expectation"]
        elif "experience" in combined_text and "year" in combined_text:
            return self.dummy_profile["years_experience"]
        elif "university" in combined_text or "school" in combined_text:
            return self.dummy_profile["university"]
        elif "graduation" in combined_text or "grad" in combined_text:
            return self.dummy_profile["graduation_year"]
        elif input_type == "url":
            return self.dummy_profile["website"]
        elif input_type == "number":
            return self.dummy_profile["years_experience"]
        elif input_type == "date":
            # Return a reasonable date
            return (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        else:
            # Default text value
            return self.dummy_profile["full_name"]
    
    def _choose_select_option(self, options: List[Dict], name: str, label: str) -> Dict[str, str]:
        """Choose appropriate option from select field"""
        combined_text = f"{name} {label}".lower()
        
        # Filter out empty or placeholder options
        valid_options = [opt for opt in options if opt.get("text") and opt["text"].strip() 
                        and not any(placeholder in opt["text"].lower() 
                                  for placeholder in ["select", "choose", "pick", "--", "please"])]
        
        if not valid_options:
            return None
        
        # Context-specific selections
        if "experience" in combined_text or "year" in combined_text:
            # Look for year ranges
            for opt in valid_options:
                if any(year in opt["text"] for year in ["3-5", "4-6", "5+"]):
                    return opt
        
        elif "education" in combined_text or "degree" in combined_text:
            # Look for degree options
            for opt in valid_options:
                if "bachelor" in opt["text"].lower() or "degree" in opt["text"].lower():
                    return opt
        
        elif "authorization" in combined_text or "eligible" in combined_text:
            # Look for positive authorization responses
            for opt in valid_options:
                if any(word in opt["text"].lower() for word in ["yes", "authorized", "eligible"]):
                    return opt
        
        elif "relocate" in combined_text:
            # Random yes/no for relocation
            yes_no_options = [opt for opt in valid_options if opt["text"].lower() in ["yes", "no"]]
            if yes_no_options:
                return random.choice(yes_no_options)
        
        # Default: choose first valid option
        return valid_options[0] if valid_options else None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


# Demo functions to test the tools
def demo_extract_fields(url: str):
    """Demo function to extract fields from a job application form"""
    extractor = JobApplicationExtractor()
    try:
        print("=== FIELD EXTRACTION DEMO ===")
        fields = extractor.extract_form_fields(url)
        print("\nExtracted Fields JSON:")
        print(json.dumps(fields, indent=2))
        return fields
    finally:
        extractor.close()


def demo_fill_form(fields_json, url: str = None):
    """Demo function to fill out a form with dummy data"""
    filler = JobApplicationFiller()
    try:
        print("\n=== FORM FILLING DEMO ===")
        results = filler.fill_application_form(fields_json, url)
        print("\nForm Filling Results:")
        print(json.dumps(results, indent=2))
        
        print("\n" + "="*50)
        print("FORM READY FOR REVIEW")
        print("IMPORTANT: DO NOT SUBMIT - Form is filled but not submitted as requested")
        print("You can now manually review the filled form in the browser")
        print("="*50)
        
        input("\nPress Enter to close the browser...")
        return results
    finally:
        filler.close()


if __name__ == "__main__":
    # Example usage
    url = "https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application"
    
    print("Job Application AI Tools Demo")
    print("=============================")
    
    # Tool 1: Extract fields
    fields = demo_extract_fields(url)
    
    if fields and "fields" in fields and len(fields["fields"]) > 0:
        # Tool 2: Fill form with dummy data
        demo_fill_form(fields, url)
    else:
        print("No fields were extracted. Please check the URL and try again.") 