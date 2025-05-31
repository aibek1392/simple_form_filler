# Job Application AI Agents

Two AI-powered tools for automating job application form handling:

1. **JobApplicationExtractor** - Extracts all required fields from job application forms
2. **JobApplicationFiller** - Fills out forms with realistic dummy profile data

## Features

- 🔍 **Smart Field Detection**: Automatically identifies all form inputs, textareas, selects, and file uploads
- 🤖 **Intelligent Form Filling**: Context-aware field population with appropriate dummy data
- 👁️ **Non-Headless Mode**: Browser stays visible so you can see the process in action
- ⚠️ **Safe Operation**: Form is filled but **NEVER submitted automatically**
- 📊 **Detailed Reporting**: JSON output with extraction and filling results

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Tools

```bash
python run_job_application_tools.py
```

The script will:
1. Extract all form fields from the Wander job application
2. Ask if you want to proceed with form filling
3. Fill the form with dummy data (without submitting)
4. Keep the browser open for manual review

## Tool Details

### Tool 1: JobApplicationExtractor

Scans the job application page and extracts:
- Input fields (text, email, phone, etc.)
- Textarea fields
- Select dropdowns with options
- File upload fields
- Field labels and requirements
- Form metadata

**Output**: JSON file with complete form structure

### Tool 2: JobApplicationFiller

Uses the extracted field data to intelligently fill forms with:
- Realistic personal information
- Appropriate contact details
- Professional background data
- Context-appropriate responses

**Dummy Profile Includes**:
- Name, email, phone
- Address and location
- Professional links (LinkedIn, GitHub, portfolio)
- Work experience and education
- Cover letter and responses

## Safety Features

- ✅ Browser runs in **non-headless mode** (visible)
- ✅ Form is **never submitted automatically**
- ✅ Manual review required before any submission
- ✅ Detailed logging of all actions
- ✅ Error handling and graceful failures

## File Structure

```
├── job_application_tools.py      # Main AI agent classes
├── run_job_application_tools.py  # Runner script
├── requirements.txt              # Dependencies
├── README.md                     # This file
├── extracted_fields.json         # Generated: Field extraction results
└── form_filling_results.json     # Generated: Form filling results
```

## Usage Examples

### Standalone Usage

```python
from job_application_tools import JobApplicationExtractor, JobApplicationFiller

# Extract fields
extractor = JobApplicationExtractor()
fields = extractor.extract_form_fields(url)
extractor.close()

# Fill form
filler = JobApplicationFiller()
results = filler.fill_application_form(fields, url)
# Manual review required here - DO NOT SUBMIT
filler.close()
```

### Custom Dummy Profile

You can modify the `_generate_dummy_profile()` method in `JobApplicationFiller` to customize the dummy data used for form filling.

## Important Notes

⚠️ **NEVER SUBMIT FORMS AUTOMATICALLY** - This tool is for testing and development purposes only. Always review filled forms manually before any submission.

🔒 **Privacy**: Uses only dummy/fake data - no real personal information is used.

🌐 **Browser Compatibility**: Requires Chrome browser and chromedriver (automatically managed).

## Target URL

Currently configured for:
```
https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application
```

The URL can be modified in `run_job_application_tools.py` or passed as a parameter.

## Requirements

- Python 3.7+
- Chrome browser
- Internet connection
- Dependencies listed in `requirements.txt`

## Error Handling

The tools include comprehensive error handling for:
- Network timeouts
- Missing form elements  
- Browser automation failures
- Invalid field types
- Page loading issues

All errors are logged and reported in the output JSON files.

## Contributing

Feel free to extend the tools with additional field types, smarter form detection, or enhanced dummy data generation.

---

**Disclaimer**: This tool is for development and testing purposes only. Always respect website terms of service and never use for unauthorized automation. # AI_tool_to_fill_forms
