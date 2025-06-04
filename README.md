# Job Application AI Agent

An intelligent AI-powered tool for automating job application form filling with contextual responses and resume upload capability.

## 🎯 **What It Does**

This AI agent automatically fills out the Wander QA Engineer job application with:
- ✅ **25 fields successfully filled** (including resume upload)
- 🤖 **Contextual responses** tailored to each question type  
- 📄 **Automatic resume upload** from PDF file
- 👁️ **Non-headless browser** so you can watch it work
- ⚠️ **Safe operation** - Never submits the form automatically

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Resume (Optional)
```bash
python create_resume.py
```
This creates `Taylor_Johnson_QA_Resume.pdf` for upload testing.

### 3. Run the AI Agent
```bash
python enhanced_form_filler.py
```

**That's it!** The AI will:
1. Open Chrome browser (visible)
2. Navigate to the Wander job application
3. Fill 25 fields with intelligent, contextual responses
4. Upload the resume automatically
5. Leave browser open for your review
6. **Never submit** the form (you control that)

## ✨ **Features**

### 🧠 **Intelligent Response Matching**
The AI provides different responses based on question context:

- **Travel questions** → Personal travel experiences  
- **Remote work questions** → Remote work expertise
- **Technical questions** → QA and testing knowledge
- **Career questions** → Professional development goals
- **Work style questions** → Productivity and collaboration preferences
- **Salary questions** → Appropriate compensation expectations

### 📄 **Resume Upload**
- Automatically detects hidden file upload fields
- Uploads PDF resume and confirms success
- Handles both visible and hidden file inputs

### 🛡️ **Safety Features**
- Browser runs in **visible mode** (non-headless)
- Form is **never submitted automatically**
- Detailed logging of all actions
- Error handling and graceful failures

## 📊 **Latest Results**

**Successful Test Run:**
- ✅ **25 out of 27 fields filled** (93% success rate)
- ✅ **Resume uploaded successfully** 
- ✅ **All questions answered contextually**
- ✅ **Zero form submissions** (safe operation)

**Fields Successfully Handled:**
- Name and contact information
- Online profiles (LinkedIn, GitHub, Portfolio)
- 20+ detailed questionnaire responses
- Resume file upload with confirmation
- Salary expectations
- Work preferences and availability

## 📁 **Project Structure**

```
├── enhanced_form_filler.py          # 🎯 Main AI agent (USE THIS)
├── create_resume.py                 # Resume PDF generator
├── test_resume_upload.py            # Resume upload testing utility
├── requirements.txt                 # Dependencies  
├── README.md                        # This documentation
├── Taylor_Johnson_QA_Resume.pdf     # Generated resume file
└── extracted_fields.json           # Form field analysis data
```

## 🔧 **How It Works**

### 1. **Context Analysis**
The AI analyzes each form field using:
- Field names and IDs
- Placeholder text
- Surrounding label text
- Parent element context

### 2. **Intelligent Matching**
Based on context analysis, it provides appropriate responses:

```python
# Example: Travel question detection
if "travel" in context:
    response = "I've traveled to over 15 countries and understand 
               the importance of reliable technology when away from home..."

# Example: Remote work question  
if "remote" in context:
    response = "I have 3 years of remote work experience and am 
               comfortable with distributed teams..."
```

### 3. **Resume Upload**
- Detects file input fields (even if hidden)
- Uploads PDF resume with full path
- Confirms upload success by checking page source

## 🎮 **Usage Examples**

### Basic Usage
```bash
python enhanced_form_filler.py
```

### Test Resume Upload Only
```bash
python test_resume_upload.py
```

### Generate New Resume
```bash
python create_resume.py
```

## ⚠️ **Important Notes**

- **FOR TESTING ONLY** - Always review filled data before any submission
- **Dummy Data** - Uses realistic but fake profile information
- **Manual Review Required** - Form stays open for your inspection
- **No Auto-Submit** - You have full control over form submission
- **Respectful Usage** - Only use for legitimate testing/demo purposes

## 🔧 **Customization**

### Update the Profile
Edit the `profile` dictionary in `enhanced_form_filler.py`:

```python
self.profile = {
    "full_name": "Your Name",
    "email": "your.email@example.com",
    "phone": "(555) 123-4567",
    # ... other fields
}
```

### Add New Response Types
Extend the `responses` dictionary for new question patterns:

```python
self.responses = {
    "new_topic": "Your response for this topic...",
    # ... other responses
}
```

## 🐛 **Troubleshooting**

### Resume Not Uploading?
```bash
python test_resume_upload.py  # Debug upload issues
python create_resume.py       # Regenerate resume file
```

### Browser Won't Start?
```bash
brew install chromedriver     # macOS
# or check Chrome/chromedriver compatibility
```

### Fields Not Filling?
- Check if page loaded completely (wait longer)
- Verify form structure hasn't changed
- Run with more verbose logging

## 📈 **Success Metrics**

- **Field Detection**: 27 fields found
- **Filling Success**: 25 fields completed (93%)
- **Resume Upload**: ✅ Working  
- **Context Matching**: ✅ Intelligent responses
- **Safety**: ✅ Zero auto-submissions

## 🎯 **Target Application**

Currently configured for:
**Wander QA Engineer Position**
```
https://jobs.ashbyhq.com/wander/121c24e0-eeff-49a8-ac56-793d2dbc9fcd/application
```

The URL can be modified in `enhanced_form_filler.py` if needed.

---

**⚡ Ready to use!** Run `python enhanced_form_filler.py` and watch the AI fill your job application intelligently.
