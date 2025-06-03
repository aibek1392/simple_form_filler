#!/usr/bin/env python3
"""
Create a sample PDF resume for testing form uploads
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def create_pdf_resume_reportlab():
    """Create PDF resume using reportlab"""
    doc = SimpleDocTemplate("Taylor_Johnson_QA_Resume.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30)
    story.append(Paragraph("Taylor Johnson", title_style))
    story.append(Paragraph("Quality Assurance Engineer", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    # Contact Info
    story.append(Paragraph("📧 taylor.johnson@example.com | 📞 (555) 123-4567", styles['Normal']))
    story.append(Paragraph("🔗 linkedin.com/in/taylorjohnson | 💻 github.com/taylorjohnson | 🌐 taylorjohnson.dev", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Professional Summary
    story.append(Paragraph("Professional Summary", styles['Heading2']))
    story.append(Paragraph("Dedicated Quality Assurance Engineer with 5 years of experience in automated testing, "
                          "manual testing, and quality assurance processes. Expertise in testing frameworks, "
                          "cross-platform testing, and ensuring exceptional user experiences in travel technology platforms.", 
                          styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Experience
    story.append(Paragraph("Experience", styles['Heading2']))
    story.append(Paragraph("<b>Senior QA Engineer</b> | TechTravel Inc. | 2021 - Present", styles['Normal']))
    story.append(Paragraph("• Led automated testing initiatives, reducing regression testing time by 60%", styles['Normal']))
    story.append(Paragraph("• Implemented comprehensive test suites for mobile and web applications", styles['Normal']))
    story.append(Paragraph("• Collaborated with cross-functional teams to ensure quality deliverables", styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>QA Engineer</b> | Digital Solutions LLC | 2019 - 2021", styles['Normal']))
    story.append(Paragraph("• Developed and maintained automated test scripts using Selenium and Cypress", styles['Normal']))
    story.append(Paragraph("• Performed API testing and database validation", styles['Normal']))
    story.append(Paragraph("• Created detailed test documentation and bug reports", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Skills
    story.append(Paragraph("Technical Skills", styles['Heading2']))
    story.append(Paragraph("• Testing Frameworks: Selenium, Cypress, Jest, PyTest", styles['Normal']))
    story.append(Paragraph("• Programming: Python, JavaScript, Java", styles['Normal']))
    story.append(Paragraph("• Tools: JIRA, TestRail, Postman, Git, Jenkins", styles['Normal']))
    story.append(Paragraph("• Platforms: Web, Mobile (iOS/Android), API Testing", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Education
    story.append(Paragraph("Education", styles['Heading2']))
    story.append(Paragraph("Bachelor of Science in Computer Science | University of Technology | 2019", styles['Normal']))
    
    doc.build(story)
    print("✅ PDF resume created: Taylor_Johnson_QA_Resume.pdf")

def create_text_resume():
    """Create a simple text resume if reportlab not available"""
    resume_content = """TAYLOR JOHNSON
Quality Assurance Engineer

Contact Information:
Email: taylor.johnson@example.com
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/taylorjohnson
GitHub: github.com/taylorjohnson
Portfolio: taylorjohnson.dev

PROFESSIONAL SUMMARY
Dedicated Quality Assurance Engineer with 5 years of experience in automated testing, 
manual testing, and quality assurance processes. Expertise in testing frameworks, 
cross-platform testing, and ensuring exceptional user experiences in travel technology platforms.

EXPERIENCE

Senior QA Engineer | TechTravel Inc. | 2021 - Present
• Led automated testing initiatives, reducing regression testing time by 60%
• Implemented comprehensive test suites for mobile and web applications
• Collaborated with cross-functional teams to ensure quality deliverables

QA Engineer | Digital Solutions LLC | 2019 - 2021
• Developed and maintained automated test scripts using Selenium and Cypress
• Performed API testing and database validation
• Created detailed test documentation and bug reports

TECHNICAL SKILLS
• Testing Frameworks: Selenium, Cypress, Jest, PyTest
• Programming: Python, JavaScript, Java
• Tools: JIRA, TestRail, Postman, Git, Jenkins
• Platforms: Web, Mobile (iOS/Android), API Testing

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2019

CERTIFICATIONS
• ISTQB Foundation Level Certified Tester
• Agile Testing Certification

PROJECTS
• Automated Testing Pipeline: Designed and implemented CI/CD testing pipeline
• Mobile App Testing Suite: Created comprehensive testing framework for travel app
• API Testing Framework: Built robust API testing solution using Python and Postman
"""
    
    with open("Taylor_Johnson_QA_Resume.txt", "w") as f:
        f.write(resume_content)
    print("✅ Text resume created: Taylor_Johnson_QA_Resume.txt")
    print("⚠️  Note: PDF version not available (reportlab not installed)")

def main():
    print("📄 Creating Sample Resume for Form Upload Testing")
    print("=" * 50)
    
    if REPORTLAB_AVAILABLE:
        try:
            create_pdf_resume_reportlab()
        except Exception as e:
            print(f"❌ Error creating PDF: {e}")
            create_text_resume()
    else:
        print("📦 Installing reportlab for PDF generation...")
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "reportlab"])
            print("✅ Reportlab installed! Please run this script again.")
        except:
            print("❌ Could not install reportlab automatically.")
            create_text_resume()

if __name__ == "__main__":
    main() 