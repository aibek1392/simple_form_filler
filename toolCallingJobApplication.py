from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent



#Create tool for that generates application info
@tool
def calculate_salary_range(url: str) -> dict:
    """Go to Ashby job posting via provided link, read the html adn return all required fields
    
    Args:
        url: Ashby Job posting URL
    
    Returns:
        Dictionary with all required info.
    """
    min_total = min_salary * (1 + bonus_percentage / 100)
    max_total = max_salary * (1 + bonus_percentage / 100)
    
    return {
        "base_range": f"${min_salary:,} - ${max_salary:,}",
        "total_comp_range": f"${min_total:,.0f} - ${max_total:,.0f}",
        "bonus_percentage": bonus_percentage
    }

## Create tool that uses the application info to fill out a job application