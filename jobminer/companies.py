"""Database of well-established companies matching the criteria."""
from typing import Dict, List

from jobminer.models import Company

# Curated list of well-established tech companies (200+ employees, 5+ years, stable growth)
ESTABLISHED_COMPANIES: List[Dict] = [
    # Major Tech Companies
    {"name": "Microsoft", "employee_count": 221000, "founded_year": 1975, "is_public": True, "industry": "Software"},
    {"name": "Amazon", "employee_count": 1540000, "founded_year": 1994, "is_public": True, "industry": "E-commerce/Cloud"},
    {"name": "Google", "employee_count": 190000, "founded_year": 1998, "is_public": True, "industry": "Technology"},
    {"name": "Meta", "employee_count": 86000, "founded_year": 2004, "is_public": True, "industry": "Social Media"},
    {"name": "Apple", "employee_count": 164000, "founded_year": 1976, "is_public": True, "industry": "Technology"},
    {"name": "Netflix", "employee_count": 13000, "founded_year": 1997, "is_public": True, "industry": "Streaming"},
    {"name": "Adobe", "employee_count": 29000, "founded_year": 1982, "is_public": True, "industry": "Software"},
    {"name": "Salesforce", "employee_count": 80000, "founded_year": 1999, "is_public": True, "industry": "CRM/Cloud"},
    {"name": "Oracle", "employee_count": 164000, "founded_year": 1977, "is_public": True, "industry": "Database/Cloud"},
    {"name": "IBM", "employee_count": 282000, "founded_year": 1911, "is_public": True, "industry": "Technology"},
    {"name": "Intel", "employee_count": 124800, "founded_year": 1968, "is_public": True, "industry": "Semiconductors"},
    {"name": "Cisco", "employee_count": 83000, "founded_year": 1984, "is_public": True, "industry": "Networking"},
    {"name": "VMware", "employee_count": 38000, "founded_year": 1998, "is_public": True, "industry": "Cloud/Virtualization"},
    {"name": "SAP", "employee_count": 112000, "founded_year": 1972, "is_public": True, "industry": "Enterprise Software"},

    # Cloud & Infrastructure
    {"name": "Snowflake", "employee_count": 6800, "founded_year": 2012, "is_public": True, "industry": "Data Cloud"},
    {"name": "Databricks", "employee_count": 5000, "founded_year": 2013, "is_public": False, "industry": "Data/AI"},
    {"name": "MongoDB", "employee_count": 4100, "founded_year": 2007, "is_public": True, "industry": "Database"},
    {"name": "Confluent", "employee_count": 3000, "founded_year": 2014, "is_public": True, "industry": "Data Streaming"},
    {"name": "HashiCorp", "employee_count": 2100, "founded_year": 2012, "is_public": True, "industry": "Cloud Infrastructure"},
    {"name": "GitLab", "employee_count": 2200, "founded_year": 2014, "is_public": True, "industry": "DevOps"},
    {"name": "Atlassian", "employee_count": 11000, "founded_year": 2002, "is_public": True, "industry": "Software"},
    {"name": "Elastic", "employee_count": 3500, "founded_year": 2012, "is_public": True, "industry": "Search/Analytics"},
    {"name": "Cloudflare", "employee_count": 3500, "founded_year": 2009, "is_public": True, "industry": "CDN/Security"},
    {"name": "Datadog", "employee_count": 6500, "founded_year": 2010, "is_public": True, "industry": "Monitoring"},

    # Financial Technology
    {"name": "Stripe", "employee_count": 8000, "founded_year": 2010, "is_public": False, "industry": "Payments"},
    {"name": "Square", "employee_count": 13000, "founded_year": 2009, "is_public": True, "industry": "FinTech"},
    {"name": "PayPal", "employee_count": 30000, "founded_year": 1998, "is_public": True, "industry": "Payments"},
    {"name": "Adyen", "employee_count": 3800, "founded_year": 2006, "is_public": True, "industry": "Payments"},
    {"name": "Plaid", "employee_count": 1000, "founded_year": 2013, "is_public": False, "industry": "FinTech"},

    # E-commerce & Marketplace
    {"name": "Shopify", "employee_count": 11600, "founded_year": 2006, "is_public": True, "industry": "E-commerce"},
    {"name": "eBay", "employee_count": 13200, "founded_year": 1995, "is_public": True, "industry": "E-commerce"},
    {"name": "Etsy", "employee_count": 2600, "founded_year": 2005, "is_public": True, "industry": "E-commerce"},
    {"name": "Wayfair", "employee_count": 16800, "founded_year": 2002, "is_public": True, "industry": "E-commerce"},

    # Cybersecurity
    {"name": "CrowdStrike", "employee_count": 8500, "founded_year": 2011, "is_public": True, "industry": "Cybersecurity"},
    {"name": "Palo Alto Networks", "employee_count": 13800, "founded_year": 2005, "is_public": True, "industry": "Cybersecurity"},
    {"name": "Okta", "employee_count": 6000, "founded_year": 2009, "is_public": True, "industry": "Identity/Security"},
    {"name": "Zscaler", "employee_count": 6500, "founded_year": 2007, "is_public": True, "industry": "Cloud Security"},
    {"name": "Fortinet", "employee_count": 11000, "founded_year": 2000, "is_public": True, "industry": "Cybersecurity"},

    # Communication & Collaboration
    {"name": "Slack", "employee_count": 3000, "founded_year": 2009, "is_public": False, "industry": "Collaboration"},
    {"name": "Zoom", "employee_count": 8400, "founded_year": 2011, "is_public": True, "industry": "Video Conferencing"},
    {"name": "Twilio", "employee_count": 9000, "founded_year": 2008, "is_public": True, "industry": "Communications API"},
    {"name": "DocuSign", "employee_count": 7500, "founded_year": 2003, "is_public": True, "industry": "Document Management"},

    # SaaS & Business Software
    {"name": "ServiceNow", "employee_count": 22000, "founded_year": 2003, "is_public": True, "industry": "Enterprise SaaS"},
    {"name": "Workday", "employee_count": 18000, "founded_year": 2005, "is_public": True, "industry": "HR/Finance SaaS"},
    {"name": "HubSpot", "employee_count": 7900, "founded_year": 2006, "is_public": True, "industry": "Marketing Software"},
    {"name": "Zendesk", "employee_count": 6000, "founded_year": 2007, "is_public": True, "industry": "Customer Service"},
    {"name": "Splunk", "employee_count": 7500, "founded_year": 2003, "is_public": True, "industry": "Data Analytics"},
    {"name": "Tableau", "employee_count": 5000, "founded_year": 2003, "is_public": False, "industry": "Analytics"},
    {"name": "Asana", "employee_count": 1600, "founded_year": 2008, "is_public": True, "industry": "Project Management"},

    # Ride-sharing & Transportation
    {"name": "Uber", "employee_count": 32800, "founded_year": 2009, "is_public": True, "industry": "Transportation"},
    {"name": "Lyft", "employee_count": 4000, "founded_year": 2012, "is_public": True, "industry": "Transportation"},

    # Gaming
    {"name": "Roblox", "employee_count": 2400, "founded_year": 2004, "is_public": True, "industry": "Gaming"},
    {"name": "Unity", "employee_count": 7700, "founded_year": 2004, "is_public": True, "industry": "Gaming Engine"},

    # AI & Machine Learning
    {"name": "Scale AI", "employee_count": 800, "founded_year": 2016, "is_public": False, "industry": "AI/ML"},
    {"name": "DataRobot", "employee_count": 1000, "founded_year": 2012, "is_public": False, "industry": "AI/ML"},

    # Traditional Companies with Strong Tech Divisions
    {"name": "Capital One", "employee_count": 55000, "founded_year": 1994, "is_public": True, "industry": "Financial Services"},
    {"name": "JPMorgan Chase", "employee_count": 293000, "founded_year": 1799, "is_public": True, "industry": "Financial Services"},
    {"name": "Goldman Sachs", "employee_count": 45000, "founded_year": 1869, "is_public": True, "industry": "Financial Services"},
    {"name": "Bloomberg", "employee_count": 20000, "founded_year": 1981, "is_public": False, "industry": "Financial Data"},
    {"name": "Visa", "employee_count": 26500, "founded_year": 1958, "is_public": True, "industry": "Payments"},
    {"name": "Mastercard", "employee_count": 24000, "founded_year": 1966, "is_public": True, "industry": "Payments"},

    # European Tech Companies
    {"name": "Spotify", "employee_count": 9800, "founded_year": 2006, "is_public": True, "industry": "Music Streaming"},
    {"name": "Booking.com", "employee_count": 23000, "founded_year": 1996, "is_public": True, "industry": "Travel"},
    {"name": "Delivery Hero", "employee_count": 42000, "founded_year": 2011, "is_public": True, "industry": "Food Delivery"},
]


def get_companies() -> List[Company]:
    """Get list of Company objects from the database."""
    return [Company(**company_data) for company_data in ESTABLISHED_COMPANIES]


def get_company_names() -> List[str]:
    """Get list of company names for filtering."""
    return [company["name"] for company in ESTABLISHED_COMPANIES]


def is_established_company(company_name: str) -> bool:
    """Check if a company is in our established companies list."""
    company_names_lower = [name.lower() for name in get_company_names()]
    return company_name.lower() in company_names_lower


def get_company_info(company_name: str) -> Company | None:
    """Get company information by name."""
    for company_data in ESTABLISHED_COMPANIES:
        if company_data["name"].lower() == company_name.lower():
            return Company(**company_data)
    return None
