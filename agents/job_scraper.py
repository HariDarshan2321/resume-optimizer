import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import streamlit as st

def scrape_job_description(url):
    """Scrape job description from a given URL"""

    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find job description content based on common patterns
        job_content = extract_job_content(soup, url)

        if not job_content:
            # Fallback: get all text content
            job_content = soup.get_text()

        # Clean up the text
        job_content = clean_job_text(job_content)

        return job_content

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error processing job description: {str(e)}"

def extract_job_content(soup, url):
    """Extract job description content based on website-specific patterns"""

    domain = urlparse(url).netloc.lower()

    # LinkedIn job posts
    if 'linkedin.com' in domain:
        job_desc = soup.find('div', {'class': re.compile(r'.*job.*description.*', re.I)})
        if job_desc:
            return job_desc.get_text()

    # Indeed job posts
    elif 'indeed.com' in domain:
        job_desc = soup.find('div', {'id': 'jobDescriptionText'}) or soup.find('div', {'class': re.compile(r'.*jobsearch.*', re.I)})
        if job_desc:
            return job_desc.get_text()

    # Glassdoor job posts
    elif 'glassdoor.com' in domain:
        job_desc = soup.find('div', {'class': re.compile(r'.*jobDesc.*', re.I)})
        if job_desc:
            return job_desc.get_text()

    # AngelList/Wellfound
    elif 'angel.co' in domain or 'wellfound.com' in domain:
        job_desc = soup.find('div', {'class': re.compile(r'.*description.*', re.I)})
        if job_desc:
            return job_desc.get_text()

    # Generic patterns for other job sites
    else:
        # Try common class names and IDs
        selectors = [
            'div[class*="job-description"]',
            'div[class*="description"]',
            'div[id*="job-description"]',
            'div[id*="description"]',
            'section[class*="job"]',
            'article[class*="job"]',
            '.job-content',
            '.posting-content',
            '.job-details'
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                return ' '.join([elem.get_text() for elem in elements])

    return None

def clean_job_text(text):
    """Clean and format job description text"""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove common unwanted elements
    text = re.sub(r'(Apply now|Apply for this job|Submit application).*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(Share this job|Save job|Email this job).*', '', text, flags=re.IGNORECASE)

    # Split into lines and clean
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if len(line) > 10 and not line.startswith(('©', 'Cookie', 'Privacy')):
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def validate_job_url(url):
    """Validate if the URL is likely a job posting"""

    if not url:
        return False, "Please provide a URL"

    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "Invalid URL format"
    except:
        return False, "Invalid URL format"

    # Check if it's from a known job site
    job_sites = [
        'linkedin.com', 'indeed.com', 'glassdoor.com', 'monster.com',
        'careerbuilder.com', 'ziprecruiter.com', 'angel.co', 'wellfound.com',
        'stackoverflow.com', 'dice.com', 'simplyhired.com', 'jobs.com'
    ]

    domain = parsed.netloc.lower()
    is_job_site = any(site in domain for site in job_sites)

    if not is_job_site:
        return True, f"Warning: {domain} is not a recognized job site. Proceeding anyway..."

    return True, url

def get_job_description_from_url(url):
    """Main function to get job description from URL with validation"""

    is_valid, message = validate_job_url(url)

    if not is_valid:
        return f"Error: {message}"

    if message.startswith("Warning"):
        st.warning(message)
        url = message.split("Proceeding anyway...")[0].replace("Warning: ", "").replace(" is not a recognized job site.", "")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
    else:
        url = message

    return scrape_job_description(url)
